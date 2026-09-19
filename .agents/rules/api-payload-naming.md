# No traducir a camelCase los campos que reflejan el JSON crudo del backend

## Alcance
Aplica a `frontend/src/lib/financial-types.ts` y a cualquier código que consuma la respuesta de los endpoints `/api/metrics*`.

## Evidencia
- `backend/app/routes.py` define `class FinancialMovement(BaseModel)` con campos snake_case: `create_date`, `amount`, `operation_type`, `category`, `business_type`.
- `frontend/src/lib/financial-types.ts` replica exactamente esos mismos nombres snake_case en `interface FinancialMovement`.
- Los tipos *derivados* en el mismo archivo (`KPIMetrics`: `totalIncome`, `profitPercent`) sí usan camelCase, porque no provienen directamente del JSON de la API sino de cálculos locales (`financial-utils.ts`).
- No existe ninguna capa de mapeo/transformación (`mapper.ts`, `adapter.ts`) entre la respuesta HTTP y `FinancialMovement` en el frontend.

## Justificación
Sin capa de mapeo, `FinancialMovement` en TypeScript debe calzar campo a campo con la respuesta real de FastAPI (que serializa los `BaseModel` de Pydantic tal cual, en snake_case). Cambiar los nombres en un solo lado rompe el parseo silenciosamente (los campos llegarían como `undefined`).

## Instrucciones para futuros agentes
- Si se agrega un campo nuevo a `FinancialMovement` en `backend/app/routes.py`, agregar el mismo campo con el mismo nombre (snake_case) en `frontend/src/lib/financial-types.ts`.
- Reservar camelCase únicamente para tipos que resultan de cálculos en `financial-utils.ts` (como `KPIMetrics`, `MonthlyDataPoint`), no para tipos que reflejan la respuesta HTTP directa.

## Qué NO hacer
- No renombrar `create_date`/`operation_type`/`business_type` a camelCase en `financial-types.ts` sin agregar una capa de transformación explícita en el fetch.
- No asumir que existe conversión automática snake_case → camelCase; no hay evidencia de librerías como `camelize-keys` en `frontend/package.json`.
