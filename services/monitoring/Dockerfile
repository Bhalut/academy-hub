FROM grafana/grafana:latest

COPY grafana/grafana.ini /etc/grafana/grafana.ini
COPY grafana/datasources.yaml /etc/grafana/provisioning/datasources/datasources.yaml
COPY grafana/dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
COPY grafana/dashboards /var/lib/grafana/dashboards
