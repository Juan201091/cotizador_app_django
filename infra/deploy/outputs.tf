# Sin dominio todavía: se expone la dirección del ALB.
# TODO: cuando exista dns.tf, usar aws_route53_record.app.fqdn
output "api_endpoint" {
  value = aws_lb.api.dns_name
}
