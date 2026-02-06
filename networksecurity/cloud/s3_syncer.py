import os  # Módulo estándar de Python para interactuar con el sistema operativo


class S3Sync:
    """
    Clase encargada de sincronizar carpetas locales con Amazon S3
    usando la AWS CLI.
    """

    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """
        Sincroniza una carpeta LOCAL hacia un bucket de S3.

        folder:
            Ruta local de la carpeta que quieres subir
            Ej: "saved_models/"

        aws_bucket_url:
            URL del bucket de S3
            Ej: "s3://my-ml-models-bucket/"
        """

        # Construimos el comando de consola usando aws s3 sync
        # aws s3 sync copia SOLO los archivos nuevos o modificados
        command = f"aws s3 sync {folder} {aws_bucket_url}"

        # Ejecuta el comando en el sistema operativo
        # Es equivalente a escribir el comando en la terminal
        os.system(command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        """
        Sincroniza una carpeta DESDE S3 hacia el sistema LOCAL.

        folder:
            Ruta local donde se descargarán los archivos
            Ej: "saved_models/"

        aws_bucket_url:
            URL del bucket de S3
            Ej: "s3://my-ml-models-bucket/"
        """

        # Construimos el comando inverso:
        # Copia los archivos del bucket de S3 a la carpeta local
        command = f"aws s3 sync {aws_bucket_url} {folder}"

        # Ejecuta el comando en el sistema operativo
        os.system(command)
