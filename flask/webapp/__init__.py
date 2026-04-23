from flask import Flask
from flask_session import Session
#Para ocupar las claves .env
from dotenv import load_dotenv
import os 

load_dotenv()

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuracion de llave secreta 
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  

# Configuraciones para Flask-Session
app.config["SESSION_TYPE"] = "filesystem"  # Usa el sistema de archivos para almacenar sesiones
app.config["SESSION_PERMANENT"] = False    # Las sesiones no son permanentes
app.config["SESSION_FILE_DIR"] = os.getenv("SESSION_FILE_DIR")  # Directorio para almacenar las sesiones
app.config["SESSION_COOKIE_NAME"] = os.getenv("SESSION_COOKIE_NAME")  # Nombre de la cookie de sesión

# Inicializa la extensión de sesiones
Session(app)

# Importa las rutas
from . import view