## Context

Sistema automatizado para publicación de contenido en Instagram. Monitorea Google Drive en busca de nuevas imágenes, las procesa con IA (edición + caption) y notifica al usuario por Telegram. El sistema corre como contenedor Docker en Render.

## Goals / Non-Goals

**Goals:**
- Workflow Agno con 2 agentes especializados (Image Editor Agent, Caption Agent)
- Polling configurable a Google Drive cada N minutos
- Edición de imágenes usando modelo Qwen via LiteLLM
- Generación de captions para Instagram usando modelo Groq via LiteLLM
- Notificaciones por Telegram con imagen editada y caption
- Dockerización completa para despliegue en Render
- Prompts editables desde archivos .md externos

**Non-Goals:**
- No incluye publicación directa a Instagram (solo genera contenido)
- No maneja autenticación de usuarios múltiples
- No implementa webhooks de Google Drive (usa polling simple)

## Decisions

| Decisión | Alternativas | Selección |
|----------|--------------|-----------|
| Orquestación | Agente único vs Multi-agente | **Multi-agente** - Dos agentes especializados permite separación de responsabilidades y mayor flexibilidad |
| Modelo de LLM | Un modelo para todo vs Múltiples | **LiteLLM unificado** - Proxy para cambiar modelos sin código |
| Editor de imagen | Qwen VL, DALL-E, Stable Diffusion | **Qwen** - Ya disponible en LiteLLM via DashScope |
| Polling | Intervalo fijo vs Exponential backoff | **Intervalo configurable** - Definido por variable `POLLING_INTERVAL_MINUTES` |
| Tracking | Base de datos vs Archivo | **Archivo JSON** - Simplicidad para tracking de procesadas |
| Contenedor | Un solo contenedor vs Múltiples | **Un solo contenedor** - Suficiente para este caso, más simple en Render |

## Risks / Trade-offs

- [Riesgo] API rate limits de LiteLLM/DashScope → **Mitigación**: Implementar retry con backoff, hacer configurable el intervalo de polling
- [Riesgo] Fallo en procesamiento de imagen → **Mitigación**: Logging detallado, notificación de error por Telegram
- [Riesgo] Google Drive quota exceeded → **Mitigación**: Manejo de errores con reintentos
- [Riesgo] Imagen grande ocupa mucha memoria → **Mitigación**: Limitar tamaño de imagen antes de enviar al LLM
- [Trade-off] Polling vs Webhooks → Menos eficiente pero más simple de implementar y mantener