resource "outscale_vm" "vm_workshop" {
  image_id         = "ami-1111f1b5"
  vm_type          = "tinav7.c2r2p3"
  keypair_name     = outscale_keypair.keypair_workshop.keypair_name
  security_group_ids = [
    outscale_security_group.security_group_workshop.security_group_id,
  ]
  tags {
    key   = "Name"
    value = "vm-johanna"
  }
}
