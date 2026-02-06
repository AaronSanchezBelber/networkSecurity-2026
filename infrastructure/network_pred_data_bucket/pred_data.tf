# Recurso que asigna una política a un bucket S3
resource "aws_s3_bucket_policy" "allow_full_access" {
  bucket = aws_s3_bucket.pred_data_bucket.id  # Aplica la política al bucket de datos de predicción
  policy = data.aws_iam_policy_document.allow_full_access.json  # Política definida en el data source
}

# Data source que genera un documento de política IAM para S3
data "aws_iam_policy_document" "allow_full_access" {
  statement {
    principals {
      type        = "AWS"                # Tipo de principal: cuenta o entidad de AWS
      identifiers = [var.aws_account_id] # Identificador del principal (ID de cuenta de AWS)
    }

    actions = ["s3:*"]  # Permite todas las acciones de S3 (lectura, escritura, borrado, etc.)

    resources = [
      aws_s3_bucket.pred_data_bucket.arn,      # Aplica la política al bucket
      "${aws_s3_bucket.pred_data_bucket.arn}/*", # Aplica la política a todos los objetos dentro del bucket
    ]
  }
}
