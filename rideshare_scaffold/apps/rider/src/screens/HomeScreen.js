import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  Platform
} from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';
import { GooglePlacesAutocomplete } from 'react-native-google-places-autocomplete';
import { useSocket } from '../context/SocketContext';
import { ridesAPI } from '../services/api';

const { width, height } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const [location, setLocation] = useState(null);
  const [pickupLocation, setPickupLocation] = useState(null);
  const [dropoffLocation, setDropoffLocation] = useState(null);
  const [rideQuote, setRideQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentRide, setCurrentRide] = useState(null);
  
  const mapRef = useRef(null);
  const { socket, isConnected } = useSocket();

  useEffect(() => {
    getCurrentLocation();
    setupSocketListeners();
  }, []);

  const getCurrentLocation = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission denied', 'Location permission is required');
        return;
      }

      const currentLocation = await Location.getCurrentPositionAsync({});
      const { latitude, longitude } = currentLocation.coords;
      setLocation({ latitude, longitude });
      
      // Set pickup location to current location by default
      setPickupLocation({ latitude, longitude, address: 'Current Location' });
    } catch (error) {
      console.error('Error getting location:', error);
      Alert.alert('Error', 'Could not get your location');
    }
  };

  const setupSocketListeners = () => {
    if (socket) {
      socket.on('ride_assigned', (data) => {
        Alert.alert('Driver Assigned!', 'A driver has accepted your ride');
        setCurrentRide(data);
      });

      socket.on('ride_status_update', (data) => {
        if (data.status === 'arrived') {
          Alert.alert('Driver Arrived', 'Your driver has arrived at pickup location');
        } else if (data.status === 'started') {
          Alert.alert('Ride Started', 'Your ride is now in progress');
        } else if (data.status === 'completed') {
          Alert.alert('Ride Completed', 'Your ride has been completed');
          setCurrentRide(null);
          navigation.navigate('Payment', { rideId: data.ride_id });
        }
      });

      socket.on('driver_location', (data) => {
        // Update driver location on map
        console.log('Driver location update:', data);
      });
    }
  };

  const handleLocationSelect = (place, type) => {
    const { geometry, formatted_address } = place;
    const locationData = {
      latitude: geometry.location.lat,
      longitude: geometry.location.lng,
      address: formatted_address
    };

    if (type === 'pickup') {
      setPickupLocation(locationData);
    } else {
      setDropoffLocation(locationData);
    }
  };

  const getRideQuote = async () => {
    if (!pickupLocation || !dropoffLocation) {
      Alert.alert('Error', 'Please select both pickup and dropoff locations');
      return;
    }

    setLoading(true);
    try {
      const quote = await ridesAPI.getQuote({
        pickup_address: pickupLocation.address,
        pickup_latitude: pickupLocation.latitude,
        pickup_longitude: pickupLocation.longitude,
        dropoff_address: dropoffLocation.address,
        dropoff_latitude: dropoffLocation.latitude,
        dropoff_longitude: dropoffLocation.longitude
      });
      
      setRideQuote(quote.data);
    } catch (error) {
      Alert.alert('Error', 'Could not get ride quote');
    } finally {
      setLoading(false);
    }
  };

  const requestRide = async () => {
    if (!rideQuote) {
      Alert.alert('Error', 'Please get a quote first');
      return;
    }

    setLoading(true);
    try {
      const ride = await ridesAPI.requestRide({
        pickup_address: pickupLocation.address,
        pickup_latitude: pickupLocation.latitude,
        pickup_longitude: pickupLocation.longitude,
        dropoff_address: dropoffLocation.address,
        dropoff_latitude: dropoffLocation.latitude,
        dropoff_longitude: dropoffLocation.longitude
      });
      
      setCurrentRide(ride.data);
      Alert.alert('Ride Requested', 'Looking for drivers...');
    } catch (error) {
      Alert.alert('Error', 'Could not request ride');
    } finally {
      setLoading(false);
    }
  };

  const cancelRide = async () => {
    if (!currentRide) return;

    try {
      await ridesAPI.cancelRide(currentRide.id);
      setCurrentRide(null);
      Alert.alert('Ride Cancelled', 'Your ride has been cancelled');
    } catch (error) {
      Alert.alert('Error', 'Could not cancel ride');
    }
  };

  return (
    <View style={styles.container}>
      <MapView
        ref={mapRef}
        style={styles.map}
        provider={PROVIDER_GOOGLE}
        initialRegion={{
          latitude: location?.latitude || 37.8716,
          longitude: location?.longitude || -122.2727,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
        showsUserLocation={true}
        showsMyLocationButton={true}
      >
        {pickupLocation && (
          <Marker
            coordinate={{
              latitude: pickupLocation.latitude,
              longitude: pickupLocation.longitude
            }}
            title="Pickup"
            pinColor="green"
          />
        )}
        
        {dropoffLocation && (
          <Marker
            coordinate={{
              latitude: dropoffLocation.latitude,
              longitude: dropoffLocation.longitude
            }}
            title="Dropoff"
            pinColor="red"
          />
        )}
      </MapView>

      <View style={styles.searchContainer}>
        <GooglePlacesAutocomplete
          placeholder="Pickup location"
          onPress={(data, details = null) => handleLocationSelect(details, 'pickup')}
          query={{
            key: 'YOUR_GOOGLE_PLACES_API_KEY',
            language: 'en',
          }}
          styles={{
            container: styles.autocompleteContainer,
            textInput: styles.autocompleteInput,
          }}
        />
        
        <GooglePlacesAutocomplete
          placeholder="Where to?"
          onPress={(data, details = null) => handleLocationSelect(details, 'dropoff')}
          query={{
            key: 'YOUR_GOOGLE_PLACES_API_KEY',
            language: 'en',
          }}
          styles={{
            container: styles.autocompleteContainer,
            textInput: styles.autocompleteInput,
          }}
        />
      </View>

      {rideQuote && (
        <View style={styles.quoteContainer}>
          <Text style={styles.quoteText}>
            Estimated Fare: ${rideQuote.fare.toFixed(2)}
          </Text>
          <Text style={styles.quoteText}>
            Distance: {rideQuote.distance_miles.toFixed(1)} miles
          </Text>
          <Text style={styles.quoteText}>
            Time: ~{rideQuote.estimated_time_minutes} min
          </Text>
          
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={requestRide}
            disabled={loading}
          >
            <Text style={styles.buttonText}>
              {loading ? 'Requesting...' : 'Request Ride'}
            </Text>
          </TouchableOpacity>
        </View>
      )}

      {!rideQuote && pickupLocation && dropoffLocation && (
        <TouchableOpacity
          style={styles.quoteButton}
          onPress={getRideQuote}
        >
          <Text style={styles.quoteButtonText}>Get Quote</Text>
        </TouchableOpacity>
      )}

      {currentRide && (
        <View style={styles.currentRideContainer}>
          <Text style={styles.currentRideText}>Ride in Progress</Text>
          <TouchableOpacity
            style={styles.cancelButton}
            onPress={cancelRide}
          >
            <Text style={styles.cancelButtonText}>Cancel Ride</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  searchContainer: {
    position: 'absolute',
    top: 50,
    left: 20,
    right: 20,
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  autocompleteContainer: {
    flex: 0,
    marginBottom: 10,
  },
  autocompleteInput: {
    height: 40,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 4,
    paddingHorizontal: 10,
  },
  quoteContainer: {
    position: 'absolute',
    bottom: 100,
    left: 20,
    right: 20,
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  quoteText: {
    fontSize: 16,
    marginBottom: 8,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  quoteButton: {
    position: 'absolute',
    bottom: 100,
    left: 20,
    right: 20,
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  quoteButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  currentRideContainer: {
    position: 'absolute',
    bottom: 100,
    left: 20,
    right: 20,
    backgroundColor: '#FF9500',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  currentRideText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
  },
  cancelButton: {
    backgroundColor: '#FF3B30',
    borderRadius: 6,
    padding: 10,
    paddingHorizontal: 20,
  },
  cancelButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
});

export default HomeScreen;
