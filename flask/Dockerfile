# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the Flask port
EXPOSE 5000            

# Run Flask app

CMD ["python", "app.py"]
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
