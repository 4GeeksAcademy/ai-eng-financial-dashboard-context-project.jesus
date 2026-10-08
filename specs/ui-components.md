# Arquitectura de componentes UI para las Funcionalidades 1, 2 y 3

Especificación de arquitectura para las tres funcionalidades descritas en [`api-evidence.md`](./api-evidence.md) y los contratos de datos de [`contracts.md`](./contracts.md).

Este documento define componentes, props, estados de interfaz, validaciones y comportamiento de filtros. **No crea ni modifica código del proyecto.**

## Funcionalidades

| Funcionalidad | Endpoint | Componente raíz propuesto |
|---|---|---|
| 1. Top categories | `GET /api/metrics/categories/top` | `TopCategoriesCard` |
| 2. Period comparison | `GET /api/metrics/comparison` | `PeriodComparisonCard` |
| 3. Expense alerts | `GET /api/metrics/alerts` | `ExpenseAlertsCard` |

## Arquitectura común

```text
DashboardFeaturesSection
├── DateRangeFilter
├── TopCategoriesCard
├── PeriodComparisonCard
└── ExpenseAlertsCard
```

### `DashboardFeaturesSection`

Componente orquestador propuesto para coordinar el rango de fechas, las peticiones y los estados compartidos de las tres funcionalidades.

#### Props

```ts
interface DashboardFeaturesSectionProps {
  initialStartDate?: ISODate
  initialEndDate?: ISODate
  businessType?: BusinessType
  operationType?: OperationType
  topCategoriesLimit?: number
  alertThreshold?: number
  alertGroupBy?: AlertGroupBy
}
```

#### Responsabilidades

- Mantener el rango de fechas seleccionado.
- Validar el rango antes de lanzar peticiones.
- Aplicar el mismo rango a `TopCategoriesCard` y `ExpenseAlertsCard`.
- Aplicar el rango obligatoriamente a `PeriodComparisonCard`, porque su API requiere `start_date` y `end_date`.
- Mantener estados de carga y error independientes por funcionalidad para que una respuesta fallida no oculte las otras tarjetas.
- Cancelar o ignorar respuestas obsoletas cuando el usuario aplica un nuevo filtro antes de que termine la petición anterior.
- No calcular en el frontend los valores agregados de las respuestas; la agregación es responsabilidad del backend.

## Componente transversal: `DateRangeFilter`

Selector compartido de fechas para las tres funcionalidades.

### Props

```ts
interface DateRangeFilterProps {
  startDate?: ISODate
  endDate?: ISODate
  onApply: (range: DateRange) => void
  onClear?: () => void
  disabled?: boolean
  required?: boolean
}

interface DateRange {
  startDate?: ISODate
  endDate?: ISODate
}
```

### Elementos de UI

- Campo `startDate` con input de fecha.
- Campo `endDate` con input de fecha.
- Botón `Apply`.
- Botón `Clear` opcional.
- Mensaje de validación asociado a cada campo y al rango completo.

### Reglas de validación

| Regla | Estado | Resultado |
|---|---:|---|
| Fecha con formato ISO `YYYY-MM-DD` | ✅ | Requisito de serialización del backend. El control de fecha debe producir este formato. |
| `startDate` no puede ser posterior a `endDate` | ✅ | No permite aplicar; muestra `Start date must be on or before end date`. |
| `startDate` y `endDate` para comparación | ✅ | Ambos son obligatorios antes de solicitar `/api/metrics/comparison`. |
| Fechas para top categories | ✅ | Ambas son opcionales; si solo se introduce una, se aplica únicamente ese límite. |
| Fechas para alerts | ✅ | Ambas son opcionales; si solo se introduce una, se aplica únicamente ese límite. |
| Fecha fuera del rango de datos | ❓ | El backend puede responder una lista vacía, pero no existe un error específico de rango fuera de datos. La UI debe mostrar empty state, no asumir que es un error de red. |
| Fecha inválida enviada al backend | ✅ | No debe ocurrir desde la UI; si ocurre, tratar `422` como error de validación y conservar los valores editados. |

### Comportamiento al aplicar filtros

1. El usuario edita las fechas sin disparar peticiones por cada pulsación.
2. `onApply` solo se ejecuta si el rango es válido.
3. Al aplicar:
   - Se normalizan las fechas al formato `YYYY-MM-DD`.
   - Se actualiza el rango activo.
   - Se muestran estados `loading` en las tarjetas afectadas.
   - Se envían `start_date` y/o `end_date` únicamente cuando tienen valor.
