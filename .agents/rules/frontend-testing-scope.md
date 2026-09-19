# El frontend solo tiene cobertura de test para `financial-utils.ts`, no para componentes

## Alcance
Aplica a cambios en `frontend/src/components/**` y a la percepción de qué está cubierto por tests automatizados en el frontend.

## Evidencia
- `frontend/src/lib/financial-utils.test.ts` prueba `computeKPIs`, `computeMonthlyData`, `formatCurrency`, `formatPercent` (confirmado por sus imports: `import { computeKPIs, computeMonthlyData, formatCurrency, formatPercent } from "./financial-utils"`).
- No existe ningún archivo `*.test.tsx` en `frontend/src/components/` (confirmado por listado de directorio de `frontend/src/components/dashboard/` y `frontend/src/components/ui/`).
- `frontend/package.json` define `"test": "vitest run"` como único comando de test del frontend.

## Justificación
Cambios en componentes (`KPICard`, `DashboardHeader`, `KPIRow`, gráficos) no están validados automáticamente por `npm run test`; solo la lógica de cálculo en `lib/` lo está. Asumir cobertura de UI que no existe puede llevar a introducir regresiones visuales o de props sin que ningún test las detecte.

## Instrucciones para futuros agentes
- Al modificar un componente, ejecutar `npm run test` únicamente confirma que la lógica de `financial-utils.ts` sigue intacta, no que el componente renderiza correctamente.
- Si se agrega lógica de cálculo nueva a un componente, considerar moverla a `financial-utils.ts` (ver regla `shared-lib.md`) para que quede cubierta por el mismo patrón de test existente.

## Qué NO hacer
- No reportar "tests pasan" como evidencia de que un cambio de componente es seguro sin aclarar que no hay tests de componentes en este repo.
- No inventar la existencia de `@testing-library/react` u otra librería de testing de componentes — no aparece en `frontend/package.json`.
