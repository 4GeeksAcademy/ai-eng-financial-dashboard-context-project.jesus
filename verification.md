# Verification Log

Generado siguiendo únicamente evidencia de: `README.md`, `README.es.md`, `docker-compose.yml`, `frontend/package.json`, `backend/requirements.txt`, `backend/Dockerfile`, `frontend/Dockerfile`, `frontend/vite.config.ts`, `backend/app/main.py`, `backend/app/routes.py`.

## Claims Verified

**Afirmación:** El proyecto tiene dos servicios: `frontend` y `backend`, orquestados por Docker Compose.
**Estado:** ✅ Verificada
**Evidencia:** [docker-compose.yml](../docker-compose.yml) declara exactamente dos entradas bajo `services:` — `frontend` (build context `./frontend`) y `backend` (build context `./backend`).

**Afirmación:** El backend expone su API en el puerto 8000 y un debugger remoto en el puerto 5678.
**Estado:** ✅ Verificada
**Evidencia:** `docker-compose.yml` → `backend.ports: ["8000:8000", "5678:5678"]`; confirmado en [backend/Dockerfile](../backend/Dockerfile) → `EXPOSE 8000 5678` y `CMD [... "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", ..., "--port", "8000", ...]`.

**Afirmación:** El frontend corre en el puerto 5173 mediante Vite.
**Estado:** ✅ Verificada
**Evidencia:** `docker-compose.yml` → `frontend.ports: ["5173:5173"]`; [frontend/Dockerfile](../frontend/Dockerfile) → `EXPOSE 5173`, `CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]`.

**Afirmación:** El entry point del backend es `app.main:app`.
**Estado:** ✅ Verificada
**Evidencia:** `backend/Dockerfile` `CMD` referencia literalmente `uvicorn app.main:app`; [backend/app/main.py](../backend/app/main.py) define `app = FastAPI(title="Financial Metrics API")` e incluye `app.include_router(router)` desde `app.routes`.

**Afirmación:** El entry point del frontend es `src/main.tsx`.
**Estado:** ✅ Verificada
**Evidencia:** [frontend/index.html](../frontend/index.html) — patrón estándar de Vite (`<script type="module" src="/src/main.tsx">`); confirmado por existencia de `frontend/src/main.tsx` en el árbol de archivos del workspace.

**Afirmación:** El frontend se comunica con el backend a través de un proxy `/api` configurado en Vite, no mediante una URL fija en el código de los componentes.
**Estado:** ✅ Verificada
**Evidencia:** [frontend/vite.config.ts](../frontend/vite.config.ts) → `server.proxy["/api"].target = "http://backend:8000"`.

**Afirmación:** El comando oficial para levantar todo el proyecto es `docker compose up --build`.
**Estado:** ✅ Verificada
**Evidencia:** Cita literal idéntica en [README.md](../README.md) y [README.es.md](../README.es.md), sección "How to run locally"/"Cómo ejecutar en local".

**Afirmación:** El backend no tiene manejo de errores (`HTTPException`/`try-except`) en ninguna ruta, salvo el que se añadió en esta sesión.
**Estado:** ✅ Verificada (con corrección aplicada en Fase 4)
**Evidencia:** Búsqueda (`grep`) de `HTTPException|try:|except |raise` en `backend/` antes del cambio de Fase 4 no arrojó resultados de manejo de errores real. Tras la Fase 4, [backend/app/routes.py](../backend/app/routes.py) función `build_metrics_facets` ahora contiene el único `raise HTTPException(...)` del archivo.

**Afirmación:** No existe pipeline de CI/CD.
**Estado:** ✅ Verificada
**Evidencia:** Búsqueda de archivos (`file_search`) con patrón `.github/workflows/*` no devolvió resultados en el repositorio.

**Afirmación:** El frontend usa TypeScript, Tailwind CSS y componentes estilo shadcn/ui.
**Estado:** ✅ Verificada
**Evidencia:** [frontend/package.json](../frontend/package.json) — `"typescript": "~6.0.2"`, `"tailwindcss": "^4.2.2"`, `"@tailwindcss/vite": "^4.2.2"`; [frontend/components.json](../frontend/components.json) — `"style": "new-york"`, `"baseColor": "zinc"`.

**Afirmación:** El backend genera datos financieros simulados en memoria (no hay base de datos).
**Estado:** ✅ Verificada
**Evidencia:** `backend/app/routes.py` función `generate_mock_movements(seed=42)` usa `random.uniform`/`random.choice`; ningún archivo en `backend/requirements.txt` incluye un driver de base de datos (`psycopg2`, `sqlalchemy`, `pymongo`, etc. — ausentes).

## Incorrect Claims Found

**Afirmación revisada:** En un resumen previo de esta conversación se afirmó que `/docs` estaba "parcialmente verificado".
**Estado:** ❌ Incorrecta (corregida en su momento)
**Evidencia de la corrección:** Se confirmó mediante lectura completa de `backend/app/main.py` y búsqueda de `docs_url|redoc_url|openapi_url` en todo `backend/` (sin resultados) que Swagger UI en `/docs` está activo por defecto de FastAPI. La reclasificación a ✅ ya se documentó en el turno de auditoría previo de esta misma conversación.

No se encontraron otras afirmaciones incorrectas en el material verificado hasta ahora. No se afirmó la existencia de bases de datos, colas de mensajes, autenticación, ni frameworks adicionales — por lo tanto no hay correcciones pendientes en esas áreas.

## Corrections Made

1. **Clasificación de `/docs`:** de ❓ a ✅, respaldado por inspección directa de `backend/app/main.py` (sin turno adicional necesario en esta fase, ya corregido previamente).
2. **Manejo de errores en `build_metrics_facets`:** se corrigió la ausencia de manejo de errores (riesgo documentado en `.agents/rules/api-design.md` y `memory-bank/risks.md`) agregando `raise HTTPException(status_code=404, ...)` cuando la lista de movimientos está vacía. Ver [backend/app/routes.py](../backend/app/routes.py) y test añadido en [backend/tests/test_routes.py](../backend/tests/test_routes.py) (`test_build_metrics_facets_raises_404_for_empty_movements`). Verificado con `pytest -q`: 15 tests pasaban antes del cambio, 16 pasan después (incluyendo el nuevo).
