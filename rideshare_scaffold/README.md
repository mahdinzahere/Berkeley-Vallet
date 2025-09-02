# 🚗 Valleyet - Your Trusted Rideshare Partner

**Valleyet** is a complete, functional Uber clone built with modern web technologies, featuring real-time ride booking, AI-powered pricing, Google Maps integration, and separate dashboards for riders and drivers.

## ✨ Features

### 🎯 **Main Website (Uber-like Landing Page)**
- **Search Bar with Google Maps Integration**: Enter pickup and destination locations with autocomplete
- **Current Location Detection**: Automatically detects user's location for pickup
- **Real-time Pricing**: See prices only after entering both locations (AI-powered pricing algorithm)
- **Responsive Design**: Beautiful, modern interface that works on all devices
- **Login/Signup System**: Seamless authentication flow with role-based routing

### 🚖 **Rider Dashboard**
- **Interactive Google Maps**: Real-time location tracking and route visualization
- **Smart Pricing System**: AI-powered pricing that calculates fares based on distance and time
- **Pickup Time Selection**: Choose between immediate pickup or scheduled rides
- **Ride Type Selection**: Economy, Comfort, and Premium options with real-time pricing
- **Past Rides History**: Complete ride history with ratings, drivers, and trip details
- **Real-time Driver Tracking**: Live updates on driver location and ETA
- **Location Autocomplete**: Google Places API integration for accurate addresses

### 🚘 **Driver Dashboard**
- **Real-time Ride Requests**: Live incoming ride requests with passenger details
- **Interactive Map Interface**: Google Maps with pickup/destination markers
- **Online/Offline Toggle**: Control when to receive ride requests
- **Ride Management**: Accept, decline, start, and complete rides
- **Earnings Tracking**: Real-time stats and earnings calculation
- **Ride History**: Complete history of completed rides with earnings
- **Location Updates**: Continuous GPS tracking for accurate driver positioning

### 🗺️ **Google Maps Integration**
- **Full Maps API**: Interactive maps with custom markers and styling
- **Location Services**: GPS integration for real-time positioning
- **Address Autocomplete**: Google Places API for accurate location input
- **Route Visualization**: Visual representation of pickup and destination points
- **Real-time Updates**: Live location tracking for both riders and drivers

### 🤖 **AI-Powered Features**
- **Dynamic Pricing**: Intelligent fare calculation based on distance, time, and demand
- **Route Optimization**: Smart routing algorithms for efficient trips
- **Demand Prediction**: AI-based pricing adjustments for peak hours
- **Real-time Analytics**: Live data processing for optimal ride matching

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Google Maps API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rideshare_scaffold
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database and API credentials
   ```

5. **Set up Google Maps API**
   - Get API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` in:
     - `backend/app/web/index.html`
     - `backend/app/web/rider-dashboard.html`
     - `backend/app/web/driver-dashboard.html`

6. **Start the server**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

7. **Access Valleyet**
   - **Main Website**: http://localhost:8000/
   - **Rider Dashboard**: http://localhost:8000/rider-dashboard
   - **Driver Dashboard**: http://localhost:8000/driver-dashboard
   - **API Documentation**: http://localhost:8000/docs

## 🎮 How to Use

### For Riders
1. **Visit the main page** and enter pickup/destination locations
2. **Click "See Prices"** to view ride options and pricing
3. **Select ride type** (Economy, Comfort, or Premium)
4. **Book your ride** and track your driver in real-time
5. **View ride history** in the Past Rides tab

### For Drivers
1. **Go online** using the toggle button
2. **Receive ride requests** in real-time
3. **Accept rides** and view passenger details
4. **Navigate to pickup** using integrated maps
5. **Complete rides** and track earnings

## 🏗️ Architecture

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript ES6+**: Interactive functionality and real-time updates
- **Google Maps API**: Location services and mapping
- **Font Awesome**: Professional icons and UI elements

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Robust database with pgvector extension
- **SQLAlchemy**: Database ORM and migrations
- **Uvicorn**: ASGI server for production deployment

### Key Components
- **Real-time Location Tracking**: GPS integration with continuous updates
- **AI Pricing Engine**: Dynamic fare calculation algorithms
- **Ride Matching System**: Intelligent driver-rider pairing
- **Payment Integration**: Ready for Stripe integration
- **WebSocket Support**: Real-time communication infrastructure

## 🔧 Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/rideshare
GOOGLE_MAPS_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### Google Maps API Setup
1. Enable Google Maps JavaScript API
2. Enable Google Places API
3. Enable Geocoding API
4. Set up billing and quotas
5. Restrict API key to your domain

## 📱 Mobile Responsiveness

Valleyet is fully responsive and works seamlessly on:
- **Desktop computers**
- **Tablets**
- **Mobile phones**
- **All modern browsers**

## 🚀 Deployment

### Production Deployment
1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Set up Google Maps API with domain restrictions**
4. **Deploy using Docker or direct server deployment**
5. **Set up SSL certificates**
6. **Configure reverse proxy (nginx/Apache)**

### Docker Deployment
```bash
docker-compose up -d
```

## 🔒 Security Features

- **CORS protection** with configurable origins
- **Input validation** and sanitization
- **SQL injection protection** via SQLAlchemy
- **XSS protection** with proper content encoding
- **Rate limiting** capabilities
- **Secure authentication** system

## 📊 Performance Features

- **Async/await** support for high concurrency
- **Database connection pooling**
- **Static file serving** optimization
- **Caching strategies** for frequently accessed data
- **Real-time updates** via WebSocket connections

## 🧪 Testing

### Manual Testing
1. **Test rider flow**: Book rides, track drivers, view history
2. **Test driver flow**: Go online, accept rides, complete trips
3. **Test maps integration**: Location detection, routing, markers
4. **Test responsive design**: Various screen sizes and devices

### Automated Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests (if implemented)
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Issues**: Create an issue in the GitHub repository
- **Documentation**: Check the API docs at `/docs`
- **Community**: Join our developer community

## 🎯 Roadmap

### Upcoming Features
- **Payment Integration**: Stripe payment processing
- **Push Notifications**: Real-time alerts for riders and drivers
- **Advanced Analytics**: Driver performance metrics and insights
- **Multi-language Support**: Internationalization features
- **Mobile Apps**: Native iOS and Android applications

### Future Enhancements
- **Machine Learning**: Advanced pricing and demand prediction
- **Blockchain Integration**: Decentralized ride sharing
- **IoT Integration**: Smart city connectivity
- **AR Navigation**: Augmented reality directions

---

**Valleyet** - Safe, Reliable, Valleyet. 🚗✨

*Built with ❤️ for the modern rideshare experience*