import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Switch,
  Alert,
  ScrollView
} from 'react-native';
import * as Location from 'expo-location';
import { useSocket } from '../context/SocketContext';

const HomeScreen = ({ navigation }) => {
  const [isOnline, setIsOnline] = useState(false);
  const [currentLocation, setCurrentLocation] = useState(null);
  const [locationPermission, setLocationPermission] = useState(false);

  const { socket, emit } = useSocket();

  useEffect(() => {
    checkLocationPermission();
  }, []);

  const checkLocationPermission = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      setLocationPermission(status === 'granted');
      
      if (status === 'granted') {
        getCurrentLocation();
      }
    } catch (error) {
      console.error('Error checking location permission:', error);
    }
  };

  const getCurrentLocation = async () => {
    try {
      const location = await Location.getCurrentPositionAsync({});
      const { latitude, longitude } = location.coords;
      setCurrentLocation({ latitude, longitude });
    } catch (error) {
      console.error('Error getting location:', error);
    }
  };

  const toggleOnlineStatus = async () => {
    if (!locationPermission) {
      Alert.alert('Permission Required', 'Location permission is required to go online');
      return;
    }

    if (!currentLocation) {
      Alert.alert('Location Required', 'Please wait for location to be determined');
      return;
    }

    const newStatus = !isOnline;
    setIsOnline(newStatus);

    if (newStatus) {
      // Go online
      try {
        // In a real app, you'd call the API here
        emit('driver_online', {
          user_id: 1, // Replace with actual user ID
          latitude: currentLocation.latitude,
          longitude: currentLocation.longitude
        });
        
        Alert.alert('Online', 'You are now online and can receive ride requests');
      } catch (error) {
        Alert.alert('Error', 'Could not go online');
        setIsOnline(false);
      }
    } else {
      // Go offline
      try {
        emit('driver_offline', {
          user_id: 1 // Replace with actual user ID
        });
        
        Alert.alert('Offline', 'You are now offline');
      } catch (error) {
        Alert.alert('Error', 'Could not go offline');
        setIsOnline(true);
      }
    }
  };

  const startLocationUpdates = () => {
    if (isOnline && locationPermission) {
      // Start location updates every 10 seconds when online
      const locationSubscription = Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 10000,
          distanceInterval: 10
        },
        (location) => {
          const { latitude, longitude } = location.coords;
          setCurrentLocation({ latitude, longitude });
          
          // Update location on server
          if (socket) {
            emit('update_location', {
              user_id: 1, // Replace with actual user ID
              latitude,
              longitude
            });
          }
        }
      );

      return () => locationSubscription?.remove();
    }
  };

  useEffect(() => {
    if (isOnline) {
      const cleanup = startLocationUpdates();
      return cleanup;
    }
  }, [isOnline]);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Driver Dashboard</Text>
        <Text style={styles.subtitle}>
          {isOnline ? 'You are online and receiving ride requests' : 'Go online to start earning'}
        </Text>
      </View>

      <View style={styles.statusCard}>
        <View style={styles.statusHeader}>
          <Text style={styles.statusTitle}>Online Status</Text>
          <Switch
            value={isOnline}
            onValueChange={toggleOnlineStatus}
            trackColor={{ false: '#767577', true: '#34C759' }}
            thumbColor={isOnline ? '#ffffff' : '#f4f3f4'}
          />
        </View>
        
        <View style={styles.statusIndicator}>
          <View style={[styles.statusDot, { backgroundColor: isOnline ? '#34C759' : '#FF3B30' }]} />
          <Text style={[styles.statusText, { color: isOnline ? '#34C759' : '#FF3B30' }]}>
            {isOnline ? 'ONLINE' : 'OFFLINE'}
          </Text>
        </View>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.cardTitle}>Location Information</Text>
        
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Permission Status:</Text>
          <Text style={[styles.infoValue, { color: locationPermission ? '#34C759' : '#FF3B30' }]}>
            {locationPermission ? 'Granted' : 'Denied'}
          </Text>
        </View>
        
        {currentLocation && (
          <>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Latitude:</Text>
              <Text style={styles.infoValue}>{currentLocation.latitude.toFixed(6)}</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Longitude:</Text>
              <Text style={styles.infoValue}>{currentLocation.longitude.toFixed(6)}</Text>
            </View>
          </>
        )}
        
        <TouchableOpacity
          style={styles.locationButton}
          onPress={getCurrentLocation}
        >
          <Text style={styles.locationButtonText}>Update Location</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.actionCard}>
        <Text style={styles.cardTitle}>Quick Actions</Text>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('RideRequests')}
        >
          <Text style={styles.actionButtonText}>View Ride Requests</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Profile')}
        >
          <Text style={styles.actionButtonText}>Driver Profile</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('StripeConnect')}
        >
          <Text style={styles.actionButtonText}>Stripe Connect Setup</Text>
        </TouchableOpacity>
      </View>

      {!locationPermission && (
        <View style={styles.warningCard}>
          <Text style={styles.warningTitle}>⚠️ Location Permission Required</Text>
          <Text style={styles.warningText}>
            Location permission is required to go online and receive ride requests. 
            Please enable location access in your device settings.
          </Text>
          
          <TouchableOpacity
            style={styles.permissionButton}
            onPress={checkLocationPermission}
          >
            <Text style={styles.permissionButtonText}>Request Permission</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: 'white',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  statusCard: {
    backgroundColor: 'white',
    margin: 20,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  statusHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  statusTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  infoCard: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoLabel: {
    fontSize: 16,
    color: '#666',
  },
  infoValue: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  locationButton: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
    marginTop: 16,
  },
  locationButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  actionCard: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  actionButton: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  actionButtonText: {
    color: '#333',
    fontSize: 16,
    fontWeight: '600',
  },
  warningCard: {
    backgroundColor: '#FFF3CD',
    marginHorizontal: 20,
    marginBottom: 40,
    padding: 20,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#FFEAA7',
  },
  warningTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#856404',
    marginBottom: 12,
  },
  warningText: {
    fontSize: 14,
    color: '#856404',
    lineHeight: 20,
    marginBottom: 16,
  },
  permissionButton: {
    backgroundColor: '#856404',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  permissionButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default HomeScreen;
