## ADDED Requirements

### Requirement: Cargar prompt de caption desde archivo .md
El sistema DEBE leer el contenido del archivo `caption_prompt.md` para obtener las instrucciones de generación del caption.

#### Scenario: Prompt de caption cargado
- **WHEN** el agente solicita generar un caption
- **THEN** debe leer el archivo de prompt de caption y usarlo en la llamada al LLM

### Requirement: Generar caption usando modelo via LiteLLM
El sistema DEBE llamar al modelo de texto configurado en LiteLLM (por defecto qwen) para generar una descripción para Instagram.

#### Scenario: Caption generado exitosamente
- **WHEN** el Caption Agent recibe la imagen (opcionalmente para contexto) y el prompt de caption
- **THEN** debe hacer la llamada a LiteLLM con el modelo de texto y obtener el caption generado

### Requirement: Caption válido para Instagram
El sistema DEBE generar un caption que sea apropiado para Instagram (incluir hashtags, menciones, etc. según el prompt).

#### Scenario: Caption con formato correcto
- **WHEN** el LLM genera el caption
- **THEN** el caption debe ser texto plano válido para Instagram

### Requirement: Manejo de errores en caption
El sistema DEBE manejar errores de la llamada al LLM para caption y usar un caption fallback.

#### Scenario: Error en generación de caption
- **WHEN** la llamada al modelo de caption falla
- **THEN** debe registrar el error y usar un caption alternativo de fallback