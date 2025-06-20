.PHONY: help install setup run test deploy-cr deploy-ae clean

help:
	@echo "Project Agora - Makefile Commands:"
	@echo ""
	@echo "  install      : Install dependencies using Poetry."
	@echo "  setup        : Run the full environment setup script."
	@echo "  run          : Start the local ADK web server."
	@echo "  test         : Run the evaluation test suite."
	@echo "  deploy-cr    : Deploy the agent to Cloud Run with UI."
	@echo "  deploy-ae    : Deploy the agent to Vertex AI Agent Engine."
	@echo "  clean        : Run the environment cleanup script."
	@echo ""
	@echo "Usage: make <command>"

install:
	@echo "📦 Installing dependencies with Poetry..."
	poetry install
	@echo "🌐 Installing Playwright browser dependencies..."
	npx playwright install --with-deps

setup:
	@echo "🚀 Setting up Project Agora environment..."
	@./setup_environment.sh

run:
	@echo "🌐 Starting ADK web server..."
	adk web

test:
	@echo "🧪 Running evaluation tests..."
	poetry run pytest eval/

deploy-cr:
	@echo "☁️  Deploying to Cloud Run..."
	@bash deployment/deploy_cloud_run.sh

deploy-ae:
	@echo "🤖 Deploying to Vertex AI Agent Engine..."
	python3 deployment/deploy_agent_engine.py --create

clean:
	@echo "⚠️  WARNING: This will delete cloud resources. Are you sure? (y/N)" && read ans && [ $${ans:-N} = y ] && ./cleanup.sh || echo "Cleanup cancelled." 