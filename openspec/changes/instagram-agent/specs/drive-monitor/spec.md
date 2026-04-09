## ADDED Requirements

### Requirement: Detectar nuevas imágenes en Google Drive
El sistema DEBE verificar periódicamente la carpeta de Google Drive configurada en busca de nuevas imágenes que no hayan sido procesadas previamente.

#### Scenario: Nueva imagen detectada
- **WHEN** el sistema detecta un archivo de imagen en la carpeta de Drive que no está en la lista de procesadas
- **THEN** debe marcar la imagen como "pendiente" y descargarla

### Requirement: Descargar imagen de Google Drive
El sistema DEBE poder descargar las imágenes detectadas para su procesamiento.

#### Scenario: Descarga exitosa
- **WHEN** se inicia la descarga de una imagen válida
- **THEN** la imagen debe guardarse localmente para procesamiento

### Requirement: Registrar imagen procesada
El sistema DEBE mantener un registro de las imágenes ya procesadas para evitar duplicados.

#### Scenario: Imagen registrada
- **WHEN** una imagen ha sido procesada completamente
- **THEN** debe agregarse al archivo de tracking para evitar reprocesamiento

### Requirement: Ignorar imágenes procesadas
El sistema DEBE ignorar imágenes que ya están en el registro de procesadas.

#### Scenario: Imagen duplicada
- **WHEN** el sistema detecta una imagen que ya fue procesada anteriormente
- **THEN** debe omitirla y continuar con la siguiente