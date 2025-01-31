# 📖 API Reference - Tracking Service

## 🚀 **Endpoints**

### 📌 `POST /events/`
- **Descripción**: Recibe y almacena eventos de usuario.
- **Request Body**:
```json
{
  "event_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user123",
  "event_type": "click",
  "timestamp": "2025-01-31T12:00:00Z",
  "metadata": { "element": "button", "page": "home" }
}
```
- **Response**:
```json
{ "message": "Event processed successfully" }
```

### 📌 `GET /metrics/`
- **Descripción**: Devuelve métricas de monitoreo.

### 📌 `GET /health/`
- **Descripción**: Endpoint de health-check.
