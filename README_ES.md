# Sistema de Alertas de Calidad y Riesgo de Vencimiento

---

## Descripción General

Este sistema monitorea lotes de materias primas a través de flujos de trabajo automatizados utilizando n8n, Python e agentes de IA (Groq/Google Gemini) para detectar riesgos de deterioro y alertar a los administradores.

---

## Diagrama del Sistema

![System diagram](system-diagram.png)

---

## Componentes de la Arquitectura

| Componente | Propósito | Ubicación del Archivo |
|------------|-----------|----------------------|
| Simulador de Lotes | Genera conjuntos de datos realistas para pruebas | `simulators/batch_simulator.py` |
| Pre-procesador | Valida datos de lotes contra límites de materiales (nodo n8n) | `processor/pre-processor.py` |
| Agente de IA | Procesa desviaciones y asigna categorías de riesgo (nodo n8n) | `agent/agent.py` |
| Programador de Alertas | Envía notificaciones por email/Slack (n8n) | `alerts/alert_scheduler.py` |

---

## Cómo Ejecutar el Proyecto

1. **Iniciar los servicios** usando Docker Compose:
   ```bash
   docker compose up -d
   ```

2. **Generar datos simulados**:
   ```bash
   python3.12 simulators/batch_simulator.py
   ```

3. **Ver los resultados** en `data/generated_batches.json`

---

## Categorías de Riesgo

- **1 - Mínimo**: Condiciones dentro de límites aceptables; continuar con el monitoreo y almacenamiento normales
- **2 - Medio**: Condiciones aproximándose o exceden moderadamente los límites; inspección del lote recomendada (desencadena **alerta por email**)
- **3 - Alto**: Desviaciones significativas de condiciones de almacenamiento; alta probabilidad de deterioro o vencimiento (desencadena **alerta por email**)

---

## Desarrollo

- Ver `processor/spec.md` para documentación del pre-procesador
- Ver `simulators/spec.md` para documentación del simulador
- Ver `agent/spec.md` para especificación del agente de IA
- Ver `n8n/spoilageAndRiskWorkflow.json` para ver el archivo de configuración del flujo de trabajo n8n.

---

*Desarrollado por Juan Camilo Cardenas Zabala. Documento generado el 23 de julio de 2026*