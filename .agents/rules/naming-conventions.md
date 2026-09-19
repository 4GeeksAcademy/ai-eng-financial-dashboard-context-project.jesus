# Los archivos `.tsx`/`.ts` van en kebab-case; los componentes exportados en PascalCase con named export

## Alcance
Aplica a la creación de cualquier archivo nuevo en `frontend/src/components/` o `frontend/src/lib/`.

## Evidencia
- `frontend/src/components/dashboard/kpi-card.tsx` exporta `export function KPICard(...)`.
- `frontend/src/components/dashboard/dashboard-header.tsx` exporta `export function DashboardHeader(...)`.
- `frontend/src/components/ui/card.tsx` agrupa sus exports al final del archivo: `export { Card, CardHeader, CardFooter, ... }`.
- Ningún componente del repo usa `export default`.
- `frontend/tsconfig.app.json` define `"paths": {"@/*": ["./src/*"]}`, usado por todos los imports (`@/components/...`, `@/lib/...`).

## Justificación
Los imports en todo el árbol usan el alias `@/...` con el nombre de archivo literal en kebab-case. Cambiar la convención de nombres rompe esos imports sin que TypeScript necesariamente avise antes del build.

## Instrucciones para futuros agentes
- Nombrar archivos nuevos en kebab-case (`nuevo-componente.tsx`), nunca PascalCase ni camelCase.
- Exportar el componente como función nombrada (`export function NombreComponente(...)`), replicando el patrón de `kpi-card.tsx`/`card.tsx`.

## Qué NO hacer
- No usar `export default` en ningún componente nuevo — no hay precedente de ese patrón en el repo.
- No renombrar archivos existentes a PascalCase sin actualizar todos sus imports vía `@/...` en el resto del árbol.
