# Contratos TypeScript para las funcionalidades del PM

Especificación de tipos para las peticiones y respuestas de las tres funcionalidades descritas en [`specs/api-evidence.md`](./api-evidence.md).

Este documento **no crea ni modifica código del proyecto**. Las interfaces siguientes son el contrato propuesto para una futura implementación en `frontend/src/lib/financial-types.ts` o en una capa de API.

## Convenciones

- Las fechas se representan como `string` y deben serializarse en formato ISO `YYYY-MM-DD`, porque el backend las publica como `string` con formato OpenAPI `date`.
- Los valores numéricos del backend se representan como `number`.
- Los parámetros opcionales se marcan con `?` y deben omitirse de la URL cuando no tengan valor.
- `delta_pct` admite explícitamente `null`; no debe convertirse automáticamente en `0`.
- Los nombres de propiedades de respuestas conservan exactamente los nombres publicados por la API.

## Tipos compartidos

```ts
export type OperationType = 'income' | 'outcome'

export type Category =
  | 'suppliers'
  | 'sales'
  | 'operational'
  | 'administrative'
  | 'others'

export type BusinessType = 'B2B' | 'B2C'

export type AlertGroupBy = 'day' | 'week' | 'month'

export type ISODate = string
```

### Notas sobre tipos compartidos

- `OperationType`, `Category` y `BusinessType` ya existen en [`frontend/src/lib/financial-types.ts`](../frontend/src/lib/financial-types.ts) y coinciden con los enums confirmados por OpenAPI.
- `AlertGroupBy` no existe actualmente en el frontend; corresponde al parámetro `group_by` de `/api/metrics/alerts`.
- `ISODate` es un alias de documentación. TypeScript no valida por sí solo que una cadena tenga formato `YYYY-MM-DD`.

## 1. Top categories

Endpoint: `GET /api/metrics/categories/top`

### Petición

```ts
export interface TopCategoriesRequest {
  operation_type?: OperationType
  limit?: number
  start_date?: ISODate
  end_date?: ISODate
  business_type?: BusinessType
}
```

### Restricciones de la petición

| Campo | Presencia | Restricción |
|---|---|---|
| `operation_type` | Opcional | `'income'` o `'outcome'`; default backend: `'outcome'`. |
| `limit` | Opcional | Entero entre `1` y `20`; default backend: `5`. |
| `start_date` | Opcional | Fecha `YYYY-MM-DD`; filtro inclusivo según backend. |
| `end_date` | Opcional | Fecha `YYYY-MM-DD`; filtro inclusivo según backend. |
| `business_type` | Opcional | `'B2B'` o `'B2C'`. |

TypeScript no expresa por sí solo que `limit` sea entero ni sus límites. La capa de petición debe validar estas restricciones o manejar la respuesta `422` del backend.

### Respuesta

```ts
export interface TopCategoryItem {
  category: Category
  operation_type: OperationType
  total_amount: number
}

export type TopCategoriesResponse = TopCategoryItem[]
```

### Garantías y límites del contrato

- La respuesta exitosa es siempre un array según OpenAPI.
- El array puede estar vacío.
- El array puede contener menos elementos que `limit`.
- OpenAPI no garantiza el orden descendente por `total_amount`, aunque la implementación actual del backend lo devuelve ordenado así.

## 2. Period comparison

Endpoint: `GET /api/metrics/comparison`

### Petición

```ts
export interface PeriodComparisonRequest {
  start_date: ISODate
  end_date: ISODate
  business_type?: BusinessType
}
```

### Restricciones de la petición

| Campo | Presencia | Restricción |
|---|---|---|
| `start_date` | Obligatorio | Fecha `YYYY-MM-DD`. |
| `end_date` | Obligatorio | Fecha `YYYY-MM-DD`. |
| `business_type` | Opcional | `'B2B'` o `'B2C'`. |

No existe un valor por defecto para `start_date` ni `end_date`. Omitir cualquiera de ellos produce un error de validación `422`.

### Respuesta

```ts
export interface MetricsComparison {
  current_period: number
  previous_period: number
  delta_abs: number
  delta_pct: number | null
}

type PeriodComparisonResponse = MetricsComparison
```

