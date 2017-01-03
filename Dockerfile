FROM python:3.5

# Create directory
RUN mkdir /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy sources
COPY . /app

VOLUME /app/exports

CMD ["python", "-m", "geohisto"]
