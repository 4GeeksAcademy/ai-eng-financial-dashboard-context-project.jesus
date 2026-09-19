# Los tests de backend dependen de imports directos de símbolos internos de `routes.py`

## Alcance
Aplica a cualquier cambio de nombre, firma o ubicación de funciones usadas por `backend/tests/test_routes.py`.

## Evidencia
- `backend/tests/test_routes.py` importa `from app.routes import build_metrics_facets, filter_movements_by_date, generate_mock_movements`.
- La suite usa `TestClient(app)` (importado de `app.main`) para probar los 9 endpoints reales vía HTTP (`client.get("/health")`, `client.get("/api/metrics")`, etc.).
- Ejecución real confirmada en esta sesión: `python3 -m pytest -q` en `backend/` → 16 tests pasan (`test_generate_mock_movements_returns_full_year_sorted_data`, `test_filter_movements_by_date_includes_range_edges`, `test_health_endpoint_returns_ok`, `test_metrics_endpoint_respects_date_filters`, `test_b2b_endpoint_only_returns_b2b_records`, `test_b2b_endpoint_combines_new_filters`, `test_metrics_facets_returns_filter_options_and_date_range`, `test_metrics_summary_by_month_returns_balances`, `test_metrics_summary_by_week_honors_business_type_filter`, `test_top_categories_returns_limited_sorted_categories`, `test_metrics_comparison_returns_delta_fields`, `test_metrics_alerts_returns_anomaly_candidates`, `test_build_metrics_facets_raises_404_for_empty_movements`, entre otros).

## Justificación
Renombrar o mover estas funciones sin actualizar los imports de `test_routes.py` rompe la suite completa aunque el comportamiento HTTP no haya cambiado, porque el archivo falla en el paso de `import` antes de ejecutar ningún test.

## Instrucciones para futuros agentes
- Antes de renombrar `generate_mock_movements`, `filter_movements_by_date` o `build_metrics_facets`, hacer `grep` en `backend/tests/` para localizar todos los usos.
- Ejecutar `python3 -m pytest -q` desde `backend/` después de cualquier cambio en `routes.py` para confirmar que la suite sigue en verde.

## Qué NO hacer
- No asumir que los tests solo verifican HTTP; varios (`test_generate_mock_movements_returns_full_year_sorted_data`, `test_filter_movements_by_date_includes_range_edges`, `test_build_metrics_facets_raises_404_for_empty_movements`) llaman funciones internas directamente, no solo endpoints.
- No eliminar `backend/requirements.txt` → `pytest`/`httpx` asumiendo que no se usan en CI; son la única forma de correr esta suite (no hay CI configurado, por lo que la ejecución local es la única validación existente).
