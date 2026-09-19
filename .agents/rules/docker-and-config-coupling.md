# Los puertos 5173, 8000 y 5678 están acoplados entre `docker-compose.yml` y los Dockerfiles

## Alcance
Aplica a cualquier cambio de puertos, nombres de servicio o del proxy `/api` del frontend.

## Evidencia
- `docker-compose.yml` mapea `"5173:5173"` (servicio `frontend`) y `"8000:8000"`, `"5678:5678"` (servicio `backend`).
- `backend/Dockerfile`: `EXPOSE 8000 5678` y `CMD [... "--port", "8000" ...]`, `debugpy --listen 0.0.0.0:5678`.
- `frontend/Dockerfile`: `EXPOSE 5173` y `CMD [..., "--port", "5173"]`.
- `frontend/vite.config.ts`: `proxy: {"/api": {target: "http://backend:8000"}}`, donde `backend` es el nombre literal del servicio en `docker-compose.yml`.
- El alias `@/*` está definido por separado en `frontend/tsconfig.app.json` (`"paths": {"@/*": ["./src/*"]}`) y en `frontend/vite.config.ts` (`resolve.alias`).

## Justificación
Ningún archivo de configuración central unifica estos valores; están duplicados literalmente en al menos dos archivos cada uno. Un cambio parcial (solo en `docker-compose.yml` o solo en un Dockerfile) rompe el arranque o el proxy sin ningún error de compilación que lo señale.

## Instrucciones para futuros agentes
- Si se cambia un puerto, actualizarlo simultáneamente en `docker-compose.yml` y en el `CMD`/`EXPOSE` del Dockerfile correspondiente.
- Si se renombra el servicio `backend` en `docker-compose.yml`, actualizar también el `target` del proxy en `frontend/vite.config.ts` en el mismo cambio.
- Si se modifica el alias `@/*`, aplicar el cambio tanto en `frontend/tsconfig.app.json` como en `frontend/vite.config.ts`.

## Qué NO hacer
- No cambiar el nombre del servicio `backend` en `docker-compose.yml` sin buscar (`grep -r "http://backend"`) todas sus referencias en `frontend/`.
- No modificar únicamente `tsconfig.app.json` o únicamente `vite.config.ts` para el alias `@/*`; deben mantenerse sincronizados manualmente porque no comparten una fuente única.
