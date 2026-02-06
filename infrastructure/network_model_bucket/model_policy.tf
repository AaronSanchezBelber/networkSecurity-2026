# Recurso para generar un número entero aleatorio
resource "random_integer" "random" {
  min = 1      # Valor mínimo que puede generar
  max = 50000  # Valor máximo que puede generar
}
