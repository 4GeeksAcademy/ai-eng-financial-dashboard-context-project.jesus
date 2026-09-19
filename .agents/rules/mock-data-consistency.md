# No introducir una fuente de datos distinta a `generate_mock_movements(seed=42)` sin revisar todos los endpoints

## Alcance
Aplica a cualquier cambio en la forma en que los endpoints de `backend/app/routes.py` obtienen sus datos.

## Evidencia
- Cada uno de los 8 endpoints de negocio en `backend/app/routes.py` llama individualmente a `generate_mock_movements(seed=42)`: `get_metrics`, `get_metrics_facets`, `get_metrics_summary`, `get_top_categories`, `get_metrics_comparison`, `get_metrics_alerts`, `get_b2b_metrics`, `get_b2c_metrics`.
- No existe ninguna función central (`get_movements()` compartida, caché, dependencia de FastAPI) que unifique esta llamada; cada endpoint la repite de forma literal.

## Justificación
Como el seed está hardcodeado de forma independiente en cada función, cambiarlo en un solo endpoint desincroniza los datos entre endpoints que un usuario del frontend puede estar comparando simultáneamente (p. ej. `/api/metrics` vs `/api/metrics/summary` para el mismo periodo).

## Instrucciones para futuros agentes
- Si se cambia el seed de datos mock, aplicar el cambio a las 8 ocurrencias de `generate_mock_movements(seed=42)` en `backend/app/routes.py` en la misma tarea (usar búsqueda exacta de la cadena antes de commitear).
- Si se decide centralizar esta llamada, actualizar también las funciones de test en `backend/tests/test_routes.py` que dependen de `generate_mock_movements(seed=42)` para reproducir resultados determinísticos.

## Qué NO hacer
- No cambiar el seed en un único endpoint como "prueba rápida" y dejar los demás con `seed=42`.
- No asumir que hay una dependencia de FastAPI (`Depends(...)`) inyectando los movimientos — no existe en el código actual.
