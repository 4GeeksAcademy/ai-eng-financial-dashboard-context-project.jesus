# Spec: `KPIRow` y `KPICard`

Fuentes: [../src/components/dashboard/kpi-row.tsx](../src/components/dashboard/kpi-row.tsx), [../src/components/dashboard/kpi-card.tsx](../src/components/dashboard/kpi-card.tsx)

## `KPIRow`

### Props

| Prop | Tipo | Requerido |
|---|---|---|
| `metrics` | `KPIMetrics \| null` | Sí |
| `loading` | `boolean` | No |

`KPIMetrics` (de [../src/lib/financial-types.ts](../src/lib/financial-types.ts)): `{ totalIncome, totalOutcome, profit, profitPercent }` (todos `number`).

### Comportamiento

- Renderiza un grid (`grid-cols-1` en móvil, `sm:grid-cols-2`, `xl:grid-cols-4`) con exactamente 4 `KPICard` fijos, en este orden:
  1. **Total Income** — `variant="income"`, ícono `TrendingUp`, valor `formatCurrency(metrics.totalIncome)`.
  2. **Total Outcome** — `variant="outcome"`, ícono `TrendingDown`, valor `formatCurrency(metrics.totalOutcome)`.
  3. **Profit** — `variant="profit"`, ícono `DollarSign`, valor `formatCurrency(metrics.profit)`.
  4. **Profit Margin** — `variant="profitPercent"`, ícono `BarChart2`, valor `formatPercent(metrics.profitPercent)`.
- Si `metrics` es `null`, cada `value` se renderiza como `'—'` (em-dash) en lugar de invocar el formateador.
- El `helperText` de cada tarjeta es un texto fijo por KPI (no derivado de datos), por ejemplo: `"Cumulative revenue from all income movements"` para Total Income.
- `loading` se propaga igual a las 4 `KPICard`.

## `KPICard`

### Props

| Prop | Tipo | Requerido |
|---|---|---|
| `label` | `string` | Sí |
| `value` | `string` | Sí |
| `helperText` | `string` | Sí |
| `icon` | `LucideIcon` | Sí |
| `variant` | `'income' \| 'outcome' \| 'profit' \| 'profitPercent'` | Sí |
| `loading` | `boolean` | No |

### Comportamiento

- Si `loading` es `true`, renderiza un `Card` con 3 `Skeleton` (label, ícono, valor, helper) y **no** renderiza `label`/`value`/`helperText`/`icon` reales.
- Si `loading` es falsy, renderiza:
  - `label` en mayúsculas vía CSS (`uppercase`), no transformado en JS.
  - Badge con ícono (`Icon`) coloreado según `variant`, usando clases CSS variable (`--income-badge`, `--outcome-badge`, `--profit-badge`; `profitPercent` reutiliza las variables de `profit`).
  - `value` como texto grande (`text-3xl`).
  - `helperText` como texto pequeño debajo.
- No valida el formato de `value` (recibe el string ya formateado por el caller).
