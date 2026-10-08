# Riesgos conocidos

Todos los riesgos listados aquí están además documentados como reglas accionables en [.agents/rules/](../.agents/rules/).

## 1. Manejo de errores inexistente en el backend (parcialmente corregido)

✅ **Verificada** — Búsqueda exhaustiva de `HTTPException`, `try`/`except`, `raise` en `backend/` originalmente no encontró manejo de errores real en [backend/app/routes.py](../backend/app/routes.py) ni [backend/app/main.py](../backend/app/main.py).
**Riesgo:** funciones que acceden a `ordered[0]`/`ordered[-1]` sin verificar lista vacía pueden producir un `IndexError` → HTTP 500 sin mensaje claro.
**Corrección aplicada:** `build_metrics_facets` ahora lanza `HTTPException(status_code=404, ...)` si la lista está vacía, validado con `test_build_metrics_facets_raises_404_for_empty_movements` en [backend/tests/test_routes.py](../backend/tests/test_routes.py) (`pytest -q`: 16 tests pasan). **Riesgo residual:** otras funciones de `routes.py` que indexan listas (`calculate_net_value`, `summarize_movements`) no fueron revisadas ni corregidas en esta sesión.

## 2. Seed de datos mock duplicado en cada endpoint

✅ **Verificada** — `generate_mock_movements(seed=42)` se llama de forma independiente y repetida en al menos 7 funciones de `routes.py` (`get_metrics`, `get_metrics_facets`, `get_metrics_summary`, `get_top_categories`, `get_metrics_comparison`, `get_metrics_alerts`, `get_b2b_metrics`, `get_b2c_metrics`), sin una función central compartida.
**Riesgo:** modificar el seed en un solo endpoint desincroniza los datos entre endpoints que deberían ser comparables.

## 3. Tipos duplicados manualmente entre backend y frontend

✅ **Verificada** — `Category`, `OperationType`, `BusinessType` están definidos como `Literal` en [backend/app/routes.py](../backend/app/routes.py) y replicados como *union types* de TypeScript en [frontend/src/lib/financial-types.ts](../frontend/src/lib/financial-types.ts), sin generación automática desde OpenAPI.
**Riesgo:** un cambio en un solo lado (agregar/quitar una categoría) rompe la sincronización sin que ninguna herramienta lo detecte automáticamente en build.

## 4. Alias `@/*` y proxy `/api` acoplados a nombres literales en múltiples archivos

✅ **Verificada** — El alias `@/*` está definido por separado en [frontend/tsconfig.app.json](../frontend/tsconfig.app.json) y [frontend/vite.config.ts](../frontend/vite.config.ts). El proxy de Vite depende del nombre de servicio Docker `backend` (`vite.config.ts` `target: "http://backend:8000"`), que coincide con el nombre del servicio en [docker-compose.yml](../docker-compose.yml).
**Riesgo:** cambiar cualquiera de estos nombres/alias en un solo archivo rompe builds o el proxy de forma silenciosa.

## 5. CORS totalmente abierto

✅ **Verificada** — [backend/app/main.py](../backend/app/main.py): `allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]`.
**Riesgo:** configuración adecuada para desarrollo local, pero insegura si se despliega tal cual a un entorno con datos reales o autenticación, ya que `allow_credentials=True` combinado con `allow_origins=["*"]` es una práctica desaconsejada por las especificaciones CORS/OWASP.

## 6. Ausencia de CI/CD

❌ **No soportada por evidencia** — No hay `.github/workflows/`. No hay validación automática de lint/tests/build antes de mergear a `main` (el historial de `git log` muestra un merge directo del PR #1 sin evidencia de checks).
**Riesgo:** cambios rotos pueden llegar a `main` sin detección automática; depende enteramente de revisión manual.

## 7. Sin persistencia real de datos

✅ **Verificada** — Todos los endpoints regeneran datos en memoria vía `generate_mock_movements`; no hay conexión a base de datos en `requirements.txt` ni en `docker-compose.yml`.
**Riesgo:** cualquier funcionalidad futura que asuma persistencia (guardar movimientos, histórico real) requiere una reescritura arquitectónica; el estado actual es solo de datos simulados con seed fijo.

## 8. Contenido de `frontend/.env.example` no verificable en este entorno

❓ **Parcialmente verificada** — El archivo existe pero su contenido está bloqueado para lectura automatizada en este entorno de trabajo.
**Riesgo:** documentación o cambios futuros que asuman el formato exacto de esa variable deben confirmarse abriendo el archivo manualmente, no asumiendo su contenido.

## 9. Accesibilidad del dashboard no automatizada

⚠️ **Pendiente** — La auditoría interna `accessibility` identificó necesidades de nombres accesibles para iconos y regiones, anuncios de estados de carga/error, alternativas textuales para gráficos, foco visible y verificación formal de contraste en el frontend (`frontend/src/`). No existe axe, Lighthouse ni una suite de tests de componentes que mantenga estos criterios.
**Riesgo:** regresiones de teclado, lector de pantalla o contraste pueden llegar a producción sin detección automática.
**Referencia:** [quality-baseline.md](./quality-baseline.md).

## 10. Rendimiento y metadatos frontend pendientes

⚠️ **Verificada parcialmente** — La auditoría `vercel-react-best-practices` confirmó que el proyecto usa Vite + React, no Next.js, y que no usa `next/image` ni `next/font`. El build pasa, pero genera un chunk minificado superior a 500 kB por la carga inicial de Recharts. `frontend/index.html` todavía contiene metadatos mínimos y el error de carga puede insertar contenido y desplazar el dashboard.
**Riesgo:** peor LCP/INP, SEO incompleto y posibles desplazamientos de layout (CLS).
**Referencia:** [quality-baseline.md](./quality-baseline.md).

## 11. Skills de calidad no versionadas

⚠️ **Verificada** — Se aplicaron las prácticas `accessibility` y `vercel-react-best-practices`, pero el repositorio actual no contiene `.agents/skills/`; solo contiene reglas en `.agents/rules/`.
**Riesgo:** otros agentes no pueden descubrir ni ejecutar automáticamente las skills, y su alcance puede divergir si no se versionan.
