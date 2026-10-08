# Spec: `DashboardHeader`

Fuente: [../src/components/dashboard/dashboard-header.tsx](../src/components/dashboard/dashboard-header.tsx)

## Props

| Prop | Tipo | Requerido | Default |
|---|---|---|---|
| `period` | `string` | No | `'2024 — Full Year'` |

## Comportamiento

- Renderiza un `<header>` con layout responsive: columna en móvil (`flex-col`), fila con `justify-between` desde `sm`.
- Lado izquierdo: ícono `LayoutDashboard` (lucide-react, `size={18}`) dentro de un círculo con fondo `bg-primary/10`, seguido de título fijo `"Financial Overview"` y subtítulo fijo `"Executive metrics dashboard"`.
- Lado derecho: badge tipo píldora (`rounded-full`) que muestra el valor de `period` tal cual se recibe (sin formateo ni validación).
- No tiene estado interno, no dispara eventos, no tiene variante de `loading`.

## Uso actual

- `App.tsx` lo invoca con `period="2024 - Full Year"` (nótese guion simple `-`, distinto del em-dash `—` del default), ver [app-dashboard.md](./app-dashboard.md).
