## Why

Necesito automatizar el flujo de publicación de fotos en Instagram: detectar nuevas imágenes en Google Drive, editarlas con IA, generar captions y recibir una notificación cuando esté listo. Actualmente es un proceso manual que consume tiempo.

## What Changes

- Crear workflow con Agno orquestando múltiples agentes
- **Agente 1 - Editor de Foto**: Edita imágenes usando modelo de IA via LiteLLM
- **Agente 2 - Creador de Descripción**: Genera captions para Instagram via LiteLLM
- Integrar Google Drive API para detectar y descargar imágenes
- Usar LiteLLM como proxy unificado para llamadas a LLMs (Qwen)
- Implementar polling configurable para detectar nuevas fotos
- Dockerizar la aplicación para despliegue en Render
- Integrar Telegram Bot para notificaciones

## Capabilities

### New Capabilities

- `drive-monitor`: Monitoriza carpeta de Google Drive y detecta nuevas imágenes
- `image-editor-agent`: Agente Agno que edita imágenes usando modelo de IA via LiteLLM
- `caption-agent`: Agente Agno que genera descripciones para Instagram via LiteLLM
- `telegram-notifier`: Envía notificaciones con imagen editada y caption
- `polling-scheduler`: Gestiona el intervalo de verificación configurable

### Modified Capabilities

- Ninguno por ahora

## Impact

- Workflow Agno con 2 agentes especializados
- Nueva aplicación Python dockerizada
- Dependencias: agno, litellm, google-api-python-client, python-telegram-bot
- Variables de entorno para credenciales de Google Drive, LiteLLM, Telegram
- Despliegue en Render con Docker