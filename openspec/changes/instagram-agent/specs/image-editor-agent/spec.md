## ADDED Requirements

### Requirement: Cargar prompt de edición desde archivo .md
El sistema DEBE leer el contenido del archivo `image_prompt.md` para obtener las instrucciones de edición de imagen.

#### Scenario: Prompt cargado exitosamente
- **WHEN** el agente solicita editar una imagen
- **THEN** debe leer el archivo de prompt y usarlo en la llamada al LLM

### Requirement: Editar imagen usando modelo via LiteLLM
El sistema DEBE llamar al modelo de edición de imagen configurado en LiteLLM (por defecto qwen) con la imagen y el prompt.

#### Scenario: Llamada a LiteLLM exitosa
- **WHEN** el Image Editor Agent recibe una imagen y el prompt
- **THEN** debe hacer la llamada a LiteLLM con el modelo de imagen configurado y obtener la imagen editada

### Requirement: Guardar imagen editada en Drive
El sistema DEBE guardar la imagen editada en la carpeta de salida de Google Drive.

#### Scenario: Imagen guardada en Drive
- **WHEN** la imagen ha sido editada exitosamente
- **THEN** debe subir la imagen a la carpeta de salida configurada

### Requirement: Manejo de errores en edición
El sistema DEBE manejar errores de la llamada al LLM y notificar por Telegram si falla.

#### Scenario: Error en edición de imagen
- **WHEN** la llamada al modelo de imagen falla
- **THEN** debe registrar el error y enviar una notificación de fallo por Telegram