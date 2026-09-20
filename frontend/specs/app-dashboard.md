# Spec: `App` — flujo principal del dashboard

Fuente: [../src/App.tsx](../src/App.tsx)

## Responsabilidad

Componente raíz que obtiene los movimientos financieros desde el backend, calcula KPIs y datos mensuales, y orquesta los estados de carga/error para el resto de la UI.

## Flujo de datos

1. Al montar (`useEffect`), llama a `fetchFinancialData()`, que hace `GET ${API_BASE_URL}/api/metrics`.
   - `API_BASE_URL` viene de `import.meta.env.VITE_API_BASE_URL`, con fallback a cadena vacía (usa proxy relativo).
2. Si la respuesta no es OK (`!response.ok`), lanza `Error("Failed to fetch financial data: ${response.status}")`.
3. En éxito: `computeKPIs(movements)` → `setMetrics`; `computeMonthlyData(movements)` → `setMonthlyData`.
4. En error (catch): `setError("No se pudo cargar la informacion financiera. Revisa la API de backend.")`.
5. En `finally`: `setLoading(false)`.

## Estados

| Estado | Tipo | Valor inicial |
|---|---|---|
| `metrics` | `KPIMetrics \| null` | `null` |
| `monthlyData` | `MonthlyDataPoint[]` | `[]` |
| `loading` | `boolean` | `true` |
| `error` | `string \| null` | `null` |

## Renderizado

- `<main>` con clase `dark` fija (tema oscuro forzado, no hay toggle de tema).
- `DashboardHeader` con `period="2024 - Full Year"` fijo (no configurable desde `App`).
- Si `error` es truthy, se muestra un bloque `<div>` con el mensaje antes de las secciones de KPIs/gráficos (el contenido de esas secciones se sigue renderizando igual, con `metrics=null` / `monthlyData=[]` si el fetch falló).
- `<section aria-label="Key performance indicators">` contiene `KPIRow`.
- `<section aria-label="Financial charts">` contiene `IncomeOutcomeChart` y `ProfitPercentChart`, en grid de 1 columna (`grid-cols-1`) o 2 columnas desde `xl` (`xl:grid-cols-2`).
- `loading` se pasa igual a `KPIRow`, `IncomeOutcomeChart` y `ProfitPercentChart`.

## No cubierto por este componente

- No hay reintento automático de fetch ni botón de "reintentar".
- No hay paginación ni filtros de fecha/categoría en la UI (aunque el backend los soporta, ver [../../memory-bank/project-overview.md](../../memory-bank/project-overview.md)).
