# Cómo ejecutar el proyecto

## Comando principal

✅ **Verificada** — Cita literal de [README.md](../README.md) / [README.es.md](../README.es.md):
```bash
docker compose up --build
```

## URLs resultantes

✅ **Verificada** — Frontend en `http://localhost:5173`: mapeo de puerto `"5173:5173"` en [docker-compose.yml](../docker-compose.yml).
✅ **Verificada** — Backend en `http://localhost:8000`: mapeo de puerto `"8000:8000"` en `docker-compose.yml`.
✅ **Verificada** — Documentación interactiva de la API en `http://localhost:8000/docs`: `backend/app/main.py` instancia `FastAPI(title="Financial Metrics API")` sin desactivar `docs_url`/`redoc_url`/`openapi_url` (confirmado por búsqueda en todo `backend/`, sin resultados de esos parámetros), por lo que el Swagger UI por defecto de FastAPI queda expuesto.
✅ **Verificada** — Puerto de debugger remoto `5678` disponible para adjuntar `debugpy`: mapeo `"5678:5678"` en `docker-compose.yml` + `CMD` de `backend/Dockerfile`.

## Configuración opcional

✅ **Verificada** — El proxy de Vite para `/api` funciona sin variables de entorno adicionales en Docker/Codespaces: `frontend/vite.config.ts` apunta directo a `http://backend:8000`.
❓ **Parcialmente verificada** — Existe [frontend/.env.example](../frontend/.env.example) para definir `VITE_API_BASE_URL` si se necesita apuntar a otro backend (según texto del README), pero el contenido del archivo no pudo leerse en este entorno (bloqueado por configuración de acceso a archivos `.env*`), por lo que no puedo confirmar su formato exacto.

## Ejecución sin Docker

❌ **No soportada por evidencia** — No encontré instrucciones ni scripts en el repositorio para correr `backend` o `frontend` fuera de Docker (no hay `Makefile`, `install.sh`, ni sección alternativa en el README). Sería posible inferir comandos (`uvicorn app.main:app --reload`, `npm run dev`) a partir de `requirements.txt`/`package.json`, pero el repositorio no lo documenta explícitamente como flujo soportado.

## Tests

✅ **Verificada** — Backend: `pytest` (dependencia en `requirements.txt`), suite en [backend/tests/test_routes.py](../backend/tests/test_routes.py) y [backend/tests/conftest.py](../backend/tests/conftest.py). No se encontró un script/documentación que indique el comando exacto de invocación (p. ej. no hay `pytest.ini` ni sección en README); el comando estándar `pytest` se infiere de la presencia de la dependencia, no está documentado literalmente.
✅ **Verificada** — Frontend: scripts declarados en [frontend/package.json](../frontend/package.json): `"test": "vitest run"`, `"test:watch": "vitest"`, `"test:coverage": "vitest run --coverage"`.
