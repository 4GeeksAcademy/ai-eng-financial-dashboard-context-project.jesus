# Manejar explícitamente las listas de movimientos vacías antes de indexarlas

## Alcance
Aplica a cualquier función en `backend/app/routes.py` que reciba `list[FinancialMovement]` y acceda a índices (`[0]`, `[-1]`) o asuma que la lista no está vacía.

## Evidencia
- Antes de esta sesión, `build_metrics_facets` accedía a `ordered[0].create_date` y `ordered[-1].create_date` sin ninguna verificación previa.
- Búsqueda de `HTTPException|try:|except |raise` en todo `backend/` antes del cambio no arrojó ningún manejo de errores real en el archivo.
- Corrección aplicada en esta sesión: `build_metrics_facets` ahora valida `if not ordered: raise HTTPException(status_code=404, ...)` antes de indexar (ver `backend/app/routes.py`), validado con el test `test_build_metrics_facets_raises_404_for_empty_movements` en `backend/tests/test_routes.py` (`pytest -q`: 16 tests pasan tras el cambio, 15 antes).

## Justificación
No hay ningún patrón previo de manejo de errores en el archivo; cualquier función nueva que filtre movimientos por criterios que puedan no tener coincidencias (fechas fuera de rango, categorías inexistentes) puede producir un `IndexError` sin control, devuelto como HTTP 500 genérico por FastAPI.

## Instrucciones para futuros agentes
- Antes de indexar una lista de movimientos filtrada (`[0]`, `[-1]`, `min()`, `max()`), verificar explícitamente que no esté vacía y lanzar `HTTPException` con un código de estado y mensaje claros, replicando el patrón agregado en `build_metrics_facets`.
- Agregar un test unitario que llame la función directamente con una lista vacía y verifique el `status_code` de la excepción, replicando `test_build_metrics_facets_raises_404_for_empty_movements`.

## Qué NO hacer
- No agregar manejo de errores genérico (`try/except Exception`) que oculte el tipo real de fallo; el patrón validado en este repo es una verificación explícita (`if not ordered`) antes de acceder al índice.
- No asumir que los endpoints que agregan filtros a `get_metrics_facets` (actualmente sin `Query` params) seguirán siempre recibiendo datos no vacíos si se les agregan filtros en el futuro.