4. Si el usuario modifica los campos después de aplicar, el rango activo no cambia hasta pulsar `Apply` otra vez.
5. `Clear` elimina el rango opcional de top categories y alerts, pero no puede ejecutar una comparación sin un rango; para comparison debe restaurar un rango inicial válido o dejar la tarjeta en estado `needs-range`.
6. Si se aplica un nuevo rango durante una petición, la respuesta anterior no debe sobrescribir los datos del rango nuevo.

## Funcionalidad 1: `TopCategoriesCard`

Endpoint: `GET /api/metrics/categories/top`.

### Props

```ts
interface TopCategoriesCardProps {
  data: TopCategoryItem[]
  loading?: boolean
  error?: string | null
  operationType?: OperationType
  limit?: number
  startDate?: ISODate
  endDate?: ISODate
  businessType?: BusinessType
  onRetry?: () => void
}
```

### Presentación

- Renderiza una tarjeta con título `Top categories`.
- Cada fila muestra `category`, `total_amount` formateado como moneda y el tipo de operación cuando sea necesario para contexto.
- El orden recibido del backend debe conservarse; el componente no debe volver a ordenar ni recalcular los totales.
- `limit` controla la cantidad solicitada, pero la UI no debe renderizar filas ficticias para completar el límite.

### Validación de props/filtros

- `operationType`, si está presente, solo puede ser `income` u `outcome`.
- `limit` debe ser entero entre `1` y `20`; si no es válido, no se realiza la petición.
- `businessType`, si está presente, solo puede ser `B2B` o `B2C`.
- `startDate` y `endDate` son opcionales, pero si ambos están presentes `startDate <= endDate`.
- La tarjeta debe tratar los errores `422` como errores de parámetros, no como ausencia de datos.

### Empty states

1. **Sin resultados:** `data.length === 0` y no hay error.
   - Mensaje: `No categories available for the selected filters.`
   - No muestra barras, filas placeholder ni un valor `0` inventado.
2. **Cargando:** `loading === true`.
   - Muestra skeleton de título y filas.
   - No muestra el empty state simultáneamente.
3. **Error:** `error` presente.
   - Muestra `Unable to load top categories.` y `onRetry` si existe.
4. **Menos resultados que `limit`:** es un resultado válido; muestra solo las categorías devueltas.

### Filtros de fecha

- Al aplicar un rango válido, solicita el endpoint con `start_date` y/o `end_date`.
- El backend aplica los límites de fecha de forma inclusiva.
- Si se limpia el rango, vuelve a solicitar sin esos parámetros y muestra los resultados globales.
- El cambio de fechas no debe alterar `operationType`, `limit` ni `businessType` salvo que el usuario los cambie explícitamente.

## Funcionalidad 2: `PeriodComparisonCard`

Endpoint: `GET /api/metrics/comparison`.

### Props

```ts
interface PeriodComparisonCardProps {
  data: MetricsComparison | null
  loading?: boolean
  error?: string | null
  startDate?: ISODate
  endDate?: ISODate
  businessType?: BusinessType
  onRetry?: () => void
  onSelectDateRange?: () => void
}
```

### Presentación

- Renderiza `current_period`, `previous_period`, `delta_abs` y `delta_pct`.
- Los importes monetarios se formatean con la utilidad monetaria existente.
- `delta_abs` debe mostrar signo positivo o negativo.
- `delta_pct === null` se presenta como `N/A` o `Not available`; nunca como `0%`, `NaN%` o una cadena vacía.
- La tarjeta no calcula el periodo anterior ni transforma los datos recibidos.

### Validación de props/filtros

- `startDate` es obligatorio para solicitar datos.
- `endDate` es obligatorio para solicitar datos.
- Ambas fechas deben ser válidas y cumplir `startDate <= endDate`.
- `businessType`, si está presente, debe ser `B2B` o `B2C`.
- Si falta alguna fecha, la UI no realiza la petición; muestra estado `needs-range`.
- Si el backend devuelve `422`, conserva el rango visible y muestra un mensaje de validación accionable.

### Empty and prerequisite states

1. **Sin rango (`needs-range`):** `data === null`, no hay petición activa y falta una fecha.
   - Mensaje: `Select a start and end date to compare periods.`
   - Puede mostrar `onSelectDateRange` para enfocar el filtro.
