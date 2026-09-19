# Product — Financial Metrics Dashboard

## Descripción del producto

✅ **Verificada** — Cita literal de [README.md](../README.md):
> "Financial metrics dashboard with a React + TypeScript frontend and a FastAPI backend."

✅ **Verificada** — El backend expone datos financieros simulados (no reales): [backend/app/routes.py](../backend/app/routes.py) función `generate_mock_movements(seed=42)` genera movimientos aleatorios (`random.uniform`, `random.choice`) de tipo `income`/`outcome`, con categorías (`suppliers`, `sales`, `operational`, `administrative`, `others`) y tipo de negocio (`B2B`/`B2C`).

✅ **Verificada** — Funcionalidades expuestas por la API, evidenciadas por los endpoints en `routes.py`:
- Listado de movimientos filtrable por fecha/categoría/tipo (`/api/metrics`)
- Facetas disponibles para filtros (`/api/metrics/facets`)
- Resumen agregado por día/semana/mes (`/api/metrics/summary`)
- Top categorías por monto (`/api/metrics/categories/top`)
- Comparación entre periodos (`/api/metrics/comparison`)
- Alertas de incremento de gasto (`/api/metrics/alerts`)
- Filtrado por tipo de negocio B2B/B2C (`/api/metrics/b2b`, `/api/metrics/b2c`)

✅ **Verificada** — El frontend consume estos datos para mostrar KPIs (ingreso total, gasto total, ganancia, % de ganancia) y gráficos: ver componentes [frontend/src/components/dashboard/kpi-row.tsx](../frontend/src/components/dashboard/kpi-row.tsx), [income-outcome-chart.tsx](../frontend/src/components/dashboard/income-outcome-chart.tsx), [profit-percent-chart.tsx](../frontend/src/components/dashboard/profit-percent-chart.tsx).

❓ **Parcialmente verificada** — No encontré evidencia de persistencia real (base de datos, archivo de datos). Todo lo inspeccionado usa datos generados en memoria con seed fijo (`seed=42`). No confirmé si esto es intencional como "modo demo" o un estado temprano/incompleto del producto — es una inferencia razonable pero no está documentada explícitamente en el repo.
