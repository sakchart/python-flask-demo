# Stage 1: Build the environment for Python app
FROM python:3.9-slim AS build

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies (such as pip and build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the app source code into the container
COPY . .

# Stage 2: Setup the final container image
FROM python:3.9-slim

# Set the working directory for the app
WORKDIR /app

# Install runtime dependencies (e.g., to run the app)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the installed Python dependencies from the build stage
COPY --from=build /app /app

# Expose the application port (Flask default is 5000)
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the application when the container starts
CMD ["flask", "run", "--host", "0.0.0.0"]
