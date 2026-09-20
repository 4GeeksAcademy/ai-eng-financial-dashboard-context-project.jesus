# Evidencia API para las 3 funcionalidades del PM

Fecha de exploración: 2026-09-19.

## Fuente y alcance

- ✅ `GET http://localhost:8000/docs` respondió `200` y expone Swagger UI.
- ✅ `GET http://localhost:8000/openapi.json` respondió `200`.
- ✅ El documento OpenAPI activo declara versión `3.1.0`.
- ✅ La evidencia de contratos de este documento proviene del OpenAPI generado por el backend en ejecución, no solo de una lectura estática del código.
- ❓ Los tres endpoints existen en el backend, pero no son consumidos actualmente por ningún archivo bajo `frontend/src/` (búsqueda sin coincidencias para `categories/top`, `comparison`, `alerts` ni sus tipos de respuesta).

## Tipos actuales del frontend

Fuente: [frontend/src/lib/financial-types.ts](../frontend/src/lib/financial-types.ts).

- ✅ Existe `OperationType = 'income' | 'outcome'`; coincide con el enum OpenAPI usado por top categories.
- ✅ Existe `Category = 'suppliers' | 'sales' | 'operational' | 'administrative' | 'others'`; coincide con el enum OpenAPI usado por top categories.
- ✅ Existe `BusinessType = 'B2B' | 'B2C'`; coincide con el filtro opcional de los tres endpoints.
- ❌ No existe `TopCategoryItem` en el frontend.
- ❌ No existe `MetricsComparison` en el frontend.
- ❌ No existe `MetricsAlert` en el frontend.
- ❓ `FinancialMovement` y `MonthlyDataPoint` existentes no representan directamente ninguna de las tres respuestas nuevas; no deben reutilizarse como tipos de respuesta.
- ❓ El frontend representa fechas como `string`, mientras OpenAPI las publica como `string` con formato `date`; hay que conservar el formato ISO `YYYY-MM-DD` al construir query params.

## 1. Top categories

Endpoint requerido: `GET /api/metrics/categories/top`.

### Query params confirmados por OpenAPI

| Campo | Estado | Contrato |
|---|---:|---|
| `operation_type` | ✅ | Opcional; enum `income`/`outcome`; default `outcome`. Coincide con `OperationType`. |
| `limit` | ✅ | Opcional; integer; default `5`; mínimo `1`, máximo `20`. |
| `start_date` | ✅ | Opcional; fecha ISO (`date` en backend). |
| `end_date` | ✅ | Opcional; fecha ISO (`date` en backend). |
| `business_type` | ✅ | Opcional; enum `B2B`/`B2C`. Coincide con `BusinessType`. |

### Respuesta confirmada

- ✅ Respuesta `200`: array de `TopCategoryItem`.
- ✅ Cada elemento requiere `category`, `operation_type` y `total_amount`.
- ✅ `category` usa los cinco valores existentes en el frontend.
- ✅ `operation_type` usa los dos valores existentes en el frontend.
- ✅ `total_amount` es `number`.
- ❌ No existe el tipo TypeScript equivalente en `frontend/src/lib/financial-types.ts`.
- ❓ OpenAPI no expresa que el array está ordenado por `total_amount` descendente ni que puede contener menos elementos que `limit`; esa semántica fue observada en la implementación/respuesta, no queda garantizada por el schema OpenAPI.

Ejemplo explorado: `?operation_type=income&limit=3` devolvió dos elementos, no tres, porque solo había dos categorías de ingreso disponibles.

## 2. Period comparison

Endpoint requerido: `GET /api/metrics/comparison`.

### Query params confirmados por OpenAPI

| Campo | Estado | Contrato |
|---|---:|---|
| `start_date` | ✅ | Obligatorio; `string` con formato `date` en OpenAPI. |
| `end_date` | ✅ | Obligatorio; `string` con formato `date` en OpenAPI. |
| `business_type` | ✅ | Opcional; enum `B2B`/`B2C`. |

- ✅ La ausencia de `start_date` o `end_date` produce `422` por validación (confirmado con una petición al endpoint).
- ✅ Respuesta `200`: objeto `MetricsComparison`.
- ✅ `current_period`, `previous_period` y `delta_abs` son `number` requeridos.
- ✅ `delta_pct` es requerido, pero acepta `number` **o** `null` (`anyOf` en OpenAPI).
- ❌ No existe el tipo TypeScript equivalente en `frontend/src/lib/financial-types.ts`.
- ❓ OpenAPI no documenta que `previous_period` representa el periodo equivalente anterior ni cómo se deriva; esa semántica requiere consultar la lógica del backend.
- ❓ OpenAPI no especifica si `delta_pct` está expresado como porcentaje (por ejemplo `-40.15`) o como ratio; el frontend debe tomar esta decisión con base en el contrato de producto/backend antes de formatearlo.

Ejemplo explorado: `?start_date=2026-06-01&end_date=2026-08-31` devolvió un objeto con las cuatro propiedades esperadas.

## 3. Expense alerts

Endpoint requerido: `GET /api/metrics/alerts`.

### Query params confirmados por OpenAPI

| Campo | Estado | Contrato |
|---|---:|---|
| `threshold` | ✅ | Opcional; `number`; default `0.3`; mínimo `0`. |
| `group_by` | ✅ | Opcional; enum `day`/`week`/`month`; default `month`. |
| `start_date` | ✅ | Opcional; fecha ISO (`date` en backend). |
| `end_date` | ✅ | Opcional; fecha ISO (`date` en backend). |
| `business_type` | ✅ | Opcional; enum `B2B`/`B2C`. |

### Respuesta confirmada

- ✅ Respuesta `200`: array de `MetricsAlert`.
- ✅ Cada elemento requiere `period`, `outcome_total`, `baseline_average` e `increase_ratio`.
- ✅ `period` es `string`.
- ✅ Los otros tres campos son `number`.
- ❌ No existe el tipo TypeScript equivalente en `frontend/src/lib/financial-types.ts`.
- ❓ OpenAPI no indica la unidad de `increase_ratio` (ratio decimal o porcentaje), ni describe cómo se calcula `baseline_average`; no debe interpretarse visualmente sin confirmar esa decisión de producto.
- ❓ OpenAPI no distingue entre un array vacío por ausencia de movimientos y un array vacío porque no se superó el umbral.

Ejemplo explorado: la petición sin parámetros devolvió un array de alertas con periodos mensuales.

## Resumen para implementación frontend

| Funcionalidad | Endpoint | Tipo frontend faltante | Requiere params obligatorios | Estado |
|---|---|---|---|---|
| Top categories | `/api/metrics/categories/top` | `TopCategoryItem` | No | ❌ No implementada en `frontend/src/`. |
| Period comparison | `/api/metrics/comparison` | `MetricsComparison` | `start_date`, `end_date` | ❌ No implementada en `frontend/src/`. |
| Expense alerts | `/api/metrics/alerts` | `MetricsAlert` | No | ❌ No implementada en `frontend/src/`. |

Los enums compartidos (`OperationType`, `Category`, `BusinessType`) sí existen y coinciden; las tres interfaces de respuesta y la lógica de consumo/fetch aún deben añadirse.
