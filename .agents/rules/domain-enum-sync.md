# Sincronizar los valores `Literal`/union type de `Category`, `OperationType`, `BusinessType` en ambos lenguajes

## Alcance
Aplica a cualquier cambio en las categorías, tipos de operación o tipos de negocio válidos del dominio.

## Evidencia
- `backend/app/routes.py` define `Category = Literal["suppliers", "sales", "operational", "administrative", "others"]`, `OperationType = Literal["income", "outcome"]`, `BusinessType = Literal["B2B", "B2C"]`, y la lista paralela `OUTCOME_CATEGORIES`.
- `frontend/src/lib/financial-types.ts` define los mismos valores como union types de TypeScript: `export type Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'`.
- No hay generación automática de tipos desde OpenAPI (no existe script `openapi-typescript` ni similar en `frontend/package.json`).

## Justificación
Los valores están escritos a mano en dos lenguajes distintos sin ninguna herramienta que los sincronice. Un cambio unilateral no produce ningún error de build que lo detecte automáticamente — el frontend simplemente aceptaría o rechazaría datos de forma inconsistente con el backend.

## Instrucciones para futuros agentes
- Al agregar/quitar un valor de `Category`, `OperationType` o `BusinessType` en `backend/app/routes.py`, aplicar el mismo cambio en la misma tarea a `frontend/src/lib/financial-types.ts`.
- Si se agrega una categoría de tipo `outcome`, actualizar también `OUTCOME_CATEGORIES` en `backend/app/routes.py` (usada por `_build_movement` para generar datos mock coherentes).

## Qué NO hacer
- No cambiar los literales solo en un lado "porque el otro no importa ahora mismo" — no hay mecanismo de detección de esta desincronización en CI (no existe `.github/workflows/`).
- No introducir nuevas categorías directamente en un componente de UI sin antes reflejarlas en `financial-types.ts` y `routes.py`.
