# Imagen base oficial de Python 3.10 en versión slim (ligera)
FROM python:3.10-slim-buster

# Cambiamos al usuario root para poder instalar paquetes
USER root

# Creamos el directorio principal de la aplicación dentro del contenedor
RUN mkdir /app

# Copiamos todo el contenido del proyecto local al contenedor
COPY . /app/

# Definimos /app como el directorio de trabajo por defecto
WORKDIR /app/

# Instalamos todas las dependencias Python necesarias para el proyecto
# (Airflow, ML, AWS SDK, etc.)
RUN pip3 install -r requirements.txt

# Región por defecto de AWS (necesaria para S3 y otros servicios)
ENV AWS_DEFAULT_REGION="eu-west-3"

# Nombre del bucket donde se guardan modelos y artefactos
ENV BUCKET_NAME="my-networksecurity"

# Bucket para datos de predicción / entrada
ENV PREDICTION_BUCKET_NAME="my-network-datasource"

# Directorio HOME de Airflow dentro del contenedor
ENV AIRFLOW_HOME="/app/airflow"

# Aumenta el tiempo máximo que Airflow tiene para importar DAGs
# Útil cuando los DAGs son grandes o complejos
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000

# Permite serializar objetos complejos en XCom (no recomendado en entornos inseguros)
# pero muy usado en pipelines ML
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True

# Inicializa la base de datos de Airflow (metadatos)
RUN airflow db init

# Crea un usuario administrador para acceder a la UI de Airflow
RUN airflow users create \
    -e dataaaronsanchezbelber@gmail.com \
    -f aaron \
    -l sanchez \
    -p admin \
    -r Admin \
    -u admin

# Damos permisos de ejecución al script que levanta Airflow
RUN chmod 777 start.sh

# Actualizamos el índice de paquetes del sistema operativo
RUN apt update -y

# Define el intérprete por defecto del contenedor
ENTRYPOINT [ "/bin/sh" ]

# Comando que se ejecuta automáticamente al arrancar el contenedor
# Inicia el scheduler y el webserver de Airflow
CMD ["start.sh"]
