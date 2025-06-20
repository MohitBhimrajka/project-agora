#!/bin/bash

# cleanup.sh - Reverse the setup_environment.sh process
# This script deletes all cloud resources created during setup

set -e

echo "🧹 Project Agora Cleanup Script"
echo "=============================="
echo ""

# Load environment variables if .env exists
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Validate required environment variables
REQUIRED_VARS=("GOOGLE_CLOUD_PROJECT" "RAG_CORPUS_ID" "GOOGLE_CLOUD_STORAGE_BUCKET" "BQ_PROJECT_ID" "BQ_DATASET_ID")

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Environment variable $var is not set"
        echo "Please ensure your .env file contains all required variables"
        exit 1
    fi
done

echo "🗑️  Starting cleanup process..."
echo ""

# Function to handle errors
cleanup_error() {
    echo "⚠️  Warning: $1"
    echo "   Continuing with cleanup..."
}

# 1. Delete RAG Corpus
echo "1️⃣  Deleting RAG Corpus..."
if gcloud ai corpora delete $RAG_CORPUS_ID --region=us-central1 --quiet 2>/dev/null; then
    echo "   ✅ RAG Corpus deleted successfully"
else
    cleanup_error "Failed to delete RAG Corpus (it may not exist or already be deleted)"
fi

# 2. Delete BigQuery dataset and all tables
echo ""
echo "2️⃣  Deleting BigQuery dataset..."
if bq rm -r -f $BQ_PROJECT_ID:$BQ_DATASET_ID 2>/dev/null; then
    echo "   ✅ BigQuery dataset deleted successfully"
else
    cleanup_error "Failed to delete BigQuery dataset (it may not exist or already be deleted)"
fi

# 3. Delete Google Cloud Storage bucket and all contents
echo ""
echo "3️⃣  Deleting GCS bucket and contents..."
if gsutil rm -r gs://$GOOGLE_CLOUD_STORAGE_BUCKET 2>/dev/null; then
    echo "   ✅ GCS bucket deleted successfully"
else
    cleanup_error "Failed to delete GCS bucket (it may not exist or already be deleted)"
fi

# 4. Check for and delete any Cloud Run services (optional)
echo ""
echo "4️⃣  Checking for Cloud Run services..."
CLOUD_RUN_SERVICES=$(gcloud run services list --filter="metadata.name:project-agora" --format="value(metadata.name)" --region=us-central1 2>/dev/null || echo "")

if [ ! -z "$CLOUD_RUN_SERVICES" ]; then
    echo "   Found Cloud Run services to delete:"
    for service in $CLOUD_RUN_SERVICES; do
        echo "   Deleting service: $service"
        if gcloud run services delete $service --region=us-central1 --quiet 2>/dev/null; then
            echo "   ✅ Cloud Run service $service deleted"
        else
            cleanup_error "Failed to delete Cloud Run service $service"
        fi
    done
else
    echo "   ℹ️  No Cloud Run services found to delete"
fi

# 5. Clean up local files (optional)
echo ""
echo "5️⃣  Cleaning up local files..."
if [ -d "logs" ]; then
    rm -rf logs/*
    echo "   ✅ Cleared logs directory"
fi

if [ -f "data/resolved_tickets.csv" ]; then
    echo "   ⚠️  Keeping data/resolved_tickets.csv (contains sample data)"
fi

echo ""
echo "🎉 Cleanup completed!"
echo ""
echo "📝 Summary:"
echo "   - RAG Corpus: Deleted"
echo "   - BigQuery Dataset: Deleted"
echo "   - GCS Bucket: Deleted"
echo "   - Cloud Run Services: Checked and deleted if found"
echo "   - Local logs: Cleared"
echo ""
echo "💡 Note: Your .env file has been preserved."
echo "   Run 'make setup' to recreate the environment."
echo ""

# Optional: Ask if user wants to remove .env file
echo "❓ Do you want to also delete the .env file? (y/N)"
read -r delete_env
if [[ $delete_env =~ ^[Yy]$ ]]; then
    rm -f .env
    echo "   ✅ .env file deleted"
else
    echo "   ℹ️  .env file preserved"
fi

echo ""
echo "🏁 All done! Your cloud resources have been cleaned up."
echo "   To avoid future charges, verify in the Google Cloud Console that all resources are deleted." 