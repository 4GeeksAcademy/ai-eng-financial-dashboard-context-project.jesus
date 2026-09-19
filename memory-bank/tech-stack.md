# Stack tecnológico

## Tech Stack

- **Lenguajes:** Python 3.13 (backend, `FROM python:3.13-slim` en `backend/Dockerfile`) y TypeScript `~6.0.2` (frontend, `frontend/package.json`).
- **Frameworks:** FastAPI + Uvicorn (backend, `backend/requirements.txt` + `backend/Dockerfile`); React 19 + Vite 8 (frontend, `frontend/package.json`).
- **Infraestructura:** Docker Compose con dos servicios (`frontend`, `backend`) definidos en [docker-compose.yml](../docker-compose.yml). Sin base de datos, sin CI/CD (no existe `.github/workflows/`).
- **Dependencias clave:** Pydantic (validación/schemas), Tailwind CSS 4 + shadcn/ui (estilos y componentes UI), Recharts (gráficos), Vitest + pytest (testing).

Detalle completo con evidencia por archivo a continuación.

## Backend

✅ **Verificada** — [backend/requirements.txt](../backend/requirements.txt):
```
fastapi
uvicorn[standard]
debugpy
pytest
pytest-cov
httpx
```
✅ **Verificada** — Python 3.13: [backend/Dockerfile](../backend/Dockerfile) línea `FROM python:3.13-slim`.
✅ **Verificada** — Framework web: FastAPI, servido con Uvicorn (`app.main:app`), ver `CMD` en `backend/Dockerfile`.
✅ **Verificada** — Validación/serialización con Pydantic `BaseModel`: ver clases en [backend/app/routes.py](../backend/app/routes.py) (`FinancialMovement`, `MetricsFacets`, etc.).
✅ **Verificada** — Testing con `pytest` + `TestClient` de FastAPI (que usa `httpx` internamente): ver [backend/tests/test_routes.py](../backend/tests/test_routes.py) y [backend/tests/conftest.py](../backend/tests/conftest.py). Ejecución real confirmada en esta sesión: `python3 -m pytest -q` → 16 tests pasan.
✅ **Verificada** — Debugging remoto con `debugpy`, puerto 5678: `backend/Dockerfile` `CMD`.

## Frontend

✅ **Verificada** — [frontend/package.json](../frontend/package.json) dependencias principales:
- `react` `^19.2.4`, `react-dom` `^19.2.4`
- `recharts` `^3.8.1` (gráficos)
- `lucide-react` `^1.8.0` (iconos)
- `class-variance-authority`, `clsx`, `tailwind-merge` (utilidades de estilo, patrón shadcn/ui)

✅ **Verificada** — Build tool: Vite `^8.0.4` (`vite.config.ts`, script `"dev": "vite"`).
✅ **Verificada** — TypeScript `~6.0.2`, con `tsc -b` como parte del build (`"build": "tsc -b && vite build"`).
✅ **Verificada** — Tailwind CSS `^4.2.2` vía plugin `@tailwindcss/vite`, ver [frontend/vite.config.ts](../frontend/vite.config.ts) `plugins: [react(), tailwindcss()]`.
✅ **Verificada** — Componentes UI basados en shadcn (`style: "new-york"`, `baseColor: "zinc"`): [frontend/components.json](../frontend/components.json).
✅ **Verificada** — Testing con Vitest `^4.1.4` + `@vitest/coverage-v8`: scripts `"test"`, `"test:watch"`, `"test:coverage"` en `package.json`; test real en [frontend/src/lib/financial-utils.test.ts](../frontend/src/lib/financial-utils.test.ts).
✅ **Verificada** — Linting con ESLint `^9.39.4` (flat config) + `typescript-eslint`, `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`: [frontend/eslint.config.js](../frontend/eslint.config.js).
✅ **Verificada** — Node.js 24 en el contenedor: `frontend/Dockerfile` línea `FROM node:24-alpine`.

## Infraestructura

✅ **Verificada** — Orquestación con Docker Compose (dos servicios: `frontend`, `backend`): [docker-compose.yml](../docker-compose.yml).
❌ **No soportada por evidencia** — No hay CI/CD configurado: no existe directorio `.github/workflows/` en el repositorio (búsqueda de archivos sin resultados).
