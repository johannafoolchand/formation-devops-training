variable "access_key" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "region" {
  type    = string
  default = "us-east-2"
}

variable "keypair_name" {
  type    = string
  default = "keypair-johanna"
}
