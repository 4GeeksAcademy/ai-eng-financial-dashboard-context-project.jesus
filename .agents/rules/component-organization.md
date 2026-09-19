# Mantener `components/dashboard/` (negocio) separado de `components/ui/` (primitivos shadcn)

## Alcance
Aplica a la creación o modificación de cualquier componente React en `frontend/src/components/`.

## Evidencia
- `frontend/src/components/dashboard/` contiene componentes de negocio con datos financieros: `kpi-card.tsx`, `dashboard-header.tsx`, `kpi-row.tsx`, `income-outcome-chart.tsx`, `profit-percent-chart.tsx`.
- `frontend/src/components/ui/` contiene solo primitivos genéricos sin lógica de negocio: `card.tsx`, `skeleton.tsx`, `button.tsx`.
- `frontend/components.json` fija la configuración del generador shadcn (`"style": "new-york"`, `"aliases": {"ui": "@/components/ui"}`), que apunta específicamente a esa carpeta.

## Justificación
El CLI de shadcn puede regenerar/sobreescribir archivos dentro de `components/ui/` usando la configuración de `components.json`. Si se mezcla lógica de negocio ahí, una regeneración futura puede borrarla sin que sea obvio por qué.

## Instrucciones para futuros agentes
- Componentes que consuman `FinancialMovement`, `KPIMetrics` o cualquier tipo de `frontend/src/lib/financial-types.ts` van en `components/dashboard/`.
- Componentes que solo envuelven un elemento HTML genérico (`div`, `button`, `span`) sin conocimiento del dominio financiero van en `components/ui/`.

## Qué NO hacer
- No importar tipos de `@/lib/financial-types` ni `@/lib/financial-utils` dentro de archivos en `components/ui/`.
- No añadir props específicas del dominio (p. ej. `variant: 'income' | 'outcome'`) a componentes de `components/ui/`; ese patrón pertenece a `components/dashboard/kpi-card.tsx`.
