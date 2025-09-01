import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
  RefreshControl
} from 'react-native';
import { ridesAPI } from '../services/api';

const RideHistoryScreen = ({ navigation }) => {
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadRides();
  }, []);

  const loadRides = async () => {
    setLoading(true);
    try {
      const response = await ridesAPI.getRides();
      setRides(response.data);
    } catch (error) {
      Alert.alert('Error', 'Could not load ride history');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadRides();
    setRefreshing(false);
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

  const renderRideItem = ({ item }) => (
    <TouchableOpacity
      style={styles.rideItem}
      onPress={() => navigation.navigate('RideDetails', { rideId: item.id })}
    >
      <View style={styles.rideHeader}>
        <Text style={styles.rideDate}>
          {new Date(item.created_at).toLocaleDateString()}
        </Text>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
          <Text style={styles.statusText}>{getStatusText(item.status)}</Text>
        </View>
      </View>
      
      <View style={styles.rideDetails}>
        <Text style={styles.locationText} numberOfLines={1}>
          📍 {item.pickup_address}
        </Text>
        <Text style={styles.locationText} numberOfLines={1}>
          🎯 {item.dropoff_address}
        </Text>
      </View>
      
      <View style={styles.rideFooter}>
        <Text style={styles.fareText}>${item.fare.toFixed(2)}</Text>
        <Text style={styles.distanceText}>{item.distance_miles.toFixed(1)} miles</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading && rides.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text>Loading rides...</Text>
      </View>
    );
  }

  if (rides.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.noRidesText}>No rides yet</Text>
        <Text style={styles.noRidesSubtext}>Your ride history will appear here</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ride History</Text>
      <FlatList
        data={rides}
        renderItem={renderRideItem}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    padding: 20,
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  listContainer: {
    padding: 20,
  },
  rideItem: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  rideHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  rideDate: {
    fontSize: 14,
    color: '#666',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  rideDetails: {
    marginBottom: 12,
  },
  locationText: {
    fontSize: 16,
    marginBottom: 4,
    color: '#333',
  },
  rideFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  fareText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  distanceText: {
    fontSize: 14,
    color: '#666',
  },
  noRidesText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 8,
  },
  noRidesSubtext: {
    fontSize: 16,
    color: '#999',
  },
});

export default RideHistoryScreen;
