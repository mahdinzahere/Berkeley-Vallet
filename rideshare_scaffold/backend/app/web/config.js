// Valleyet Configuration File
// Replace these values with your actual API keys and configuration

const config = {
    // Google Maps API Configuration
    googleMaps: {
        apiKey: 'YOUR_GOOGLE_MAPS_API_KEY_HERE', // Replace with your actual Google Maps API key
        libraries: ['places'],
        defaultLocation: {
            lat: 37.7749, // San Francisco coordinates (change to your preferred default)
            lng: -122.4194
        }
    },
    
    // App Configuration
    app: {
        name: 'Valleyet',
        version: '1.0.0',
        description: 'Your Trusted Rideshare Partner'
    },
    
    // API Configuration
    api: {
        baseUrl: 'http://localhost:8000',
        endpoints: {
            auth: '/auth',
            rides: '/rides',
            drivers: '/drivers',
            users: '/users'
        }
    },
    
    // Ride Configuration
    ride: {
        defaultRadius: 5000, // meters
        maxWaitTime: 300, // seconds
        rideTypes: {
            economy: {
                name: 'Economy',
                multiplier: 1.0,
                icon: 'fas fa-car'
            },
            comfort: {
                name: 'Comfort',
                multiplier: 1.5,
                icon: 'fas fa-car-side'
            },
            premium: {
                name: 'Premium',
                multiplier: 2.0,
                icon: 'fas fa-car-rear'
            }
        }
    },
    
    // Driver Configuration
    driver: {
        minRating: 4.0,
        maxDistance: 10000, // meters
        onlineStatuses: {
            offline: 'offline',
            online: 'online',
            busy: 'busy'
        }
    }
};

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    window.ValleyetConfig = config;
}
