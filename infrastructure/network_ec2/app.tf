# Recurso que crea un Security Group en AWS
resource "aws_security_group" "security_group" {
  name = var.app_sg_group_name  # Nombre del Security Group, útil para identificarlo en AWS

  # Regla de entrada (ingress) #1
  ingress {
    from_port   = var.app_ingress_from_port[0]  # Puerto inicial del rango que se permite
    to_port     = var.app_ingress_to_port[0]    # Puerto final del rango
    protocol    = var.app_protocol              # Protocolo (ej. "tcp", "udp", "icmp")
    cidr_blocks = var.app_cidr_block           # Rango de IPs permitido (ej. ["0.0.0.0/0"] para acceso público)
  }

  # Regla de entrada (ingress) #2
  ingress {
    from_port   = var.app_ingress_from_port[1]  # Segundo puerto o rango de puertos permitido
    to_port     = var.app_ingress_to_port[1]
    protocol    = var.app_protocol
    cidr_blocks = var.app_cidr_block
  }

  # Regla de salida (egress)
  egress {
    from_port   = var.app_egress_from_port  # Puerto inicial para tráfico saliente permitido
    to_port     = var.app_egress_to_port    # Puerto final para tráfico saliente
    protocol    = var.app_protocol          # Protocolo de salida
    cidr_blocks = var.app_cidr_block        # Rango de IPs de destino permitido
  }

  # Etiquetas del Security Group
  tags = {
    Name = var.app_sg_group_name
  }
}
