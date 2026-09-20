# Spec (propuesta): Top Categories

Feature del backend aún no consumida por ningún componente del frontend. Endpoint verificado corriendo localmente (`uvicorn` en `http://localhost:8000`) y explorado vía `/docs` + `curl` antes de escribir esta spec.

## Contrato del endpoint

Fuente: [../../backend/app/routes.py](../../backend/app/routes.py) (`get_top_categories`, `build_top_categories`).

`GET /api/metrics/categories/top`

| Query param | Tipo | Default | Notas |
|---|---|---|---|
| `operation_type` | `'income' \| 'outcome'` | `'outcome'` | |
| `limit` | `int` | `5` | Validado `1 <= limit <= 20` (422 fuera de rango) |
| `start_date` | `date \| null` | `None` | Filtra `create_date >= start_date` |
| `end_date` | `date \| null` | `None` | Filtra `create_date <= end_date` |
| `business_type` | `'B2B' \| 'B2C' \| null` | `None` | |

Respuesta: `TopCategoryItem[]` — `{ category, operation_type, total_amount }`, ordenado por `total_amount` descendente, recortado a `limit` elementos.

### Comportamiento verificado con curl

- `GET /api/metrics/categories/top` (sin params) → 4 categorías de `outcome` ordenadas por monto (`others` > `operational` > `administrative` > `suppliers`), sin error.
- `GET /api/metrics/categories/top?operation_type=income&limit=3` → solo **2** resultados (`sales`, `others`) aunque `limit=3`, porque solo existen 2 categorías con movimientos `income` en los datos mock. **La lista puede tener menos elementos que `limit`; no se rellena.**
- Si no hay movimientos que coincidan con los filtros, `build_top_categories` devuelve `[]` (no lanza 404, a diferencia de `/api/metrics/facets`).

## Feature propuesta para el frontend

### Componente: `TopCategoriesCard` (nuevo, en `frontend/src/components/dashboard/`)

Props sugeridas, siguiendo el patrón de `IncomeOutcomeChart`/`ProfitPercentChart`:

| Prop | Tipo |
|---|---|
| `data` | `TopCategoryItem[]` |
| `loading?` | `boolean` |

### Estados (mismo patrón que las cards de gráficos existentes)

1. `loading === true` → `Card` + `Skeleton` (título, descripción, lista).
2. `loading` falsy y `data.length === 0` → mensaje `"No data available to display"` (consistente con [income-outcome-chart.md](./income-outcome-chart.md)).
3. `loading` falsy y `data.length > 0` → lista/barra horizontal con `category`, `total_amount` formateado vía `formatCurrency` (de [../src/lib/financial-utils.ts](../src/lib/financial-utils.ts)).

### Riesgos a validar antes de implementar

- El tipo `TopCategoryItem` no existe aún en [../src/lib/financial-types.ts](../src/lib/financial-types.ts); debe agregarse manualmente (ver duplicación de tipos backend/frontend documentada en [../../memory-bank/risks.md](../../memory-bank/risks.md)).
- `App.tsx` no llama actualmente a `/api/metrics/categories/top`; habría que agregar un segundo `fetch` o extender `fetchFinancialData`.
