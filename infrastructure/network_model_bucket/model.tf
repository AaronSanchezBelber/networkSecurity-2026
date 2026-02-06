# Recurso para generar un número entero aleatorio
resource "random_integer" "random" {
  min = 1      # Valor mínimo que puede generar
  max = 50000  # Valor máximo que puede generar
}

# Recurso para crear un bucket S3 en AWS
resource "aws_s3_bucket" "model_bucket" {
  # El nombre del bucket combina el número aleatorio y el nombre base de la variable
  # Esto garantiza que el nombre sea único (S3 requiere nombres globalmente únicos)
  bucket        = "${random_integer.random.id}${var.model_bucket_name}" 
  
  # Permite destruir el bucket aunque tenga objetos dentro
  force_destroy = var.force_destroy_bucket
}
