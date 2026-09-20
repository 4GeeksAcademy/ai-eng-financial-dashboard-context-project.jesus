# Spec: `IncomeOutcomeChart`

Fuente: [../src/components/dashboard/income-outcome-chart.tsx](../src/components/dashboard/income-outcome-chart.tsx)

## Props

| Prop | Tipo | Requerido |
|---|---|---|
| `data` | `MonthlyDataPoint[]` | Sí |
| `loading` | `boolean` | No |

`MonthlyDataPoint` (de [../src/lib/financial-types.ts](../src/lib/financial-types.ts)): `{ month, income, outcome, profitPercent }`.

## Estados de renderizado (mutuamente excluyentes, en este orden de precedencia)

1. **`loading === true`** → `Card` con `Skeleton` de título, descripción y área de gráfico (`h-[280px]`). Ignora `data` por completo.
2. **`loading` falsy y `!hasData`** → título/descripción reales, pero el cuerpo muestra `"No data available to display"` centrado en un contenedor de `h-[280px]`.
   - `hasData = data.some((d) => d.income > 0 || d.outcome > 0)`.
3. **`loading` falsy y `hasData === true`** → `LineChart` (recharts) con:
   - Eje X: `dataKey="month"`, sin línea de eje ni ticks visibles (`axisLine={false}`, `tickLine={false}`).
   - Eje Y: formateada en miles con `tickFormatter={(v) => \`$${(v / 1000).toFixed(0)}k\`}`, ancho fijo `48`.
   - Tooltip personalizado (`CustomTooltip`): si `active` es falsy o `payload` vacío, no renderiza nada (`return null`); si no, muestra `label` (mes) y cada serie con su color y valor formateado con `formatCurrency`.
   - Dos líneas: `income` (color `var(--chart-income)`) y `outcome` (color `var(--chart-outcome)`), ambas `type="monotone"`, `strokeWidth={2}`.
   - `Legend` con formatter que capitaliza vía CSS (`capitalize`), no transforma el string.

## Título y descripción fijos

- `CardTitle`: `"Income vs. Outcome"`.
- `CardDescription`: `"Monthly revenue and expenditure evolution"`.
