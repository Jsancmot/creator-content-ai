## ADDED Requirements

### Requirement: Intervalo de polling configurable
El sistema DEBE permitir configurar el intervalo de verificación de nuevas imágenes mediante variable de entorno `POLLING_INTERVAL_MINUTES`.

#### Scenario: Polling configurado
- **WHEN** el sistema se inicia con `POLLING_INTERVAL_MINUTES=5`
- **THEN** debe verificar Google Drive cada 5 minutos

### Requirement: Ejecución continua del workflow
El sistema DEBE mantener el workflow en ejecución continua, verificando nuevas imágenes según el intervalo configurado.

#### Scenario: Workflow ejecutándose continuamente
- **WHEN** el sistema está en modo de ejecución
- **THEN** debe ejecutar el ciclo de polling indefinidamente hasta que se detenga

### Requirement: Manejo de parada gracefully
El sistema DEBE poder detenerse de forma limpia (Ctrl+C o señal) sin dejar procesos huérfanos.

#### Scenario: Parada del sistema
- **WHEN** el usuario envía señal de parada
- **THEN** debe completar el procesamiento actual y terminar limpiamente