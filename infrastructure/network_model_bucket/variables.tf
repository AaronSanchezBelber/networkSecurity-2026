# Región de AWS donde se crearán los recursos
variable "aws_region" {
  type    = string       # Tipo de dato: texto
  default = "us-east-1" # Valor por defecto: región US East (N. Virginia)
}

# Nombre del bucket de modelos (posiblemente para almacenar archivos o modelos de ML)
variable "model_bucket_name" {
  type    = string        # Tipo de dato: texto
  default = "network-model" # Nombre por defecto del bucket S3
}

# ID de la cuenta de AWS donde se crearán los recursos
variable "aws_account_id" {
  type    = string           # Tipo de dato: texto
  default = "566373416292"   # ID de cuenta por defecto
}

# Permite destruir el bucket incluso si contiene objetos
variable "force_destroy_bucket" {
  type    = bool    # Tipo de dato: booleano (true/false)
  default = true    # Por defecto, se permite borrar el bucket con todo su contenido
}
