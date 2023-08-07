###create cluster with terraform
provider "google" {
  project     = "disco-rope-393211"
  region      = "us-east1"
  credentials = file("/var/lib/jenkins/gcp/disco-rope-393211-c54c08ccc577.json")
}
resource "google_compute_network" "vpc" {
  name                    = local.network_name
  auto_create_subnetworks = false
}
locals {
  network_name = "disco-rope-393211-vpc"
  subnet_name  = "disco-rope-393211-subnet"
}
resource "google_compute_subnetwork" "subnet" {
  name          = local.subnet_name
  region        = "us-east1"
  network       = google_compute_network.vpc.self_link
  ip_cidr_range = "10.10.0.0/24"
}
resource "google_container_cluster" "primary" {
  name             = "flas-cluster1"
  location         = "us-east1"
  network          = google_compute_network.vpc.id
  subnetwork       = google_compute_subnetwork.subnet.id
  enable_autopilot = true
 }
