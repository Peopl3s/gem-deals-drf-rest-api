# Pull official base Python Docker image
FROM python:3.11.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt update && apt upgrade -y
RUN apt install netcat-traditional

# Copy the Django project
COPY . /code/

RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
