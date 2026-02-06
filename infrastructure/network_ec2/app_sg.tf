# Recurso para crear una Elastic IP en AWS
resource "aws_eip" "elastic_ip" {
  vpc      = var.app_eip_vpc        # Indica si la EIP se asigna a una VPC (true/false). Las EIP en VPC funcionan distinto que en EC2 clásico.
  instance = aws_instance.app_instance.id  # Asocia esta Elastic IP a la instancia EC2 creada anteriormente
                                             # Esto garantiza que la IP pública no cambie aunque la instancia se detenga o reinicie

  # Etiquetas para identificar la Elastic IP en la consola de AWS
  tags = {
    Name = var.app_eip_name
  }
}
