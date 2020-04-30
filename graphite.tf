# Create Graphite container
resource "docker_container" "graphite" {
  image = "${docker_image.graphite.latest}"
  name  = "graphite"
  hostname  = "graphite"
  network_mode = "${docker_network.private_network.name}"
  ports {
    internal = 80
    external = 9195
  }
  ports {
    internal = 9196
    external = 2003
  }
  ports {
    internal = 9197
    external = 2004
  }
  ports {
    internal = 2023
    external = 2023
  }
  ports {
    internal = 2024
    external = 2024
  }
  ports {
    internal = 8125
    external = 8125
    protocol = "udp"
  }
  ports {
    internal = 8126
    external = 8126
  }
  restart = "always"
}

resource "docker_image" "graphite" {
  name = "graphiteapp/graphite-statsd"
}
