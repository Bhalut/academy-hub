# 🏗️ Arquitectura del Proyecto

El **Tracking Service** sigue una arquitectura basada en **eventos**, con microservicios para procesar, almacenar y analizar la actividad del usuario.

## 🖼️ Diagrama de Arquitectura

![Architecture Diagram](images/architecture_diagram.png)

### 📌 Componentes
- **FastAPI**: API para recibir eventos de tracking.
- **MongoDB**: Base de datos para almacenamiento de eventos.
- **Kafka / RabbitMQ**: Middleware para eventos en tiempo real.
- **Celery**: Procesamiento asíncrono de datos.
- **Prometheus & Grafana**: Monitoreo de métricas y logs.
- **Loki**: Centralización de logs.

## 📡 Flujo de Eventos

![Event Flow](images/event_flow.png)

1. FastAPI recibe eventos y los valida con `EventSchema`.
2. Los eventos se almacenan en MongoDB usando `Repository Pattern`.
3. Kafka y RabbitMQ distribuyen eventos en tiempo real.
4. Celery procesa eventos asíncronamente.
5. Machine Learning analiza anomalías en eventos.
6. Prometheus monitorea métricas y Grafana visualiza datos.
