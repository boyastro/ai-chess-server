# Dockerfile for Flask + TensorFlow chess server
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model
COPY server.py ./
COPY model_move.h5 ./

EXPOSE 5001

# Run with gunicorn for production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5001", "server:app"]
