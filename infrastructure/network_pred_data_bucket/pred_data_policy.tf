# Recurso para generar un número entero aleatorio
resource "random_integer" "random" {
  min = 1      # Valor mínimo que puede generar
  max = 50000  # Valor máximo que puede generar
}
# Recurso para crear un bucket S3 en AWS para datos de predicción
resource "aws_s3_bucket" "pred_data_bucket" {
  # El nombre del bucket combina el número aleatorio y el nombre base
  # Esto garantiza que sea único a nivel global, ya que S3 no permite duplicados
  bucket = "${random_integer.random.id}${var.pred_data_bucket_name}"

  # Permite destruir el bucket aunque contenga objetos
  force_destroy = var.force_destroy_bucket
}
