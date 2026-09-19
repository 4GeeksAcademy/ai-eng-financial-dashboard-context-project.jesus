## Product Overview

Solo hechos verificables, con cita de archivo.

- **Qué es:** "Financial metrics dashboard with a React + TypeScript frontend and a FastAPI backend." — cita literal de [README.md](../README.md).
- **Qué expone la API** (todos los endpoints confirmados leyendo [backend/app/routes.py](../backend/app/routes.py)):
  - `/api/metrics` — listado de movimientos financieros filtrable por fecha, categoría y tipo de operación.
  - `/api/metrics/facets` — valores disponibles para filtros (categorías, tipos de negocio, rango de fechas).
  - `/api/metrics/summary` — agregación de ingresos/egresos por día, semana o mes.
  - `/api/metrics/categories/top` — categorías con mayor monto acumulado.
  - `/api/metrics/comparison` — comparación de neto entre un periodo y el periodo anterior equivalente.
  - `/api/metrics/alerts` — detección de incrementos anómalos de gasto respecto a un baseline histórico.
  - `/api/metrics/b2b` y `/api/metrics/b2c` — mismos movimientos filtrados por tipo de negocio.
  - `/health` — healthcheck simple (`{"status": "ok"}`).
- **Qué muestra el frontend:** KPIs (ingreso total, egreso total, ganancia, % de ganancia) y gráficos de ingreso/egreso y % de ganancia — confirmado por [frontend/src/components/dashboard/kpi-row.tsx](../frontend/src/components/dashboard/kpi-row.tsx), [income-outcome-chart.tsx](../frontend/src/components/dashboard/income-outcome-chart.tsx), [profit-percent-chart.tsx](../frontend/src/components/dashboard/profit-percent-chart.tsx).
- **Origen de los datos:** simulados en memoria con semilla fija `seed=42` (función `generate_mock_movements` en `backend/app/routes.py`), no hay base de datos ni archivo de datos persistente en el repo.

❓ **No verificado:** si el "modo mock" es un estado temporal de desarrollo o una decisión de producto permanente — no hay documentación explícita en el repo sobre este punto.
