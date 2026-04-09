## 1. Setup del Proyecto

- [x] 1.1 Crear estructura de directorios del proyecto
- [x] 1.2 Crear archivo requirements.txt con dependencias (agno, litellm, google-api-python-client, python-telegram-bot, pyyaml)
- [x] 1.3 Crear archivo .env.example con todas las variables de entorno necesarias
- [x] 1.4 Crear archivo config/settings.yaml con configuración por defecto
- [x] 1.5 Crear directorio config/prompts/ con archivos .md de ejemplo

## 2. Docker

- [x] 2.1 Crear Dockerfile con Python 3.11
- [x] 2.2 Crear archivo .dockerignore
- [x] 2.3 Crear docker-compose.yml para desarrollo local

## 3. Google Drive Integration

- [x] 3.1 Crear módulo drive_client.py para autenticación con service account
- [x] 3.2 Implementar función para listar archivos en carpeta de Drive
- [x] 3.3 Implementar función para descargar imagen desde Drive
- [x] 3.4 Implementar función para subir imagen a carpeta de salida

## 4. Tracking de Imágenes Procesadas

- [x] 4.1 Crear archivo processed_images.json para tracking
- [x] 4.2 Implementar funciones para marcar imagen como procesada
- [x] 4.3 Implementar función para verificar si imagen ya fue procesada

## 5. Image Editor Agent

- [x] 5.1 Crear agente Agno para edición de imágenes
- [x] 5.2 Implementar función para cargar prompt desde archivo .md
- [x] 5.3 Implementar integración con LiteLLM para edición de imagen
- [x] 5.4 Implementar manejo de errores y retry

## 6. Caption Agent

- [x] 6.1 Crear agente Agno para generación de captions
- [x] 6.2 Implementar función para cargar prompt de caption desde archivo .md
- [x] 6.3 Implementar integración con LiteLLM para generación de texto
- [x] 6.4 Implementar caption fallback en caso de error

## 7. Telegram Notifier

- [x] 7.1 Crear módulo telegram_client.py
- [x] 7.2 Implementar función para enviar imagen con caption
- [x] 7.3 Implementar función para enviar notificación de error

## 8. Polling Scheduler

- [x] 8.1 Crear scheduler configurable con intervalo leído de variable de entorno
- [x] 8.2 Implementar ciclo principal de polling
- [x] 8.3 Implementar manejo de señales para parada limpia

## 9. Workflow Principal

- [x] 9.1 Crear workflow Agno que orqueste los dos agentes
- [x] 9.2 Implementar flujo completo: detectar → descargar → editar → caption → subir → notificar
- [x] 9.3 Integrar todos los componentes en main.py

## 10. Testing y Despliegue

- [x] 10.1 Crear script de test para verificar credenciales
- [ ] 10.2 Probar ejecución local con Docker
- [x] 10.3 Preparar configuración para Render (Dockerfile optimizado, health check)
- [x] 10.4 Documentar variables de entorno necesarias en README.md