.PHONY: help install run-backend run-frontend run-all stop clean embed-docs test web-dashboard

# Default target
help:
	@echo "UC Berkeley Rideshare MVP - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install          Install all dependencies"
	@echo "  setup-db         Setup database with pgvector extension"
	@echo "  dev-setup        Complete development environment setup"
	@echo ""
	@echo "Running the Application:"
	@echo "  run-backend      Start the FastAPI backend with Docker"
	@echo "  run-frontend     Start the React Native apps"
	@echo "  run-all          Start both backend and frontend"
	@echo "  web-dashboard    Open web dashboard in browser"
	@echo "  stop             Stop all running services"
	@echo ""
	@echo "AI/RAG Pipeline:"
	@echo "  embed-docs       Embed documentation for AI support system"
	@echo ""
	@echo "Development:"
	@echo "  test             Run backend tests"
	@echo "  clean            Clean up Docker containers and volumes"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	@cd backend && pip install -r requirements.txt
	@cd apps/rider && npm install
	@cd apps/driver && npm install
	@echo "✓ Dependencies installed"

# Setup database with pgvector
setup-db:
	@echo "Setting up database..."
	@docker-compose up -d postgres
	@sleep 10
	@echo "Creating pgvector extension..."
	@docker-compose exec postgres psql -U user -d rideshare -c "CREATE EXTENSION IF NOT EXISTS vector;"
	@echo "✓ Database setup completed"

# Start backend services
run-backend:
	@echo "Starting backend services..."
	@docker-compose up -d postgres redis
	@echo "Waiting for database to be ready..."
	@sleep 10
	@echo "Starting FastAPI backend..."
	@cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend apps
run-frontend:
	@echo "Starting React Native apps..."
	@echo "Rider app: cd apps/rider && npm start"
	@echo "Driver app: cd apps/driver && npm start"
	@echo "Use separate terminals for each app"

# Start everything
run-all:
	@echo "Starting full rideshare application..."
	@make run-backend &
	@sleep 5
	@make run-frontend

# Open web dashboard
web-dashboard:
	@echo "Opening web dashboard..."
	@echo "Dashboard available at: http://localhost:8000/dashboard"
	@if command -v open >/dev/null 2>&1; then \
		open http://localhost:8000/dashboard; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8000/dashboard; \
	else \
		echo "Please open http://localhost:8000/dashboard in your browser"; \
	fi

# Stop all services
stop:
	@echo "Stopping all services..."
	@docker-compose down
	@pkill -f "uvicorn app.main:app" || true
	@echo "✓ All services stopped"

# Clean up Docker resources
clean:
	@echo "Cleaning up Docker resources..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "✓ Cleanup completed"

# Embed documentation for AI support
embed-docs:
	@echo "Embedding documentation for AI support system..."
	@cd backend && python app/ai/embed_docs.py

# Run tests
test:
	@echo "Running backend tests..."
	@cd backend && python -m pytest tests/ -v

# Development setup
dev-setup: install setup-db
	@echo "Development environment setup completed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Copy env.example to .env and fill in your API keys:"
	@echo "   cp env.example .env"
	@echo "   # Edit .env with your Stripe and OpenAI keys"
	@echo ""
	@echo "2. Run 'make embed-docs' to set up AI support"
	@echo "3. Run 'make run-backend' to start the backend"
	@echo "4. Run 'make web-dashboard' to view the web interface"
	@echo "5. Run 'make run-frontend' to start the mobile apps"
	@echo ""
	@echo "Web Dashboard: http://localhost:8000/dashboard"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Health Check: http://localhost:8000/health"

# Quick start - setup everything and start backend
quick-start: dev-setup embed-docs
	@echo "Quick start completed! Starting backend..."
	@make run-backend
