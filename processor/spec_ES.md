# Especificación del Pre-Procesador

**Propósito:**  
El módulo `pre-processor.py` valida los datos entrantes de los lotes contra parámetros de almacenamiento específicos por material y calcula métricas de riesgo antes de la evaluación basada en IA en el Sistema de Alertas de Calidad y Riesgo de Vencimiento.

---

## Tabla de Contenidos
1. [Descripción General](#descripción-general)  
2. [Dependencias](#dependencias)  
3. [Funciones Principales](#funciones-principales)  
   - [`calculate_temperature_deviation`](#calculate_temperature_deviation)  
   - [`calculate_humidity_deviation`](#calculate_humidity_deviation)  
   - [`calculate_storage_deviation`](#calculate_storage_deviation)  
   - [`process_batch`](#process_batch)  
4. [Parámetros de Configuración](#parámetros-de-configuración)  
5. [Estrategia de Pruebas](#estrategia-de-pruebas)  
6. [Ejemplo de Uso](#ejemplo-de-uso)  
7. [Extensibilidad](#extensibilidad)  

---

## Descripción General
`pre-processor.py` actúa como la capa de validación de datos para el flujo de riesgo de deterioro. Recibe un registro de lote (generalmente producido por `simulators/batch_simulator.py`), evalúa las condiciones de almacenamiento de cada material contra límites predefinidos, y produce una salida estructurada con métricas de desviación. Estas métricas son consumidas por el agente de IA de riesgo para determinar los niveles de alerta.

El módulo está diseñado para ejecutarse dentro de un nodo **Function** de n8n, donde procesa un lote por invocación y retorna un diccionario compatible con JSON.

---

## Dependencias
El módulo utiliza solo características estándar de Python:
- `typing` – para sugerencias de tipo y documentación del esquema
- `json` – para compatibilidad de serialización (opcional, cuando se usa fuera de n8n)

No se requieren paquetes externos o llamadas a red, garantizando una ejecución ligera y portátil.

---

## Funciones Principales

### `calculate_temperature_deviation`

```python
def calculate_temperature_deviation(actual: float, minimum: float, maximum: float) -> float:
    """
    Calcula qué tan lejos se desvía la temperatura real del rango aceptable.

    Parámetros:
        actual: Temperatura medida del contenedor.
        minimum: Límite inferior de temperatura aceptable.
        maximum: Límite superior de temperatura aceptable.

    Retorna:
        float: Valor negativo si está por debajo del mínimo, positivo si está por encima del máximo, 0 si está dentro del rango.
    """
```

**Comportamientos Clave:**
- Retorna un valor negativo si `actual` está por debajo de `minimum`.
- Retorna un valor positivo si `actual` está por encima de `maximum`.
- Retorna `0` si la temperatura está dentro del rango aceptable.

---

### `calculate_humidity_deviation`

```python
def calculate_humidity_deviation(actual: float, maximum: float) -> float:
    """
    Calcula qué tan lejos la humedad real excede el valor máximo permitido.

    Parámetros:
        actual: Humedad relativa medida.
        maximum: Nivel máximo de humedad aceptable.

    Retorna:
        float: Desviación positiva si la humedad excede el máximo, de lo contrario 0.
    """
```

**Comportamientos Clave:**
- Solo se consideran violaciones del límite superior (no hay límite inferior para humedad).
- Retorna `0` si la humedad está en o por debajo del máximo.

---

### `calculate_storage_deviation`

```python
def calculate_storage_deviation(actual: int, maximum: int | None) -> int:
    """
    Calcula qué tan lejos la duración real de almacenamiento excede los días máximos permitidos.

    Parámetros:
        actual: Número de días que el material ha sido almacenado.
        maximum: Días máximos permitidos de almacenamiento (None = ilimitado).

    Retorna:
        int: Desviación positiva si el almacenamiento excede el máximo, de lo contrario 0.
    """
```

**Comportamientos Clave:**
- Retorna `0` si `maximum` es `None` (vida útil ilimitada).
- Retorna `0` si `actual` está dentro del rango permitido.
- Retorna una desviación positiva si la duración del almacenamiento excede el límite.

---

### `process_batch`

```python
def process_batch(batch: dict) -> dict:
    """
    Valida un solo lote contra los límites de materiales y calcula métricas de riesgo.

    Parámetros:
        batch: Diccionario que contiene batch_id, timestamp, temperatura, humedad y lista de materiales.

    Retorna:
        dict: Diccionario estructurado con materiales procesados e indicadores de riesgo agregados.
    """
```

**Comportamientos Clave:**
- Itera sobre cada material en el lote.
- Busca los límites aceptables desde `MATERIAL_LIMITS`.
- Calcula desviaciones de temperatura, humedad y almacenamiento para cada material.
- Rastrea la desviación total y el conteo de materiales fuera de especificación.
- Retorna un diccionario estructurado que contiene:
  - `batch_id` y `timestamp` (pasados del input)
  - Resumen `container` con desviación total y conteo de fuera de especificación
  - Lista `materials` con detalles de desviación por material

---

## Parámetros de Configuración

| Parámetro | Descripción | Valor de Ejemplo |
|-----------|-------------|------------------|
| `MATERIAL_LIMITS` | Diccionario que mapea nombres de materiales a sus parámetros de almacenamiento aceptables. | Ver abajo |
| `temperature.min` / `temperature.max` | Rango de temperatura aceptable en Celsius para un material dado. | `10` / `20` para harina |
| `humidity_max` | Humedad relativa máxima aceptable en porcentaje. | `80` para harina |
| `storage_max_days` | Duración máxima permitida de almacenamiento en días (`None` = ilimitado). | `365` para harina |

**Ejemplo de definición de `MATERIAL_LIMITS`:**
```python
MATERIAL_LIMITS = {
    "flour": {
        "temperature": {"min": 10, "max": 20},
        "humidity_max": 80,
        "storage_max_days": 365
    },
    "sugar": {
        "temperature": {"min": 15, "max": 25},
        "humidity_max": 65,
        "storage_max_days": None
    },
    "yeast": {
        "temperature": {"min": 15, "max": 25},
        "humidity_max": 60,
        "storage_max_days": 730
    },
    # Materiales adicionales según necesidad...
}
```

---

## Estrategia de Pruebas

1. **Pruebas Unitarias**
   - Verificar que los cálculos de desviación retornan valores correctos para entradas dentro del rango, por debajo del mínimo y por encima del máximo.
   - Confirmar que `calculate_storage_deviation` maneja `None` como máximo correctamente.
   - Validar que `process_batch` cuenta correctamente los materiales fuera de especificación.

2. **Pruebas de Integración**
   - Alimentar lotes simulados (desde `simulators/batch_simulator.py`) a `process_batch`.
   - Confirmar que la estructura de salida coincide con el esquema esperado.
   - Validar que `total_deviation` refleja la suma de todas las desviaciones individuales.

3. **Escenarios Edge-Case**
   - Probar lotes con cero materiales.
   - Probar con materiales no presentes en `MATERIAL_LIMITS` (debería lanzar `KeyError`).
   - Probar con valores extremos de temperatura/humedad.
   - Probar con `storage_max_days` establecido a `None`.

---

## Ejemplo de Uso

```python
from pre_processor import process_batch

batch = {
    "batch_id": "BATCH-001",
    "timestamp": "2026-07-23T12:00:00Z",
    "temperature": 22,
    "humidity": 75,
    "materials": [
        {"name": "flour", "storage_days": 100},
        {"name": "yeast", "storage_days": 800}
    ]
}

result = process_batch(batch)
print(result)
```

**Salida de Ejemplo:**
```json
{
  "batch_id": "BATCH-001",
  "timestamp": "2026-07-23T12:00:00Z",
  "container": {
    "temperature": 22,
    "humidity": 75,
    "materials_out_of_spec": 1,
    "total_deviation": 72.0
  },
  "materials": [
    {
      "name": "flour",
      "storage_days": 100,
      "expected_storage_days": 365,
      "storage_days_deviation": 0,
      "expected_temperature": {"min": 10, "max": 20},
      "temperature_deviation": 2,
      "humidity": 75,
      "expected_humidity_max": 80,
      "humidity_deviation": 0
    },
    {
      "name": "yeast",
      "storage_days": 800,
      "expected_storage_days": 730,
      "storage_days_deviation": 70,
      "expected_temperature": {"min": 15, "max": 25},
      "temperature_deviation": 0,
      "humidity": 75,
      "expected_humidity_max": 60,
      "humidity_deviation": 15
    }
  ]
}
```

---

## Extensibilidad

Mejoras futuras pueden incluir:
- Agregar umbrales de advertencia (ej. 10% desviación = alerta amarilla).
- Soporte para detección de similitud entre lotes para correlación de anomalías.
- Implementación de cálculos de fecha de vencimiento basados en la fecha actual.
- Agregar soporte para perfiles de restricción de materiales personalizados.
- Integrar con feeds de datos de sensores en tiempo real para validación en vivo.

Este diseño asegura que el pre-procesador se mantenga ligero mientras proporciona una base robusta para alertas basadas en riesgo.

---

*Documento generado el 23 de julio de 2026 por el equipo de desarrollo del Sistema de Alertas de Calidad y Riesgo de Vencimiento.*