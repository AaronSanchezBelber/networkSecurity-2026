# Nombre del repositorio de ECR
variable "network_ecr_name" {
  default = "network"  # Valor por defecto si no se provee otro
  type    = string     # Tipo de dato esperado: cadena de texto
}

# Controla si las etiquetas de las imágenes son mutables o inmutables
variable "image_tag_mutability" {
  default = "MUTABLE"  # Por defecto las etiquetas pueden sobrescribirse
  type    = string      # Tipo de dato: texto
}

# Configuración de escaneo automático de imágenes al subirlas
variable "scan_on_push" {
  default = true   # Por defecto, cada imagen subida se escanea automáticamente
  type    = bool   # Tipo de dato: booleano (true/false)
}

# Permite eliminar el repositorio aunque tenga imágenes
variable "force_delete_image" {
  default = true   # Por defecto, Terraform podrá borrar el repositorio con imágenes
  type    = bool   # Tipo de dato: booleano
}
