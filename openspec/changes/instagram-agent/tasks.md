## 1. Setup del Proyecto

- [ ] 1.1 Crear estructura de directorios del proyecto
- [ ] 1.2 Crear archivo requirements.txt con dependencias (agno, litellm, google-api-python-client, python-telegram-bot, pyyaml)
- [ ] 1.3 Crear archivo .env.example con todas las variables de entorno necesarias
- [ ] 1.4 Crear archivo config/settings.yaml con configuración por defecto
- [ ] 1.5 Crear directorio config/prompts/ con archivos .md de ejemplo

## 2. Docker

- [ ] 2.1 Crear Dockerfile con Python 3.11
- [ ] 2.2 Crear archivo .dockerignore
- [ ] 2.3 Crear docker-compose.yml para desarrollo local

## 3. Google Drive Integration

- [ ] 3.1 Crear módulo drive_client.py para autenticación con service account
- [ ] 3.2 Implementar función para listar archivos en carpeta de Drive
- [ ] 3.3 Implementar función para descargar imagen desde Drive
- [ ] 3.4 Implementar función para subir imagen a carpeta de salida

## 4. Tracking de Imágenes Procesadas

- [ ] 4.1 Crear archivo processed_images.json para tracking
- [ ] 4.2 Implementar funciones para marcar imagen como procesada
- [ ] 4.3 Implementar función para verificar si imagen ya fue procesada

## 5. Image Editor Agent

- [ ] 5.1 Crear agente Agno para edición de imágenes
- [ ] 5.2 Implementar función para cargar prompt desde archivo .md
- [ ] 5.3 Implementar integración con LiteLLM para edición de imagen
- [ ] 5.4 Implementar manejo de errores y retry

## 6. Caption Agent

- [ ] 6.1 Crear agente Agno para generación de captions
- [ ] 6.2 Implementar función para cargar prompt de caption desde archivo .md
- [ ] 6.3 Implementar integración con LiteLLM para generación de texto
- [ ] 6.4 Implementar caption fallback en caso de error

## 7. Telegram Notifier

- [ ] 7.1 Crear módulo telegram_client.py
- [ ] 7.2 Implementar función para enviar imagen con caption
- [ ] 7.3 Implementar función para enviar notificación de error

## 8. Polling Scheduler

- [ ] 8.1 Crear scheduler configurable con intervalo leído de variable de entorno
- [ ] 8.2 Implementar ciclo principal de polling
- [ ] 8.3 Implementar manejo de señales para parada limpia

## 9. Workflow Principal

- [ ] 9.1 Crear workflow Agno que orqueste los dos agentes
- [ ] 9.2 Implementar flujo completo: detectar → descargar → editar → caption → subir → notificar
- [ ] 9.3 Integrar todos los componentes en main.py

## 10. Testing y Despliegue

- [ ] 10.1 Crear script de test para verificar credenciales
- [ ] 10.2 Probar ejecución local con Docker
- [ ] 10.3 Preparar configuración para Render (Dockerfile optimizado, health check)
- [ ] 10.4 Documentar variables de entorno necesarias en README.md