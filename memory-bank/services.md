# Servicios existentes

## `frontend` (docker-compose.yml)

✅ **Verificada** — Definición completa en [docker-compose.yml](../docker-compose.yml):
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "5173:5173"
  depends_on:
    - backend
```
✅ **Verificada** — Build con [frontend/Dockerfile](../frontend/Dockerfile): imagen `node:24-alpine`, ejecuta `npm install` y luego `npm run dev -- --host 0.0.0.0 --port 5173`.

## `backend` (docker-compose.yml)

✅ **Verificada** — Definición completa en [docker-compose.yml](../docker-compose.yml):
```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
    - "5678:5678"
```
✅ **Verificada** — Build con [backend/Dockerfile](../backend/Dockerfile): imagen `python:3.13-slim`, instala `requirements.txt`, ejecuta `uvicorn` bajo `debugpy` (puerto 8000 para la API, 5678 para el debugger remoto).

## Endpoints del backend

✅ **Verificada** — Todos definidos en [backend/app/routes.py](../backend/app/routes.py):

| Endpoint | Método | Evidencia |
|---|---|---|
| `/health` | GET | línea `@router.get("/health")` |
| `/api/metrics` | GET | `@router.get("/api/metrics", response_model=list[FinancialMovement])` |
| `/api/metrics/facets` | GET | `@router.get("/api/metrics/facets", response_model=MetricsFacets)` |
| `/api/metrics/summary` | GET | `@router.get("/api/metrics/summary", response_model=list[MetricsSummaryItem])` |
| `/api/metrics/categories/top` | GET | `@router.get("/api/metrics/categories/top", response_model=list[TopCategoryItem])` |
| `/api/metrics/comparison` | GET | `@router.get("/api/metrics/comparison", response_model=MetricsComparison)` |
| `/api/metrics/alerts` | GET | `@router.get("/api/metrics/alerts", response_model=list[MetricsAlert])` |
| `/api/metrics/b2b` | GET | `@router.get("/api/metrics/b2b", response_model=list[FinancialMovement])` |
| `/api/metrics/b2c` | GET | `@router.get("/api/metrics/b2c", response_model=list[FinancialMovement])` |

❌ **No soportada por evidencia** — No hay ningún tercer servicio (base de datos, cache, cola de mensajes). Solo `frontend` y `backend` existen en `docker-compose.yml`.
