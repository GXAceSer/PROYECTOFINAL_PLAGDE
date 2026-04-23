FROM nginx:latest  
#|------Indica que estás usando la imagen oficial de NGINX en su version mas reciente como base
#NGINX will listen on this port 
#EXPOSE 80
#Remove the default config file that 
# /etc/nginx/nginx.conf includes
RUN rm /etc/nginx/conf.d/default.conf
#|---------Elimina el archivo de ocnfiguracion por defecto que viene con NGINX
# We copy the requirements file in order to install 
# Python dependencies 
COPY nginx.conf /etc/nginx/conf.d/
#|----------Esta linea copia tu archivo personalizado nginx.conf que está en tu carpeta nginx/
#           dentro de conf.d