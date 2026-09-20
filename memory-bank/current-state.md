# Estado actual

## Current State

**Qué funciona:**
- Backend: 16 tests de `pytest` pasan (`python3 -m pytest -q` ejecutado en esta sesión), cubriendo generación de datos mock, filtros por fecha/categoría/tipo, y los 9 endpoints (incluido el guard de lista vacía agregado en `build_metrics_facets`, ver [risks.md](./risks.md) y [../verification.md](../verification.md)).
- Frontend: build declarado vía `"build": "tsc -b && vite build"` en `frontend/package.json`; tests de lógica (`financial-utils.test.ts`) cubren `computeKPIs`, `computeMonthlyData`, `formatCurrency`, `formatPercent`.
- Frontend: `npm ci && npm run build` se ejecutó correctamente en la rama de trabajo; Vite dejó una advertencia por un chunk minificado superior a 500 kB.
- Arranque completo documentado y consistente entre `README.md`, `docker-compose.yml` y los Dockerfiles (`docker compose up --build`).
- Línea base de calidad documentada en [quality-baseline.md](./quality-baseline.md), incluyendo las auditorías `accessibility` y `vercel-react-best-practices`.

**Qué no está verificado:**
- Contenido real de `frontend/.env.example` (bloqueado para lectura automatizada en este entorno).
- Si `frontend/src/lib/mock-data.ts` se usa actualmente en algún componente (no inspeccionado).
- Cobertura de tests de componentes React — no existe (`*.test.tsx` ausente en `frontend/src/components/`).
- Auditoría automatizada de accesibilidad y medición de campo de Core Web Vitals — no existe tooling ni ejecución documentada.

**Riesgos observados:** ver detalle completo con evidencia en [risks.md](./risks.md) y la línea base de calidad en [quality-baseline.md](./quality-baseline.md). Resumen: falta de manejo de errores generalizado en el backend (parcialmente corregido en `build_metrics_facets`), seed de datos mock duplicado en 8 endpoints, tipos de dominio duplicados manualmente backend/frontend, CORS abierto (`allow_origins=["*"]`), bundle inicial grande, gaps de accesibilidad/SEO pendientes y ausencia de CI/CD.

**Próximos pasos razonables** (basados solo en huecos evidenciados, no en roadmap inventado):
- Replicar el guard de lista vacía (agregado en `build_metrics_facets`) en otras funciones de `routes.py` que indexan listas sin verificar (`calculate_net_value`, `summarize_movements` con listas vacías no se verificaron en esta sesión).
- Añadir un mecanismo de sincronización o generación automática de tipos entre `backend/app/routes.py` y `frontend/src/lib/financial-types.ts` para eliminar la duplicación manual de `Literal`/union types.
- Configurar un pipeline de CI (`.github/workflows/`) que al menos ejecute `pytest` y `npm run test`/`npm run lint`, ya que hoy la única validación es manual/local.

## Historial de commits

✅ **Verificada** — Salida real de `git log --oneline -15` en este workspace (rama `main`, sincronizada con `origin/main`):
```
954f812 (HEAD -> main, origin/main, origin/HEAD) Merge pull request #1 from deimianvasquez/main
eeece05 feat: use Vite API proxy and document frontend env setup
f0812fa Update Spanish README with corrected link for project initiation instructions.
291f2db .agents folder structure in Readme
4510e15 Enhance documentation for agents and project structure.
cfd18e4 Update repo slug
87e1942 Refactor list comprehensions for clarity in movement filtering.
0c07552 Add anomaly alerts endpoint based on outcome spikes.
5df15b4 Add period-over-period comparison endpoint for net movement.
be510b5 Add top categories endpoint for ranked financial drivers.
2b5c237 Add period summary endpoint for financial aggregates.
959bc84 Add metrics facets endpoint for discoverable filters.
c061621 Add operation and category filters to metrics endpoints.
cbd20dc Adapt readmes
c5dc883 Remove extra content in Readme
```
El historial muestra desarrollo incremental del backend endpoint por endpoint (filtros → facetas → resumen → top categorías → comparación → alertas), y trabajo reciente de documentación (README, estructura `.agents`).

## Rama única

✅ **Verificada** — `git branch -a` solo muestra `main` local y `remotes/origin/main`/`origin/HEAD`. No hay otras ramas activas ni PRs abiertos visibles desde el repositorio local.

## Cambios sin commitear al momento de escribir este documento

✅ **Verificada** — `git status --short` (última ejecución en esta sesión) reporta:
```
 M backend/app/routes.py
 M backend/tests/test_routes.py
?? .agents/
?? frontend/src/components/ui/button.tsx
?? memory-bank/
?? verification.md
```
Es decir: el guard de errores agregado en `build_metrics_facets` y su test (`backend/app/routes.py`, `backend/tests/test_routes.py`), junto con `.agents/rules/`, `frontend/src/components/ui/button.tsx`, `memory-bank/` y `verification.md`, **aún no están commiteados ni pusheados** al momento de escribir este documento.

## Cobertura de tests

✅ **Verificada** — Backend: 16 tests pasan, confirmado por ejecución real de `python3 -m pytest -q` en `backend/` en esta sesión (15 preexistentes + 1 añadido: `test_build_metrics_facets_raises_404_for_empty_movements`), todos en [backend/tests/test_routes.py](../backend/tests/test_routes.py).
✅ **Verificada** — Frontend: solo `financial-utils.test.ts` (lógica de cálculo). No hay tests de componentes (`*.test.tsx`) — confirmado por ausencia en los listados de directorio de `frontend/src/components/`.

## CI/CD

❌ **No soportada por evidencia** — No existe `.github/workflows/` en el repositorio (búsqueda de archivos sin resultados). No hay pipeline automatizado de build/test/deploy documentado.
