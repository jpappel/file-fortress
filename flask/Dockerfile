FROM python:3.10

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt-get install libmagic1

# Copy the application
COPY . /app
WORKDIR /app

# Run the application
CMD [ "flask","--app", "src/app", "run", "--host=0.0.0.0", "--port=8080"]