2. **Cargando:** muestra skeletons para los cuatro valores.
3. **Respuesta nula tras error:** muestra `Unable to load period comparison.` y opción de reintento.
4. **Datos disponibles:** muestra los cuatro campos, incluyendo `N/A` para `delta_pct: null`.
5. **No existe un empty array:** la respuesta es un objeto; ausencia de datos se representa con `null` y no con `[]`.

### Filtros de fecha

- Al aplicar el rango, siempre envía ambos parámetros: `start_date` y `end_date`.
- El rango activo define el periodo actual; el backend calcula el periodo anterior equivalente.
- La UI no debe enviar un parámetro `previous_start_date` ni `previous_end_date`.
- Si el rango cambia, invalida el resultado anterior y muestra loading hasta recibir la comparación nueva.
- `Clear` deja la tarjeta en `needs-range`; no debe realizar una petición incompleta.

## Funcionalidad 3: `ExpenseAlertsCard`

Endpoint: `GET /api/metrics/alerts`.

### Props

```ts
interface ExpenseAlertsCardProps {
  data: MetricsAlert[]
  loading?: boolean
  error?: string | null
  threshold?: number
  groupBy?: AlertGroupBy
  startDate?: ISODate
  endDate?: ISODate
  businessType?: BusinessType
  onRetry?: () => void
}
```

### Presentación

- Renderiza una lista de alertas con `period`, `outcome_total`, `baseline_average` e `increase_ratio`.
- `outcome_total` y `baseline_average` se formatean como moneda.
- `increase_ratio` se muestra como porcentaje únicamente tras aplicar la conversión acordada para el ratio decimal del backend (`increase_ratio * 100`).
- Cada alerta debe tener una indicación visual de severidad, sin depender únicamente del color.
- No muestra una alerta de prueba ni un valor cero cuando el array está vacío.

### Validación de props/filtros

- `threshold` debe ser un número mayor o igual que `0`; el default del backend es `0.3`.
- `groupBy` solo puede ser `day`, `week` o `month`; el default es `month`.
- `businessType`, si está presente, debe ser `B2B` o `B2C`.
- `startDate` y `endDate` son opcionales, pero si ambos están presentes `startDate <= endDate`.
- Si se muestra `threshold` como porcentaje al usuario, la UI debe convertirlo de manera consistente antes de enviarlo. El valor enviado al backend debe seguir siendo el ratio decimal esperado por el contrato.

### Empty states

1. **Sin alertas:** `data.length === 0` y no hay error.
   - Mensaje: `No unusual expense increases detected for the selected filters.`
   - Es un resultado válido, no un error.
2. **Cargando:** muestra skeleton de varias filas.
3. **Error:** muestra `Unable to load expense alerts.` y `onRetry` si existe.
4. **Alertas disponibles:** muestra una fila por cada elemento recibido.

La UI no debe afirmar que un array vacío significa específicamente "sin movimientos" o "sin anomalías": el contrato no diferencia ambos casos.

### Filtros de fecha

- Al aplicar un rango válido, envía `start_date` y/o `end_date` junto con `threshold`, `group_by` y `business_type` activos.
- El backend agrupa después de filtrar el rango; la UI no debe agrupar ni calcular el baseline localmente.
- Cambiar el rango conserva `threshold`, `groupBy` y `businessType`.
- Al limpiar el rango, vuelve a solicitar el histórico completo usando los filtros no temporales activos.
- Mientras se actualizan los datos, se mantiene la tarjeta en loading y no se presentan alertas del rango anterior como si pertenecieran al nuevo.

## Reglas de integración y errores

- Cada tarjeta debe tener estados independientes `loading`, `success`, `empty`, `needs-range` cuando aplique y `error`.
- Un error de una funcionalidad no debe convertir las otras tarjetas en empty state.
- Los errores `422` deben asociarse a validación de filtros; los errores de red/5xx deben mostrar error de carga y permitir reintento.
- Las respuestas deben validarse antes de renderizar: objeto para comparison y arrays para top categories/alerts.
- No reutilizar `FinancialMovement` ni `MonthlyDataPoint` para estas respuestas; los contratos requieren `TopCategoryItem`, `MetricsComparison` y `MetricsAlert`.
- Las decisiones no definidas por OpenAPI —especialmente la presentación de `delta_pct` e `increase_ratio`— deben confirmarse con producto antes de cerrar la implementación visual.
