variable "clients" {
  type = number
  description = "Number of clients"
}

variable "loop" {
  type = number
  description = "Number of loops"
}

# Create test server container
resource "docker_container" "test_server" {
  image = "${docker_image.test_server.latest}"
  name  = "test_server"
  hostname = "test_server"
  network_mode = "${docker_network.private_network.name}"
  command = ["/root/start.sh"]
  ports {
    internal = 20001
    external = 20001
    protocol = "udp"
  }
}

# Create test client container
resource "docker_container" "test_client" {
  image = "${docker_image.test_server.latest}"
  name  = "test_client"
  hostname = "test_client"
  network_mode = "${docker_network.private_network.name}"
  command = ["/usr/bin/python", "/root/client.py", "--clients=${var.clients}", "--loop=${var.loop}"]
}

resource "docker_image" "test_server" {
  name = "jcua/ubuntu:18.04"
}
