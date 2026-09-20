# Frontend Specs

Especificaciones funcionales del frontend (`frontend/src/`), derivadas directamente del código existente al momento de escribirse. Cada archivo describe props, comportamiento y estados de un componente o flujo, con cita al archivo fuente.

## Índice

- [app-dashboard.md](./app-dashboard.md) — flujo de datos de la página principal (`App.tsx`): fetch, cálculo de métricas y manejo de error/loading.
- [dashboard-header.md](./dashboard-header.md) — `DashboardHeader`.
- [kpi-row.md](./kpi-row.md) — `KPIRow` y `KPICard`.
- [income-outcome-chart.md](./income-outcome-chart.md) — `IncomeOutcomeChart`.
- [profit-percent-chart.md](./profit-percent-chart.md) — `ProfitPercentChart`.

Features del backend aún no consumidas por el frontend (propuestas de implementación, verificadas contra el backend corriendo en `http://localhost:8000`):

- [top-categories.md](./top-categories.md) — feature propuesta para `/api/metrics/categories/top`.
- [period-comparison.md](./period-comparison.md) — feature propuesta para `/api/metrics/comparison`.
- [expense-alerts.md](./expense-alerts.md) — feature propuesta para `/api/metrics/alerts`.

## Convención

- Cada spec documenta únicamente comportamiento verificable en el código citado (props, condicionales, valores por defecto).
- Si se modifica un componente, actualizar su spec correspondiente en el mismo cambio.
- No hay tests de componentes en este repo (`*.test.tsx` ausente, ver [../../.agents/rules/frontend-testing-scope.md](../../.agents/rules/frontend-testing-scope.md)); estas specs no reemplazan tests automatizados, documentan el comportamiento esperado.
