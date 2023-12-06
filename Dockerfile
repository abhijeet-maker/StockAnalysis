# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory within the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install django gunicorn psycopg2
# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangokubernetesproject.wsgi"]