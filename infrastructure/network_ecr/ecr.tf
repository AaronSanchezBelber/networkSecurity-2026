# Recurso para crear un repositorio de contenedores en AWS ECR (Elastic Container Registry)
resource "aws_ecr_repository" "network_ecr_repo" {
  name                 = var.network_ecr_name        # Nombre del repositorio (ej. "mi-app-network")
  image_tag_mutability = var.image_tag_mutability    # Define si las etiquetas de las imágenes son mutables o inmutables
                                                     # "MUTABLE" permite sobrescribir una etiqueta existente
                                                     # "IMMUTABLE" bloquea la sobreescritura de una etiqueta
  force_delete         = var.force_delete_image      # Permite borrar el repositorio incluso si tiene imágenes dentro

  # Configuración de escaneo automático de vulnerabilidades
  image_scanning_configuration {
    scan_on_push = var.scan_on_push  # Si true, cada imagen subida se escanea automáticamente en busca de vulnerabilidades
  }
}
