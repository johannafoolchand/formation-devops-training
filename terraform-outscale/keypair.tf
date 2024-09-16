resource "outscale_keypair" "keypair_workshop" {
    keypair_name = "keypair-johanna"
}
output "keypair" {
    value = outscale_keypair.keypair_workshop.private_key
}
