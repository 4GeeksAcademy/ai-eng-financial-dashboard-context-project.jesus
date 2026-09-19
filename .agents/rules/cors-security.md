# CORS abierto (`allow_origins=["*"]`) es una configuración de desarrollo, no de producción

## Alcance
Aplica a cualquier cambio en `backend/app/main.py` relacionado con `CORSMiddleware` o a decisiones de despliegue del backend.

## Evidencia
- `backend/app/main.py`: `app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])`.
- No hay variables de entorno ni configuración condicional (`if ENV == "production"`) que restrinja `allow_origins` en ningún archivo del backend.

## Justificación
`allow_origins=["*"]` combinado con `allow_credentials=True` es una combinación que los navegadores y las especificaciones CORS/OWASP consideran insegura si se expone con datos reales o autenticación, ya que permite que cualquier origen envíe credenciales. Actualmente es aceptable porque el backend solo sirve datos mock sin autenticación, pero no hay ninguna salvaguarda que impida desplegar esta configuración tal cual a un entorno con datos reales.

## Instrucciones para futuros agentes
- Si se agrega autenticación o datos reales al backend, restringir `allow_origins` a una lista explícita de orígenes permitidos antes de desplegar fuera de un entorno de desarrollo local/Codespaces.
- Documentar en `backend/app/main.py` (comentario breve) si esta configuración se mantiene intencionalmente abierta para un entorno específico.

## Qué NO hacer
- No copiar esta configuración de CORS a un entorno de producción sin revisarla explícitamente.
- No asumir que `allow_credentials=True` es seguro solo porque `allow_origins=["*"]` ya estaba así en el repo original.
