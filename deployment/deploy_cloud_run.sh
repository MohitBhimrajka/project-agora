#!/bin/bash

# Cloud Run Deployment Script for ADK Copilot
# This script loads environment variables and deploys the agent to Google Cloud Run

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 ADK Copilot Cloud Run Deployment Script${NC}"
echo "================================================"

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}📋 Loading environment variables from .env file...${NC}"
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
else
    echo -e "${YELLOW}⚠️  No .env file found. Using system environment variables...${NC}"
fi

# Required environment variables
REQUIRED_VARS=(
    "GOOGLE_CLOUD_PROJECT"
    "GOOGLE_CLOUD_LOCATION"
)

# Check for required environment variables
missing_vars=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}❌ Error: Missing required environment variables:${NC}"
    printf '%s\n' "${missing_vars[@]}"
    echo ""
    echo "Please set these variables in your .env file or environment:"
    echo "GOOGLE_CLOUD_PROJECT=your-project-id"
    echo "GOOGLE_CLOUD_LOCATION=us-central1"
    exit 1
fi

# Set default values for optional variables
SERVICE_NAME=${SERVICE_NAME:-"adk-copilot"}
APP_NAME=${APP_NAME:-"adk_copilot"}
AGENT_PATH=${AGENT_PATH:-"adk_copilot"}

echo -e "${GREEN}✅ Environment variables loaded:${NC}"
echo "  📍 Project: $GOOGLE_CLOUD_PROJECT"
echo "  🌍 Region: $GOOGLE_CLOUD_LOCATION"
echo "  🚢 Service Name: $SERVICE_NAME"
echo "  📱 App Name: $APP_NAME"
echo "  📂 Agent Path: $AGENT_PATH"
echo ""

# Check if ADK CLI is available
if ! command -v adk &> /dev/null; then
    echo -e "${RED}❌ Error: ADK CLI not found. Please install the Google ADK.${NC}"
    exit 1
fi

echo -e "${BLUE}🔧 Checking if authenticated with Google Cloud...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}⚠️  Not authenticated with Google Cloud. Running authentication...${NC}"
    gcloud auth application-default login
else
    echo -e "${GREEN}✅ Already authenticated with Google Cloud.${NC}"
fi

# Set the active project
echo -e "${BLUE}🔧 Setting active Google Cloud project...${NC}"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required Google Cloud APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

echo ""
echo -e "${BLUE}🚀 Starting Cloud Run deployment...${NC}"
echo "This may take several minutes..."
echo ""

# Build the deployment command
DEPLOY_CMD="adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --service_name=$SERVICE_NAME \
    --app_name=$APP_NAME \
    --with_ui \
    $AGENT_PATH"

echo -e "${YELLOW}📋 Executing deployment command:${NC}"
echo "$DEPLOY_CMD"
echo ""

# Execute the deployment
if eval $DEPLOY_CMD; then
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📝 Deployment Summary:${NC}"
    echo "  Service Name: $SERVICE_NAME"
    echo "  Project: $GOOGLE_CLOUD_PROJECT"
    echo "  Region: $GOOGLE_CLOUD_LOCATION"
    echo ""
    echo -e "${BLUE}🔗 To view your deployed service:${NC}"
    echo "  Console: https://console.cloud.google.com/run/detail/$GOOGLE_CLOUD_LOCATION/$SERVICE_NAME/metrics?project=$GOOGLE_CLOUD_PROJECT"
    echo ""
    echo -e "${BLUE}🔗 To get the service URL:${NC}"
    echo "  gcloud run services describe $SERVICE_NAME --region=$GOOGLE_CLOUD_LOCATION --format='value(status.url)'"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo ""
    echo -e "${YELLOW}💡 Troubleshooting tips:${NC}"
    echo "  1. Check that all environment variables are correctly set"
    echo "  2. Verify you have the necessary permissions in the GCP project"
    echo "  3. Ensure the ADK agent path is correct"
    echo "  4. Check the ADK documentation for any recent changes"
    echo ""
    exit 1
fi 