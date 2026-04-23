# Usa una imagen base de Python 3.13-slim para mantener el contenedor ligero
FROM python:3.13-slim

# Actualiza el sistema operativo e instala dependencias necesarias para weasyprint, uWSGI y pdfkit
RUN apt-get update -qq && apt-get upgrade -y -qq \
    && apt-get install -y -qq \
       libpango-1.0-0 \
       libpangocairo-1.0-0 \
       gcc \
       python3-dev \
       build-essential \
       wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Crea un usuario no privilegiado para ejecutar la aplicación
RUN useradd -m -u 1000 appuser

# Crea el directorio para las sesiones de Flask-Session y asigna permisos
RUN mkdir -p /tmp/flask_session && chown appuser:appuser /tmp/flask_session

# Define una variable de entorno para el directorio de la aplicación
ENV APP=/app

# Crea el directorio /app y establece el directorio de trabajo
RUN mkdir $APP
WORKDIR $APP

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Cambia al usuario no privilegiado
USER appuser

# Ejecuta la aplicación con uWSGI
CMD ["uwsgi", "--ini", "app.ini"]