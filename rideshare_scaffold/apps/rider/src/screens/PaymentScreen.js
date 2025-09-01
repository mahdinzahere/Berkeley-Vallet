import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  TextInput
} from 'react-native';
import { tipsAPI } from '../services/api';

const PaymentScreen = ({ route, navigation }) => {
  const { rideId } = route.params;
  const [tipAmount, setTipAmount] = useState('');
  const [customAmount, setCustomAmount] = useState('');
  const [loading, setLoading] = useState(false);

  const predefinedTips = [
    { amount: 2, label: '$2' },
    { amount: 5, label: '$5' },
    { amount: 10, label: '$10' },
    { amount: 15, label: '$15' },
    { amount: 20, label: '$20' },
    { amount: 0, label: 'Custom' }
  ];

  const handleTipSelection = (amount) => {
    if (amount === 0) {
      setTipAmount(0);
      setCustomAmount('');
    } else {
      setTipAmount(amount);
      setCustomAmount('');
    }
  };

  const handleCustomAmountChange = (text) => {
    const amount = parseFloat(text) || 0;
    setCustomAmount(text);
    setTipAmount(amount);
  };

  const handleSubmitTip = async () => {
    if (!tipAmount || tipAmount <= 0) {
      Alert.alert('Error', 'Please enter a valid tip amount');
      return;
    }

    setLoading(true);
    try {
      await tipsAPI.createTip({
        ride_id: rideId,
        amount: tipAmount
      });
      
      Alert.alert(
        'Success!',
        `Thank you for your $${tipAmount.toFixed(2)} tip!`,
        [
          { text: 'OK', onPress: () => navigation.navigate('History') }
        ]
      );
    } catch (error) {
      Alert.alert('Error', 'Could not process tip. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSkipTip = () => {
    Alert.alert(
      'Skip Tip',
      'Are you sure you want to skip adding a tip?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Skip', onPress: () => navigation.navigate('History') }
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Add a Tip</Text>
        <Text style={styles.subtitle}>Show your appreciation to your driver</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Tips</Text>
        <View style={styles.tipGrid}>
          {predefinedTips.map((tip, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.tipButton,
                tipAmount === tip.amount && styles.selectedTipButton
              ]}
              onPress={() => handleTipSelection(tip.amount)}
            >
              <Text style={[
                styles.tipButtonText,
                tipAmount === tip.amount && styles.selectedTipButtonText
              ]}>
                {tip.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {tipAmount === 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Custom Amount</Text>
          <View style={styles.inputContainer}>
            <Text style={styles.currencySymbol}>$</Text>
            <TextInput
              style={styles.amountInput}
              placeholder="0.00"
              value={customAmount}
              onChangeText={handleCustomAmountChange}
              keyboardType="decimal-pad"
              autoFocus={true}
            />
          </View>
        </View>
      )}

      {tipAmount > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Tip Summary</Text>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Tip Amount</Text>
            <Text style={styles.summaryValue}>${tipAmount.toFixed(2)}</Text>
          </View>
          <View style={styles.summaryRow}>
            <Text style={styles.summaryLabel}>Driver Receives</Text>
            <Text style={styles.summaryValue}>${tipAmount.toFixed(2)}</Text>
          </View>
          <Text style={styles.summaryNote}>
            * 100% of tips go directly to your driver
          </Text>
        </View>
      )}

      <View style={styles.actionSection}>
        {tipAmount > 0 && (
          <TouchableOpacity
            style={[styles.submitButton, loading && styles.submitButtonDisabled]}
            onPress={handleSubmitTip}
            disabled={loading}
          >
            <Text style={styles.submitButtonText}>
              {loading ? 'Processing...' : `Add $${tipAmount.toFixed(2)} Tip`}
            </Text>
          </TouchableOpacity>
        )}
        
        <TouchableOpacity
          style={styles.skipButton}
          onPress={handleSkipTip}
        >
          <Text style={styles.skipButtonText}>Skip Tip</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.infoSection}>
        <Text style={styles.infoTitle}>About Tips</Text>
        <Text style={styles.infoText}>
          • Tips are completely optional but greatly appreciated
        </Text>
        <Text style={styles.infoText}>
          • 100% of your tip goes directly to your driver
        </Text>
        <Text style={styles.infoText}>
          • Tips help drivers earn a living wage
        </Text>
        <Text style={styles.infoText}>
          • You can always add a tip later from your ride history
        </Text>
      </View>
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
  tipGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  tipButton: {
    width: '30%',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedTipButton: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  tipButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  selectedTipButtonText: {
    color: 'white',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 16,
  },
  currencySymbol: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginRight: 8,
  },
  amountInput: {
    flex: 1,
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    paddingVertical: 16,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  summaryLabel: {
    fontSize: 16,
    color: '#666',
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  summaryNote: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    marginTop: 12,
  },
  actionSection: {
    marginTop: 20,
    marginHorizontal: 20,
    marginBottom: 20,
  },
  submitButton: {
    backgroundColor: '#34C759',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
  },
  submitButtonDisabled: {
    backgroundColor: '#ccc',
  },
  submitButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  skipButton: {
    backgroundColor: 'transparent',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  skipButtonText: {
    color: '#666',
    fontSize: 16,
    fontWeight: '600',
  },
  infoSection: {
    backgroundColor: 'white',
    marginHorizontal: 20,
    marginBottom: 40,
    padding: 20,
    borderRadius: 12,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
});

export default PaymentScreen;
