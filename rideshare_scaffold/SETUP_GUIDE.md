# 🚀 Valey Setup Guide - Database & Integrations

## 📋 **Prerequisites**

Before setting up Valey, ensure you have:

- ✅ **Python 3.13+** installed
- ✅ **PostgreSQL** database running
- ✅ **Google Cloud CLI** installed
- ✅ **Twilio Account** (for SMS)
- ✅ **SendGrid Account** (for emails)
- ✅ **Google OAuth Credentials** (for Google Sign-In)

## 🗄️ **Database Setup**

### **1. Install PostgreSQL**
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### **2. Create Database**
```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE rideshare;
CREATE USER valey_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE rideshare TO valey_user;
\q
```

### **3. Update Environment Variables**
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your database credentials
DATABASE_URL=postgresql://valey_user:your_secure_password@localhost:5432/rideshare
```

## 🔐 **Authentication Setup**

### **1. Google OAuth Setup**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback`
   - `https://yourdomain.com/auth/google/callback`

### **2. Update Environment Variables**
```bash
# Add to .env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
JWT_SECRET=your_super_secure_jwt_secret_key
```

## 📱 **Twilio Setup (SMS)**

### **1. Create Twilio Account**
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Purchase a phone number for SMS

### **2. Update Environment Variables**
```bash
# Add to .env file
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## 📧 **SendGrid Setup (Email)**

### **1. Create SendGrid Account**
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key
3. Verify your sender identity

### **2. Update Environment Variables**
```bash
# Add to .env file
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@valey.com
```

## 💳 **Stripe Setup (Payments)**

### **1. Create Stripe Account**
1. Sign up at [Stripe](https://stripe.com/)
2. Get your API keys
3. Set up webhooks

### **2. Update Environment Variables**
```bash
# Add to .env file
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## 🚀 **Installation & Setup**

### **1. Install Dependencies**
```bash
# Navigate to project directory
cd rideshare_scaffold

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt
```

### **2. Database Migration**
```bash
# Navigate to backend directory
cd backend

# Run database migrations
alembic upgrade head
```

### **3. Start the Server**
```bash
# Start the development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 **Access Your Application**

- **Main Website**: http://localhost:8000/
- **Rider Dashboard**: http://localhost:8000/rider-dashboard
- **Driver Dashboard**: http://localhost:8000/driver-dashboard
- **API Documentation**: http://localhost:8000/docs

## 🔧 **Configuration Files**

### **Environment Variables (.env)**
```bash
# Database
DATABASE_URL=postgresql://valey_user:password@localhost:5432/rideshare

# JWT
JWT_SECRET=your-super-secret-jwt-key

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@valey.com

# Stripe
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## 📊 **Database Schema**

The application includes the following main tables:

- **users**: User accounts (riders and drivers)
- **driver_profiles**: Driver-specific information
- **rides**: Ride requests and history
- **tips**: Tip transactions
- **ride_requests**: Active ride requests

## 🔒 **Security Features**

- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **Password Hashing**: SHA-256 password encryption
- ✅ **Google OAuth**: Secure third-party authentication
- ✅ **CORS Protection**: Cross-origin request security
- ✅ **Input Validation**: Pydantic schema validation

## 📱 **Mobile Features**

- ✅ **Responsive Design**: Works on all devices
- ✅ **Location Services**: GPS integration
- ✅ **Push Notifications**: Real-time updates
- ✅ **Offline Support**: Basic offline functionality

## 🚀 **Production Deployment**

### **1. Environment Setup**
```bash
# Set production environment variables
export ENVIRONMENT=production
export DATABASE_URL=postgresql://user:pass@prod-db:5432/rideshare
```

### **2. Database Migration**
```bash
# Run production migrations
alembic upgrade head
```

### **3. Start Production Server**
```bash
# Use production ASGI server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in .env
   - Ensure user has proper permissions

2. **Google Maps API Error**
   - Verify API key is correct
   - Check API key restrictions
   - Ensure billing is enabled

3. **Twilio SMS Not Working**
   - Verify account credentials
   - Check phone number format
   - Ensure account has sufficient balance

4. **SendGrid Email Issues**
   - Verify API key
   - Check sender verification
   - Review email templates

### **Logs and Debugging**
```bash
# Check application logs
tail -f logs/app.log

# Debug mode
export DEBUG=true
python -m uvicorn app.main:app --reload --log-level debug
```

## 📞 **Support**

For technical support or questions:

- **Documentation**: Check the `/docs` endpoint
- **Issues**: Create GitHub issues
- **Email**: support@valey.com

## 🎉 **You're Ready!**

Your Valey rideshare application is now set up with:

- ✅ **Real Database Integration**
- ✅ **Google OAuth Authentication**
- ✅ **Twilio SMS Notifications**
- ✅ **SendGrid Email Service**
- ✅ **Stripe Payment Processing**
- ✅ **Google Maps Integration**
- ✅ **Real-time Features**

**Happy coding! 🚗💨**
