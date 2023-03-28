FROM python:3.11-slim-buster

# Create and set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the application
CMD ["uvicorn", "financial.main:app", "--host", "0.0.0.0", "--port", "8000"]