### Significado de los campos

| Campo | Tipo | Significado confirmado |
|---|---|---|
| `current_period` | `number` | Neto del rango solicitado. |
| `previous_period` | `number` | Neto del periodo anterior equivalente, según la lógica actual del backend. |
| `delta_abs` | `number` | Diferencia absoluta entre el periodo actual y el anterior. |
| `delta_pct` | `number \| null` | Variación relativa; puede ser `null` cuando el periodo anterior es `0`. |

La unidad visual de `delta_pct` (porcentaje ya multiplicado por 100 frente a ratio decimal) no queda definida por OpenAPI y debe acordarse antes de implementar el formateo de UI.

## 3. Expense alerts

Endpoint: `GET /api/metrics/alerts`

### Petición

```ts
export interface ExpenseAlertsRequest {
  threshold?: number
  group_by?: AlertGroupBy
  start_date?: ISODate
  end_date?: ISODate
  business_type?: BusinessType
}
```

### Restricciones de la petición

| Campo | Presencia | Restricción |
|---|---|---|
| `threshold` | Opcional | Número mayor o igual que `0`; default backend: `0.3`. |
| `group_by` | Opcional | `'day'`, `'week'` o `'month'`; default backend: `'month'`. |
| `start_date` | Opcional | Fecha `YYYY-MM-DD`. |
| `end_date` | Opcional | Fecha `YYYY-MM-DD`. |
| `business_type` | Opcional | `'B2B'` o `'B2C'`. |

TypeScript no expresa por sí solo que `threshold` sea mayor o igual que `0`; la capa de petición debe validarlo o manejar `422`.

### Respuesta

```ts
export interface MetricsAlert {
  period: string
  outcome_total: number
  baseline_average: number
  increase_ratio: number
}

export type ExpenseAlertsResponse = MetricsAlert[]
```

### Garantías y límites del contrato

- La respuesta exitosa es siempre un array según OpenAPI.
- Un array vacío es válido; OpenAPI no distingue si significa que no hubo movimientos o que no se superó el umbral.
- OpenAPI no define la unidad de `increase_ratio`. La implementación actual lo devuelve como ratio decimal; por ejemplo, `0.7353` representa un incremento de `73.53%` si se muestra como porcentaje.
- OpenAPI no define el significado o fórmula de `baseline_average`; esa semántica depende del backend actual.

## Contrato de serialización de query params

La capa de API debería convertir las interfaces de petición a query params sin enviar campos `undefined`:

```ts
// Ejemplos conceptuales de serialización; no son código de implementación.
TopCategoriesRequest -> /api/metrics/categories/top?operation_type=outcome&limit=5
PeriodComparisonRequest -> /api/metrics/comparison?start_date=2026-06-01&end_date=2026-08-31
ExpenseAlertsRequest -> /api/metrics/alerts?threshold=0.3&group_by=month
```

Reglas:

- ✅ Usar los nombres snake_case exactos del backend: `operation_type`, `start_date`, `end_date`, `business_type`, `group_by`.
- ✅ Codificar los valores de fecha como `YYYY-MM-DD`.
- ✅ Enviar siempre `start_date` y `end_date` para `PeriodComparisonRequest`.
- ❌ No enviar `null` como texto (`"null"`) en query params opcionales.
- ❌ No asumir que `limit` garantiza esa cantidad de elementos en la respuesta.
- ❓ No transformar `delta_pct` ni `increase_ratio` a formato visual dentro de los tipos de datos; esa decisión pertenece a la presentación y requiere confirmar sus unidades.

## Errores esperados

El OpenAPI inspeccionado permite afirmar lo siguiente:

- `422 Unprocessable Entity`: parámetros ausentes o inválidos, incluyendo fechas requeridas faltantes, `limit` fuera de `1..20` o `threshold < 0`.
- `200 OK`: respuesta que cumple los contratos anteriores.

No se especifica aquí una interfaz de error porque el contrato de errores de estas tres rutas no define un schema de dominio estable para el frontend en `api-evidence.md`.
