FROM python:3.10-slim

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt update
RUN apt install -y libmagic1 

# Copy the application
COPY . /app
WORKDIR /app

# Run the application
CMD [ "gunicorn" , "-w", "4", "-b", "0.0.0.0:8080", "src.app:app"]
