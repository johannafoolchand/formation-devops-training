# Définition du groupe de sécurité
resource "outscale_security_group" "security_group_workshop" {
  security_group_name = "workshop_sg"
  description         = "Security group for workshop"
  
  # Tags optionnels pour le groupe de sécurité
}

# Règle de sécurité pour autoriser le SSH
resource "outscale_security_group_rule" "allow_ssh" {
  flow              = "Inbound"
  security_group_id = outscale_security_group.security_group_workshop.id
  ip_protocol       = "tcp"
  from_port_range   = 22
  to_port_range     = 22
  ip_range          = "0.0.0.0/0"
  
  # Tags optionnels pour la règle de sécurité SSH
}

# Règle de sécurité pour autoriser le HTTP
resource "outscale_security_group_rule" "allow_http" {
  flow              = "Inbound"
  security_group_id = outscale_security_group.security_group_workshop.id
  ip_protocol       = "tcp"
  from_port_range   = 80
  to_port_range     = 80
  ip_range          = "0.0.0.0/0"
  
  # Tags optionnels pour la règle de sécurité HTTP
}

# Règle de sécurité pour autoriser le port 5000 (Flask)
resource "outscale_security_group_rule" "allow_flask" {
  flow              = "Inbound"
  security_group_id = outscale_security_group.security_group_workshop.id
  ip_protocol       = "tcp"
  from_port_range   = 5000
  to_port_range     = 5000
  ip_range          = "0.0.0.0/0"
  
  # Tags optionnels pour la règle de sécurité Flask
}
# Règle de sécurité pour autoriser le HTTPS
resource "outscale_security_group_rule" "allow_https" {
  flow              = "Inbound"
  security_group_id = outscale_security_group.security_group_workshop.id
  ip_protocol       = "tcp"
  from_port_range   = 443
  to_port_range     = 443
  ip_range          = "0.0.0.0/0"
  
  # Tags optionnels pour la règle de sécurité HTTPS
}
