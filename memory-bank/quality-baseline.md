# Línea base de calidad

## Alcance

Esta línea base reúne los criterios aplicados al frontend del dashboard después de las auditorías de accesibilidad y de prácticas React/Vercel. El proyecto es una SPA de React 19 + TypeScript + Vite 8; no es una aplicación Next.js.

## Skills aplicadas

- **`accessibility` (skill interna):** revisión de semántica HTML, nombres accesibles, iconos, estados de carga y error, navegación por teclado, foco, contraste y alternativas para gráficos.
- **`vercel-react-best-practices` (skill comunitaria):** revisión de Core Web Vitals, tamaño del bundle, estabilidad del layout (CLS), carga de recursos, SEO y metadatos sociales.

Los nombres anteriores describen las prácticas aplicadas en esta auditoría. En el estado documentado del repositorio no existe todavía `.agents/skills/`; solo están versionadas las reglas de `.agents/rules/`. Si las skills se incorporan al repositorio, sus archivos y alcance deben quedar registrados aquí.

## Baseline frontend

- El build obligatorio es `npm run build`, que ejecuta `tsc -b && vite build`.
- La validación ejecutada con `npm ci && npm run build` terminó correctamente.
- El build produjo una advertencia de bundle JavaScript superior a 500 kB; Recharts forma parte de la carga inicial y queda como deuda de rendimiento.
- Los gráficos mantienen una altura fija de `280px` y los skeletons reservan dimensiones, lo que reduce el riesgo de CLS.
- Deben conservarse dimensiones estables para gráficos, tarjetas y cualquier imagen futura.
- No se usan `next/image` ni `next/font`: el proyecto no usa Next.js. Las imágenes futuras deben declarar dimensiones o una relación de aspecto estable.
- La SPA usa `frontend/index.html` como punto único de metadatos. Debe mantener título descriptivo, idioma correcto, descripción y metadatos OpenGraph/Twitter.

## Baseline de accesibilidad

- Los iconos decorativos deben marcarse con `aria-hidden="true"` y no sustituir texto visible.
- Las regiones de KPI y gráficos deben tener nombres accesibles relacionados con sus encabezados.
- Los errores deben exponerse mediante `role="alert"` y los estados de carga mediante `aria-busy`/`role="status"` cuando corresponda.
- Los gráficos deben ofrecer una alternativa textual o tabular; la visualización por sí sola no es suficiente.
- Los controles interactivos deben tener un indicador `:focus-visible` claro y navegable con teclado.
- Los colores de texto normal deben alcanzar al menos 4.5:1; los textos grandes y elementos gráficos, al menos 3:1, medidos contra sus fondos reales.
- No hay elementos `<img>` actualmente; el favicon no sustituye contenido informativo.

## Gaps conocidos

- No existe automatización con axe/Lighthouse ni tests de componentes React.
- No se ha hecho una medición de campo de Core Web Vitals; las observaciones de LCP, INP y CLS son estáticas.
- El mensaje de error puede insertar contenido antes de los KPI y provocar desplazamiento vertical.
- Los metadatos actuales del documento siguen siendo mínimos y deben mejorarse antes de considerar SEO completo.
- No existe CI/CD que ejecute build, lint, tests o auditorías de accesibilidad automáticamente.
