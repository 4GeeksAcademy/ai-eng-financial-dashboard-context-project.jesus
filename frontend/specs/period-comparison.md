# Spec (propuesta): Period Comparison

Feature del backend aún no consumida por ningún componente del frontend. Endpoint verificado corriendo localmente y explorado vía `/docs` + `curl` antes de escribir esta spec.

## Contrato del endpoint

Fuente: [../../backend/app/routes.py](../../backend/app/routes.py) (`get_metrics_comparison`).

`GET /api/metrics/comparison`

| Query param | Tipo | Requerido | Notas |
|---|---|---|---|
| `start_date` | `date` | **Sí** | Sin default (`Query(...)`) |
| `end_date` | `date` | **Sí** | Sin default (`Query(...)`) |
| `business_type` | `'B2B' \| 'B2C' \| null` | No | |

Respuesta: `MetricsComparison` — `{ current_period, previous_period, delta_abs, delta_pct }`.

### Comportamiento verificado con curl

- `GET /api/metrics/comparison` (sin `start_date`/`end_date`) → **422** con `detail` listando ambos campos como `"Field required"`. **No hay valores por defecto; el frontend debe enviar siempre ambas fechas.**
- `GET /api/metrics/comparison?start_date=2026-06-01&end_date=2026-08-31` → `200` con `{"current_period": 89742.94, "previous_period": 149954.49, "delta_abs": -60211.55, "delta_pct": -40.15}`.
- El periodo previo se calcula automáticamente en el backend con la misma duración (`end_date - start_date`) inmediatamente antes de `start_date`; el frontend no necesita calcularlo ni enviarlo.
- `delta_pct` es `null` (no `0`) cuando `previous_period == 0`, para evitar división por cero — el frontend debe manejar explícitamente el caso `null` (por ejemplo, mostrar "N/A" en vez de `NaN%`).

## Feature propuesta para el frontend

### Componente: `PeriodComparisonCard` (nuevo, en `frontend/src/components/dashboard/`)

Props sugeridas:

| Prop | Tipo |
|---|---|
| `data` | `MetricsComparison \| null` |
| `loading?` | `boolean` |

### Estados

1. `loading === true` → `Card` + `Skeleton`, siguiendo el patrón de `KPICard`.
2. `loading` falsy y `data === null` (fetch falló o no se han seleccionado fechas) → mostrar `'—'`, igual que `KPIRow` cuando `metrics` es `null`.
3. `loading` falsy y `data` presente → mostrar `current_period` y `previous_period` formateados con `formatCurrency`, `delta_abs` con signo, y `delta_pct` con `formatPercent` **solo si no es `null`**; si es `null`, mostrar un texto alternativo explícito (no calcularlo en el frontend).

### Riesgos a validar antes de implementar

- Requiere que la UI capture o derive un rango de fechas (`start_date`/`end_date`) — hoy no existe ningún selector de fechas en `App.tsx` ni en ningún componente (confirmado por ausencia de `<input type="date">` o librería de date-picker en `frontend/package.json`).
- El tipo `MetricsComparison` no existe aún en [../src/lib/financial-types.ts](../src/lib/financial-types.ts).
- Sin fechas por defecto documentadas por el backend, el frontend debe decidir un rango inicial razonable (p. ej. mes actual) antes de hacer el primer fetch.
