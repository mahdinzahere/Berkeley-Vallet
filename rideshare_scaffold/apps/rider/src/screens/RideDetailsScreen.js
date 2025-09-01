import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  ActivityIndicator
} from 'react-native';
import { ridesAPI } from '../services/api';

const RideDetailsScreen = ({ route, navigation }) => {
  const { rideId } = route.params;
  const [ride, setRide] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRideDetails();
  }, [rideId]);

  const loadRideDetails = async () => {
    try {
      const response = await ridesAPI.getRide(rideId);
      setRide(response.data);
    } catch (error) {
      Alert.alert('Error', 'Could not load ride details');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelRide = async () => {
    Alert.alert(
      'Cancel Ride',
      'Are you sure you want to cancel this ride?',
      [
        { text: 'No', style: 'cancel' },
        { text: 'Yes', style: 'destructive', onPress: async () => {
          try {
            await ridesAPI.cancelRide(rideId);
            Alert.alert('Success', 'Ride cancelled successfully');
            navigation.goBack();
          } catch (error) {
            Alert.alert('Error', 'Could not cancel ride');
          }
        }}
      ]
    );
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#34C759';
      case 'cancelled':
        return '#FF3B30';
      case 'in_progress':
        return '#007AFF';
      default:
        return '#8E8E93';
    }
  };

  const getStatusText = (status) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Loading ride details...</Text>
      </View>
    );
  }

  if (!ride) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Ride not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Ride Details</Text>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(ride.status) }]}>
          <Text style={styles.statusText}>{getStatusText(ride.status)}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Trip Information</Text>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>Ride ID</Text>
          <Text style={styles.value}>#{ride.id}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>Date</Text>
          <Text style={styles.value}>
            {new Date(ride.created_at).toLocaleDateString()}
          </Text>
        </View>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>Time</Text>
          <Text style={styles.value}>
            {new Date(ride.created_at).toLocaleTimeString()}
          </Text>
        </View>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>Distance</Text>
          <Text style={styles.value}>{ride.distance_miles.toFixed(1)} miles</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>Fare</Text>
          <Text style={styles.fareValue}>${ride.fare.toFixed(2)}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Locations</Text>
        
        <View style={styles.locationContainer}>
          <Text style={styles.locationLabel}>📍 Pickup</Text>
          <Text style={styles.locationText}>{ride.pickup_address}</Text>
        </View>
        
        <View style={styles.locationContainer}>
          <Text style={styles.locationLabel}>🎯 Dropoff</Text>
          <Text style={styles.locationText}>{ride.dropoff_address}</Text>
        </View>
      </View>

      {ride.driver_id && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Driver Information</Text>
          
          <View style={styles.infoRow}>
            <Text style={styles.label}>Driver ID</Text>
            <Text style={styles.value}>#{ride.driver_id}</Text>
          </View>
          
          <TouchableOpacity style={styles.contactButton}>
            <Text style={styles.contactButtonText}>Contact Driver</Text>
          </TouchableOpacity>
        </View>
      )}

      {ride.status === 'requested' && (
        <View style={styles.actionSection}>
          <TouchableOpacity
            style={styles.cancelButton}
            onPress={handleCancelRide}
          >
            <Text style={styles.cancelButtonText}>Cancel Ride</Text>
          </TouchableOpacity>
        </View>
      )}

      {ride.status === 'completed' && (
        <View style={styles.actionSection}>
          <TouchableOpacity
            style={styles.tipButton}
            onPress={() => navigation.navigate('Payment', { rideId: ride.id })}
          >
            <Text style={styles.tipButtonText}>Add Tip</Text>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  errorText: {
    fontSize: 18,
    color: '#FF3B30',
  },
  header: {
    backgroundColor: 'white',
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  statusText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  section: {
    backgroundColor: 'white',
    marginTop: 20,
    padding: 20,
    marginHorizontal: 20,
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  label: {
    fontSize: 16,
    color: '#666',
  },
  value: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  fareValue: {
    fontSize: 18,
    color: '#007AFF',
    fontWeight: 'bold',
  },
  locationContainer: {
    marginBottom: 16,
  },
  locationLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  locationText: {
    fontSize: 16,
    color: '#666',
    lineHeight: 22,
  },
  contactButton: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
    marginTop: 12,
  },
  contactButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  actionSection: {
    marginTop: 20,
    marginHorizontal: 20,
    marginBottom: 40,
  },
  cancelButton: {
    backgroundColor: '#FF3B30',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  tipButton: {
    backgroundColor: '#34C759',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  tipButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default RideDetailsScreen;
