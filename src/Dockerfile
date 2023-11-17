# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /src

# Copy the requirements file into the container at /src
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /src
COPY . /src

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
