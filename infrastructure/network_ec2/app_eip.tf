# Configuración del proveedor de AWS
provider "aws" {
  region = var.aws_region  # Define la región de AWS donde se crearán los recursos (ej. us-east-1)
}

# Definición de una instancia EC2
resource "aws_instance" "app_instance" {
  ami                    = var.app_ami               # ID de la AMI (Amazon Machine Image) que usará la instancia
  instance_type          = var.app_instance_type     # Tipo de instancia (ej. t2.micro, t3.medium)
  key_name               = var.app_key_pair_name     # Nombre del par de claves para SSH
  vpc_security_group_ids = [aws_security_group.security_group.id] # Asocia la instancia a un grupo de seguridad específico

  # Etiquetas de la instancia (útil para identificarla en la consola de AWS)
  tags = {
    Name = var.app_tag_name
  }

  # Configuración del disco raíz de la instancia
  root_block_device {
    volume_size = var.app_volume_size       # Tamaño del disco en GB
    volume_type = var.app_volume_type       # Tipo de volumen (ej. gp2, gp3, io1)
    encrypted   = var.app_volume_encryption # Si el volumen estará cifrado (true/false)
  }

  # Configuración de conexión para provisioners remotos (ej. Terraform puede ejecutar scripts en la instancia)
  connection {
    type    = var.app_connection_type # Tipo de conexión (ej. "ssh")
    host    = self.public_ip          # Dirección IP pública de la instancia para la conexión
    user    = var.app_user            # Usuario con el que se conectará (ej. ec2-user, ubuntu)
    timeout = var.app_timeout         # Tiempo máximo de espera para la conexión
  }
}
