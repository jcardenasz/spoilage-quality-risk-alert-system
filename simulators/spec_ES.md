# Especificación del Simulador de Lotes

**Propósito:**  
El módulo `batch_simulator.py` genera datos de lote simulados que representan materias primas para el Sistema de Alertas de Calidad y Riesgo de Vencimiento. Proporciona mecanismos deterministas pero flexibles para producir instancias realistas de lotes con desviaciones controladas de las condiciones de almacenamiento ideales.

---  

## Tabla de Contenidos
1. [Descripción General](#descripción-general)  
2. [Dependencias](#dependencias)  
3. [Funciones Principales](#funciones-principales)  
   - [`generate_batch`](#generate_batch)  
   - [`_validate_input_params`](#_validate_input_params)  
4. [Parámetros de Configuración](#parámetros-de-configuración)  
5. [Estrategia de Pruebas](#estrategia-de-pruebas)  
6. [Ejemplo de Uso](#ejemplo-de-uso)  
7. [Extensibilidad](#extensibilidad)  

---  

## Descripción General
`batch_simulator.py` es responsable de sintetizar los registros de lote utilizados por la etapa de preprocesamiento (`processor/pre-processor.py`). Cada lote contiene:
- Identificador único y timestamp de generación
- Valores de temperatura y humedad a nivel de contenedor
- Lista de materiales con su duración de almacenamiento
- Metadatos sintéticos utilizados para la evaluación de riesgo por IA downstream

El simulador admite rangos configurables para parámetros clave para permitir pruebas específicas de casos límite y condiciones normales de operación.

---  

## Dependencias
El módulo depende solo de bibliotecas estándar de Python:
- `datetime` – para generar timestamps realistas
- `uuid` – para crear IDs de lote basados en UUID
- `random` – para generación de valores estocásticos dentro de rangos definidos
- `typing` – para sugerencias de tipo y ayudantes de validación

No se requieren fuentes de datos externas, permitiendo operación sin conexión.

---  

## Funciones Principales

### `generate_batch`

```python
def generate_batch(
    *,
    seed: int | None = None,
    material_count: int = 5,
    batch_id: str | None = None,
    base_timestamp: str | None = None,
    min_temp: int = 5,
    max_temp: int = 35,
    min_humidity: int = 10,
    max_humidity: int = 95,
    min_storage_days: int = 1,
    max_storage_days: int = 1825,
    probability_of_out_of_spec: float = 0.3,
) -> dict:
    """
    Genera un lote determinista de lotes de material sintéticos.

    Parámetros:
        seed: Semilla entera opcional para resultados reproducibles.
        material_count: Número de materiales distintos en el lote.
        batch_id: Identificador opcional; si se omite, se generará un UUID.
        base_timestamp: Timestamp ISO 8601 opcional para anclar la generación del lote.
        min_/max_temp/humidity: Límites de rango para las lecturas ambientales generadas.
        min_/max_storage_days: Límites de duración de almacenamiento para materiales generados.
        probability_of_out_of_spec: Probabilidad de que un material exceda los límites de almacenamiento.

    Retorna:
        dict: Un diccionario que coincide con el esquema JSON esperado para entrada de simulación.
    """
```

**Comportamientos Clave:**
- Inicializa una semilla aleatoria si se proporciona para reproducibilidad.
- Selecciona aleatoriamente temperatura, humedad y días de almacenamiento dentro de los rangos configurados.
- Aplica `probability_of_out_of_spec` para asegurar que algunos materiales violen los límites.
- Retorna un diccionario que contiene `batch_id`, `timestamp` y una lista de `materiales`.

### `_validate_input_params`

```python
def _validate_input_params(
    material_count: int,
    min_temp: int,
    max_temp: int,
    min_humidity: int,
    max_humidity: int,
    min_storage_days: int,
    max_storage_days: int,
    probability_of_out_of_spec: float,
) -> None:
    """
    Valida que las entradas numéricas estén dentro de rangos plausibles.
    Lanza:
        ValueError: Si algún parámetro viola las restricciones.
    """
```

**Reglas de Validación:**
- `material_count` debe ser ≥ 1
- `min_temp` < `max_temp`
- `min_humidity` < `max_humidity`
- `min_storage_days` < `max_storage_days`
- `0` ≤ `probability_of_out_of_spec` ≤ 1

---  

## Parámetros de Configuración

| Parámetro | Predeterminado | Descripción |
|-----------|----------------|-------------|
| `material_count` | `5` | Número de entradas de materiales distintos por lote. Ajustar para intensidad de trabajo. |
| `min_temp` / `max_temp` | `5` / `35` | Rango de temperatura en Celsius para el entorno del contenedor. |
| `min_humidity` / `max_humidity` | `10` / `95` | Rango de humedad en porcentaje de humedad relativa. |
| `min_storage_days` / `max_storage_days` | `1` / `1825` (5 años) | Límites de duración de almacenamiento para materiales generados. |
| `probability_of_out_of_spec` | `0.3` | Proporción objetivo de materiales que deben exceder los umbrales permitidos. |
| `seed` | `None` | Semilla para simulación determinista; omitiendo se produce salida no determinista. |

---  

## Estrategia de Pruebas

1. **Pruebas Unitarias**
   - Verificar que `_validate_input_params` lanza `ValueError` en entradas inválidas.
   - Confirmar reproducibilidad cuando se suministra una `seed` fija.
   - Asegurar que las claves (`batch_id`, `timestamp`, `materiales`) siempre existen.

2. **Pruebas de Integración**
   - Alimentar la salida del simulador a `processor/pre-processor.py` y confirmar:
     - No ocurran excepciones durante el preprocesamiento.
     - Ocurrir los cálculos de desviación esperados.
   - Validar que algunos materiales estén marcados como fuera de especificación cuando `probability_of_out_of_spec` > 0.

3. **Escenarios Edge-Case**
   - Probar lotes con un solo material o muchos materiales.
   - Prueba de estrés con rangos extremos de temperatura/humedad.
   - Validar comportamiento cuando `storage_max_days` es `None` (vida útil ilimitada).

---  

## Ejemplo de Uso

```python
from batch_simulator import generate_batch

# Crear un lote con una semilla fija para resultados repetibles
batch = generate_batch(
    seed=42,
    material_count=3,
    probability_of_out_of_spec=0.5,
    base_timestamp="2026-07-23T12:00:00Z"
)

print(batch)
```

**Salida de Ejemplo:**
```json
{
  "batch_id": "d3f1e2a8-5c9b-4e7f-9b2a-1c2e4f5b6a7c",
  "timestamp": "2026-07-23T12:00:00Z",
  "materials": [
    {
      "name": "flour",
      "storage_days": 120,
      "out_of_spec": false
    },
    {
      "name": "yeast",
      "storage_days": 800,
      "out_of_spec": true
    },
    {
      "name": "dairy_powder",
      "storage_days": 1500,
      "out_of_spec": false
    }
  ],
  "containers": {
    "temperature": 23,
    "humidity": 67
  }
}
```

---  

## Extensibilidad

Mejoras futuras pueden incluir:
- Soportar múltiples unidades de almacenamiento con perfiles ambientales distintos.
- Agregar perfiles de restricción específicos por material (ej. zonas de temperatura preferidas).
- Exportar datos de lote a esquemas externos como JSON Lines o CSV.
- Integrar con datos meteorológicos realistas para simulación de condiciones dinámicas.

Este diseño asegura que el simulador permanezca ligero mientras ofrece suficiente flexibilidad para una prueba exhaustiva de la evaluación de riesgos.  

*Documento generado el 23 de julio de 2026 por el equipo de desarrollo del Sistema de Alertas de Calidad y Riesgo de Vencimiento.*