# No fragmentar `backend/app/routes.py` sin actualizar imports dependientes

## Alcance
Aplica a cualquier cambio que mueva código de `backend/app/routes.py` a nuevos archivos/módulos (`models.py`, `services.py`, etc.).

## Evidencia
- `backend/app/routes.py` concentra modelos Pydantic (`FinancialMovement`, `MetricsFacets`, etc.), funciones de negocio (`generate_mock_movements`, `filter_movements`, `build_metrics_facets`, etc.) y los 9 endpoints, todo en un único archivo.
- `backend/app/main.py` importa `from app.routes import router`.
- `backend/tests/test_routes.py` importa directamente `from app.routes import build_metrics_facets, filter_movements_by_date, generate_mock_movements`.

## Justificación
No existe ninguna capa de indirección (`__init__.py` re-exportando símbolos, paquete `services/`) entre `routes.py` y quienes lo consumen. Cualquier reorganización rompe imports en tiempo de ejecución y en tests, no solo en tipado.

## Instrucciones para futuros agentes
- Si se necesita dividir `routes.py`, actualizar en el mismo cambio todos los `import` en `backend/app/main.py` y `backend/tests/test_routes.py`.
- Ejecutar `python3 -m pytest -q` en `backend/` después de cualquier reorganización para confirmar que los imports siguen resolviendo.

## Qué NO hacer
- No renombrar ni mover `generate_mock_movements`, `filter_movements_by_date` o `build_metrics_facets` sin grep previo de sus usos en `backend/tests/`.
- No asumir que hay un paquete `models/` o `services/` — no existe en el repo actual.

---

Nota: las reglas sobre organización de `components/dashboard/` vs `components/ui/` y sobre `frontend/src/lib/` como fuente única de tipos/utilidades se movieron a archivos dedicados: ver [component-organization.md](./component-organization.md) y [shared-lib.md](./shared-lib.md).
