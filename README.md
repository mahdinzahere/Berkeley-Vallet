# 🚗 UC Berkeley Rideshare MVP

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React Native](https://img.shields.io/badge/React%20Native-0.72+-blue.svg)](https://reactnative.dev)
[![Stripe](https://img.shields.io/badge/Stripe-Connect-orange.svg)](https://stripe.com)
[![AI](https://img.shields.io/badge/AI-LangChain-purple.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready, full-stack rideshare application built for UC Berkeley's pilot program. Features real-time ride matching, Stripe Connect payments with 0% platform fees, and AI-powered support through LangChain.

## ✨ Features

### 🚀 Core Functionality
- **Magic Link Authentication** - Secure email/phone verification
- **Real-time Ride Matching** - Socket.IO powered driver-rider communication
- **Stripe Connect Integration** - Direct payments to drivers (0% platform fee)
- **Location Services** - GPS tracking and route optimization
- **Payment Processing** - Secure ride payments and tipping system

### 🤖 AI Support System
- **LangChain RAG Pipeline** - Intelligent support using document embeddings
- **OpenAI Integration** - GPT-4 powered responses
- **Document Knowledge Base** - FAQ, policies, and campus playbook
- **Grounded Responses** - AI answers with source citations

### 📱 Mobile Applications
- **Rider App** - Request rides, track drivers, manage payments
- **Driver App** - Accept rides, update status, manage earnings
- **Real-time Updates** - Live notifications and status changes

### 🌐 Web Dashboard
- **Admin Interface** - Monitor rides, drivers, and system health
- **Real-time Analytics** - Live data visualization
- **AI Support Testing** - Interactive support system interface

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Rider App     │    │  Driver App     │    │  Web Dashboard  │
│  (React Native) │    │ (React Native)  │    │   (HTML/JS)     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │      FastAPI Backend      │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Socket.IO Server  │  │
                    │  └─────────────────────┘  │
                    │  ┌─────────────────────┐  │
                    │  │   Stripe Connect    │  │
                    │  └─────────────────────┘  │
                    │  ┌─────────────────────┐  │
                    │  │   LangChain RAG     │  │
                    │  └─────────────────────┘  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    PostgreSQL + pgvector  │
                    │    (User data + AI docs)  │
                    └───────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Stripe Account
- OpenAI API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/uc-berkeley-rideshare.git
cd uc-berkeley-rideshare
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required environment variables:
```env
DATABASE_URL=postgresql://user:password@localhost/rideshare
JWT_SECRET=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
OPENAI_API_KEY=sk-...
```

### 3. Complete Setup
```bash
# Install dependencies and setup database
make dev-setup

# Setup AI support system
make embed-docs

# Start the backend
make run-backend
```

### 4. Access the Application
- **Web Dashboard**: http://localhost:8000/dashboard
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Start Mobile Apps
```bash
# Terminal 1 - Rider App
cd apps/rider && npm start

# Terminal 2 - Driver App  
cd apps/driver && npm start
```

## 📁 Project Structure

```
uc-berkeley-rideshare/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── ai/            # LangChain RAG implementation
│   │   ├── routes/        # API endpoints
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   └── main.py        # FastAPI application
│   ├── docs/              # AI knowledge base
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend containerization
├── apps/
│   ├── rider/             # Rider mobile app
│   └── driver/            # Driver mobile app
├── docker-compose.yml      # Development environment
├── Makefile               # Development commands
└── README.md              # This file
```

## 🛠️ Development Commands

```bash
make help              # Show all available commands
make install           # Install all dependencies
make setup-db          # Setup database with pgvector
make run-backend       # Start backend services
make run-frontend      # Start mobile apps
make web-dashboard     # Open web dashboard
make embed-docs        # Setup AI support system
make test              # Run backend tests
make clean             # Clean up Docker resources
make quick-start       # Complete setup and start backend
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/magic-link` - Request verification code
- `POST /auth/verify` - Verify code and get JWT
- `GET /auth/me` - Get current user profile

### Rides
- `POST /rides/quote` - Get ride fare estimate
- `POST /rides/request` - Request a ride
- `POST /rides/{id}/accept` - Driver accepts ride
- `PUT /rides/{id}/status` - Update ride status
- `GET /rides` - Get user's ride history

### Drivers
- `POST /drivers/profile` - Create driver profile
- `POST /drivers/online` - Go online
- `POST /drivers/offline` - Go offline
- `PUT /drivers/location` - Update location

### AI Support
- `POST /ai/support` - Ask AI support questions
- `GET /ai/health` - AI system health check

## 🤖 AI Support System

The application includes an intelligent support system powered by LangChain and OpenAI:

- **Document Embeddings**: Markdown files are processed and stored in pgvector
- **Retrieval-Augmented Generation**: AI responses are grounded in documentation
- **Knowledge Base**: FAQ, policies, and campus-specific guidance
- **Source Citations**: Responses include reference to source documents

### Example Queries
- "How do I cancel a ride?"
- "What's the refund policy?"
- "Where are the best pickup spots on campus?"
- "How does Stripe Connect work for drivers?"

## 💳 Payment Flow

1. **Ride Request**: Rider requests ride with pickup/dropoff
2. **Driver Assignment**: System matches nearby online drivers
3. **Payment Authorization**: Stripe PaymentIntent created (not captured)
4. **Ride Completion**: Driver marks ride complete
5. **Payment Capture**: Payment captured and transferred to driver
6. **Tipping**: Optional tip as separate PaymentIntent

### Stripe Connect Features
- **0% Platform Fee**: All payments go directly to drivers
- **Express Onboarding**: Quick driver account setup
- **Automatic Transfers**: Payments transferred immediately
- **Webhook Handling**: Real-time payment status updates

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Magic Link Verification**: Email/phone verification system
- **Stripe Webhooks**: Secure payment event handling
- **Input Validation**: Pydantic schema validation
- **CORS Protection**: Configurable cross-origin policies

## 🧪 Testing

```bash
# Run backend tests
make test

# Test specific components
cd backend
python -m pytest tests/ -v
```

## 🚀 Deployment

### Production Considerations
- Set `ENVIRONMENT=production` in environment variables
- Configure proper CORS origins
- Use production Stripe keys
- Set up monitoring and logging
- Configure SSL/TLS certificates
- Set up database backups

### Docker Deployment
```bash
# Build production images
docker build -t rideshare-backend ./backend

# Run with production environment
docker run -p 8000:8000 --env-file .env rideshare-backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs](docs/) folder
- **Issues**: Report bugs via [GitHub Issues](https://github.com/yourusername/uc-berkeley-rideshare/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/yourusername/uc-berkeley-rideshare/discussions)

## 🗺️ Roadmap

- [ ] **Phase 1**: Core MVP (✅ Complete)
- [ ] **Phase 2**: Advanced features (in progress)
  - [ ] Push notifications
  - [ ] Advanced analytics
  - [ ] Driver rating system
- [ ] **Phase 3**: Scale and optimize
  - [ ] Load balancing
  - [ ] Database optimization
  - [ ] Performance monitoring

## 🙏 Acknowledgments

- **UC Berkeley** for pilot program support
- **Stripe** for payment infrastructure
- **OpenAI** for AI capabilities
- **FastAPI** for modern Python web framework
- **React Native** for cross-platform mobile development

---

**Built with ❤️ for UC Berkeley's rideshare pilot program**

*This is a production-ready MVP that demonstrates modern full-stack development practices with real-time communication, secure payments, and AI-powered support.*