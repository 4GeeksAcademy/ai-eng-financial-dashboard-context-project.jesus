# Spec (propuesta): Expense Alerts

Feature del backend aún no consumida por ningún componente del frontend. Endpoint verificado corriendo localmente y explorado vía `/docs` + `curl` antes de escribir esta spec.

## Contrato del endpoint

Fuente: [../../backend/app/routes.py](../../backend/app/routes.py) (`get_metrics_alerts`, `detect_outcome_alerts`).

`GET /api/metrics/alerts`

| Query param | Tipo | Default | Notas |
|---|---|---|---|
| `threshold` | `float` | `0.3` | Validado `>= 0` |
| `group_by` | `'day' \| 'week' \| 'month'` | `'month'` | |
| `start_date` | `date \| null` | `None` | |
| `end_date` | `date \| null` | `None` | |
| `business_type` | `'B2B' \| 'B2C' \| null` | `None` | |

Respuesta: `MetricsAlert[]` — `{ period, outcome_total, baseline_average, increase_ratio }`.

### Comportamiento verificado con curl

- `GET /api/metrics/alerts` (sin params, `threshold=0.3` por default) → 4 alertas de ejemplo, p. ej. `{"period": "2025-12", "outcome_total": 103378.98, "baseline_average": 59573.44, "increase_ratio": 0.7353}`.
- `increase_ratio` es la fracción de incremento sobre el promedio histórico (`(outcome - baseline) / baseline`), **no un porcentaje ya multiplicado por 100** (0.7353 = +73.53%). El frontend debe multiplicar por 100 al mostrarlo, o usar `formatPercent` sobre `increase_ratio * 100`.
- El primer período de la serie **nunca** puede generar alerta (no hay historial previo con el que compararlo) — confirmado leyendo `detect_outcome_alerts`: `historical_outcomes` empieza vacío y solo se evalúa si ya tiene datos.
- Si `baseline` calculado es `0`, ese período se omite silenciosamente (sin alerta, sin error) — evita división por cero.
- No hay endpoint ni respuesta para "no hay alertas": el array simplemente puede venir vacío (`[]`), sin distinción respecto a "no hay datos" vs. "no hay incrementos anómalos".

## Feature propuesta para el frontend

### Componente: `ExpenseAlertsList` (nuevo, en `frontend/src/components/dashboard/`)

Props sugeridas:

| Prop | Tipo |
|---|---|
| `data` | `MetricsAlert[]` |
| `loading?` | `boolean` |

### Estados

1. `loading === true` → `Card` + `Skeleton`, mismo patrón que el resto de tarjetas del dashboard.
2. `loading` falsy y `data.length === 0` → mensaje explícito de "sin alertas en este periodo" (distinto del mensaje genérico `"No data available to display"`, porque aquí `[]` es un resultado válido y esperado, no necesariamente un error de datos).
3. `loading` falsy y `data.length > 0` → lista de alertas mostrando `period`, `outcome_total` (vía `formatCurrency`) y `increase_ratio * 100` (vía `formatPercent`), posiblemente con un ícono de advertencia (`lucide-react` ya está en dependencias, ver [../src/components/dashboard/dashboard-header.tsx](../src/components/dashboard/dashboard-header.tsx) que importa `LayoutDashboard` de esa librería).

### Riesgos a validar antes de implementar

- El tipo `MetricsAlert` no existe aún en [../src/lib/financial-types.ts](../src/lib/financial-types.ts).
- Si se expone `threshold` como control de usuario, validar en el frontend `threshold >= 0` antes de enviarlo (el backend responde 422 si no, pero mejor evitar el roundtrip).
- No hay forma de saber, solo con la respuesta, si el array vacío es porque no hay movimientos en el rango o porque no hubo incrementos — si se necesita esa distinción, requeriría combinar con `/api/metrics/summary` o `/api/metrics/facets`.
