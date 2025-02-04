terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"

}
resource "scaleway_registry_namespace" "main" {
  name        = "main-cr"
  description = "Main container registry"
  is_public   = false
}

resource "scaleway_vpc_private_network" "pn" {}

resource "scaleway_k8s_cluster" "cluster" {
  name                        = "tf-cluster"
  version                     = "1.29.1"
  cni                         = "cilium"
  private_network_id          = scaleway_vpc_private_network.pn.id
  delete_additional_resources = false
}

resource "scaleway_k8s_pool" "pool" {
  cluster_id = scaleway_k8s_cluster.cluster.id
  name       = "tf-pool"
  node_type  = "DEV1-M"
  size       = 3
}

resource "scaleway_rdb_instance" "BDD_PROD_instance" {
  name           = "prod-rdb"
  node_type      = "DB-DEV-S"
  engine         = "PostgreSQL-15"
  is_ha_cluster  = true
  disable_backup = true
  user_name      = "prod"
  password       = "production"
}

resource "scaleway_rdb_database" "BDD_PROD" {
  instance_id = scaleway_rdb_instance.BDD_PROD_instance.id
  name        = "bdd_prod"
}

resource "scaleway_rdb_instance" "BDD_DEV_instance" {
  name           = "dev-rdb"
  node_type      = "DB-DEV-S"
  engine         = "PostgreSQL-15"
  is_ha_cluster  = true
  disable_backup = true
  user_name      = "dev"
  password       = "development"
}

resource "scaleway_rdb_database" "BDD_DEV" {
  instance_id = scaleway_rdb_instance.BDD_DEV_instance.id
  name        = "bdd_dev"
}

resource "scaleway_domain_record" "dns_calculatrice" {
  dns_zone = "domain.tld"
  name     = "calculatrice-DECOUZON-polytech-dijon.kiowy.net"
  type     = "A"
  data     = "1.2.3.4"
  ttl      = 3600
}

resource "scaleway_domain_record" "dns_dev_calculatrice" {
  dns_zone = "domain.tld"
  name     = "calculatrice-dev-DECOUZON-polytech-dijon.kiowy.net"
  type     = "A"
  data     = "1.2.3.4"
  ttl      = 3600
}

resource "scaleway_lb_ip" "prod_lb_ip" {
  zone = "fr-par-1"
}

resource "scaleway_lb" "prod_lb" {
  ip_ids = [scaleway_lb_ip.prod_lb_ip.id]
  zone   = scaleway_lb_ip.prod_lb_ip.zone
  type   = "LB-S"
}

resource "scaleway_lb_ip" "dev_lb_ip" {
  zone = "fr-par-1"
}

resource "scaleway_lb" "dev_lb" {
  ip_ids = [scaleway_lb_ip.dev_lb_ip.id]
  zone   = scaleway_lb_ip.dev_lb_ip.zone
  type   = "LB-S"
}
