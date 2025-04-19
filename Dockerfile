FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Copiar los datos estáticos a las ubicaciones correctas
RUN mkdir -p /app/static/images
RUN mkdir -p /app/static/fonts
RUN mkdir -p /app/data/Funciones
RUN mkdir -p /app/data/Perfiles

# Copiar los archivos de datos
COPY static/images/* /app/static/images/
COPY static/fonts/* /app/static/fonts/
COPY data/indicators.json /app/data/
COPY data/advice.json /app/data/
COPY data/Funciones/* /app/data/Funciones/
COPY data/Perfiles/* /app/data/Perfiles/

# Recoger archivos estáticos
RUN python manage.py collectstatic --noinput

# Puerto para gunicorn
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "aneiap_ats.wsgi:application"]
