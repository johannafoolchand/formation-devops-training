terraform {
  required_providers {
    outscale = {
      source  = "outscale/outscale"
      version = "0.12.0"
    }
  }

  backend "s3" {
    access_key               = var.access_key
    secret_key               = var.secret_key
    region                   = var.region
    bucket                   = "devops-training-johanna"
    key                      = "terraform.tfstate"
    skip_region_validation   = true
    skip_credentials_validation = true
    endpoint = "https://oos.us-east-2.outscale.com"
  }
}

provider "outscale" {
  access_key_id  = var.access_key
  secret_key_id  = var.secret_key
  region         = var.region
}
