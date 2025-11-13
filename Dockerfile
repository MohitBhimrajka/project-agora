FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser

# Change ownership of /app to myuser
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Set up environment variables - Start
ENV PATH="/home/myuser/.local/bin:$PATH"

# Core Google Cloud settings
ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_CLOUD_PROJECT=supervity-witty
ENV GOOGLE_CLOUD_LOCATION=us-central1

# RAG and Storage settings
ENV GOOGLE_CLOUD_STORAGE_BUCKET=mohit-adk-docs
ENV RAG_CORPUS_NAME=projects/supervity-witty/locations/us-central1/ragCorpora/7991637538768945152

# BigQuery integration
ENV BQ_PROJECT_ID=supervity-witty
ENV BQ_DATASET_ID=cloud-dev

# Optional CRM integration
ENV CRM_API_KEY=your-crm-api-key-here

# Set up environment variables - End

# Install ADK - Start
RUN pip install google-adk==1.2.1
# Install ADK - End

# Copy agent - Start (Fixed: Use --chown to set proper permissions)
COPY --chown=myuser:myuser "agents/project-agora/" "/app/agents/project-agora/"
RUN pip install -r "/app/agents/project-agora/requirements.txt"

# Copy agent - End

EXPOSE 8000

CMD adk web --port=8000 --host=0.0.0.0   "/app/agents"
