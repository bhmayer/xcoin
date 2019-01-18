# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN apt-get update && apt-get install -y python3-twisted

RUN pip install PyNacl Twisted

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "xcoin.py"]

