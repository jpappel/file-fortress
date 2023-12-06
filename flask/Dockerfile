FROM python:3.10-slim

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y libmagic1

# Copy the application
COPY . /app
WORKDIR /app

# Generate a secret key for the app
# RUN python3 -c 'import secrets; print(secres.token_hex())' >> /app/.env

# Run the application
CMD [ "gunicorn" , "-w", "4", "-b", "0.0.0.0:8080", "src:create_app()"]
