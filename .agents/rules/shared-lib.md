# `frontend/src/lib/` es la única fuente de tipos y utilidades compartidas

## Alcance
Aplica a la definición de tipos TypeScript y funciones de cálculo/formato usadas por más de un componente.

## Evidencia
- `frontend/src/lib/financial-types.ts` define `FinancialMovement`, `KPIMetrics`, `MonthlyDataPoint`.
- `frontend/src/lib/financial-utils.ts` define `computeKPIs`, `computeMonthlyData` (y `formatCurrency`/`formatPercent`, usados y probados en `frontend/src/lib/financial-utils.test.ts`).
- `frontend/src/components/dashboard/kpi-row.tsx` importa ambos módulos vía alias: `from '@/lib/financial-types'` y `from '@/lib/financial-utils'`.

## Justificación
`financial-utils.test.ts` es el único archivo de test de lógica en todo el frontend (no hay tests de componentes). Si la lógica de cálculo se duplica dentro de un componente en lugar de vivir en `lib/`, esa duplicación queda sin cobertura de test.

## Instrucciones para futuros agentes
- Cualquier cálculo nuevo sobre `FinancialMovement[]` (sumas, porcentajes, agrupaciones) debe añadirse a `financial-utils.ts`, no inline en un componente `.tsx`.
- Al añadir una función a `financial-utils.ts`, añadir su test correspondiente en `financial-utils.test.ts` (patrón ya usado: `describe`/`it` de Vitest con `sampleMovements` de ejemplo).

## Qué NO hacer
- No crear un segundo archivo de tipos (p. ej. `types.ts` dentro de `components/dashboard/`) — `financial-types.ts` es la única fuente según la evidencia actual.
- No dejar funciones de cálculo sin test en `financial-utils.ts`; el patrón existente en el repo cubre el 100% de las funciones exportadas de ese archivo.
