# Spec: `ProfitPercentChart`

Fuente: [../src/components/dashboard/profit-percent-chart.tsx](../src/components/dashboard/profit-percent-chart.tsx)

## Props

| Prop | Tipo | Requerido |
|---|---|---|
| `data` | `MonthlyDataPoint[]` | Sí |
| `loading` | `boolean` | No |

## Estados de renderizado (mismo patrón que `IncomeOutcomeChart`, ver [income-outcome-chart.md](./income-outcome-chart.md))

1. **`loading === true`** → `Card` con `Skeleton` de título, descripción y área de gráfico. Ignora `data`.
2. **`loading` falsy y `!hasData`** → mensaje `"No data available to display"` centrado en `h-[280px]`.
   - `hasData = data.some((d) => d.profitPercent !== 0)` — a diferencia de `IncomeOutcomeChart`, aquí un solo mes con `profitPercent !== 0` ya cuenta como "hay datos", incluso si `income`/`outcome` son 0.
3. **`loading` falsy y `hasData === true`** → `LineChart` con:
   - Eje X: `dataKey="month"`, sin línea/ticks visibles.
   - Eje Y: `tickFormatter={(v) => \`${v.toFixed(0)}%\`}`, ancho fijo `40`, `domain={['auto', 'auto']}` (a diferencia del otro gráfico, no fuerza dominio desde 0).
   - `ReferenceLine y={0}` punteada, para marcar el punto de equilibrio (margen 0%).
   - Tooltip personalizado: si no hay `payload`, `return null`; si hay, muestra `"Profit margin: {value.toFixed(1)}%"` con color `var(--chart-profit)`. Usa `payload[0]?.value ?? 0` (una sola serie, a diferencia del tooltip de ingreso/egreso que itera `payload.map`).
   - Una sola línea: `profitPercent`, color `var(--chart-profit)`, `strokeWidth={2}`.
   - No tiene `Legend` (a diferencia de `IncomeOutcomeChart`).

## Título y descripción fijos

- `CardTitle`: `"Profit Margin %"`.
- `CardDescription`: `"Monthly profit as a percentage of total income"`.
