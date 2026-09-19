# Todo endpoint de negocio nuevo va bajo `/api/metrics...` y debe declarar `response_model`

## Alcance
Aplica a la adición de nuevos endpoints en `backend/app/routes.py`.

## Evidencia
- Los 8 endpoints de negocio existentes siguen el prefijo `/api/metrics`: `/api/metrics`, `/api/metrics/facets`, `/api/metrics/summary`, `/api/metrics/categories/top`, `/api/metrics/comparison`, `/api/metrics/alerts`, `/api/metrics/b2b`, `/api/metrics/b2c`.
- La única excepción es `/health`, sin prefijo, con fines de healthcheck.
- Cada uno de esos 8 endpoints declara `response_model=...` explícito en el decorador `@router.get(...)`.
- `frontend/vite.config.ts` configura el proxy de desarrollo únicamente para el path `/api`: `proxy: {"/api": {target: "http://backend:8000"}}`.

## Justificación
El proxy de Vite solo redirige rutas que empiecen con `/api`; un endpoint fuera de ese prefijo no sería alcanzable desde el frontend en desarrollo sin modificar `vite.config.ts`. `response_model` además habilita la documentación automática en `/docs` (Swagger UI, activo por defecto ya que `backend/app/main.py` no pasa `docs_url=None`).

## Instrucciones para futuros agentes
- Nombrar cualquier endpoint de negocio nuevo bajo `/api/metrics/<recurso>`.
- Declarar siempre `response_model` con una clase Pydantic existente o nueva, replicando el patrón de `MetricsSummaryItem`, `TopCategoryItem`, etc.

## Qué NO hacer
- No crear endpoints sin prefijo `/api` salvo que se actualice también `frontend/vite.config.ts`.
- No omitir `response_model` — ningún endpoint existente en el repo lo omite.
