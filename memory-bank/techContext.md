# Contexto Tecnológico

### Frontend
- **LangChain:** Versión más reciente - Framework para la creación de aplicaciones de lenguaje.
- **React:** Versión más reciente -  Para la interfaz de usuario web (opcional, si se decide crear una interfaz web además de Slack).

### Backend
- **Python:** Versión 3.x - Lenguaje principal para el backend y la lógica del agente.
- **Groq Llama API:**  - Modelo de lenguaje para procesamiento de lenguaje natural.
- **Slack Bolt:** Framework para construir aplicaciones de Slack.

### Base de Datos
- **SQLite:**  - Para almacenamiento local de datos de contexto y configuraciones del agente (adecuado para la simplicidad inicial).

### Infraestructura
- **Railway:** - Plataforma de despliegue en la nube.
- **Docker:** - Para la contenedorización de la aplicación.
- **GitHub:** - Para el repositorio de código y despliegue automático.
- **Groq Cloud:** - Para acceder al modelo Groq Llama.
- **Slack API (Socket Mode):** - Para la comunicación con Slack.

### Herramientas de Desarrollo
- **VSCode:**  - IDE principal para desarrollo.
- **pip:** - Gestor de paquetes de Python.
- **Git:** - Control de versiones.
- **Railway CLI (opcional):** - Para gestión del despliegue.

## Configuración del Entorno de Desarrollo
### Requisitos Previos
- Python 3.x
- Pip (Python package installer)
- Git
- Railway CLI (opcional)
- Cuenta de Railway y GitHub
- Cuenta de Groq Cloud
- Slack App configurada con Socket Mode

### Pasos de Configuración
1. Clonar el repositorio de GitHub.
2. Crear un entorno virtual de Python: `python3 -m venv venv`
3. Activar el entorno virtual: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar variables de entorno:
    - En el archivo `.env` (local):
        - `SLACK_BOT_TOKEN`: Token de bot de Slack (xoxb-...).
        - `SLACK_APP_TOKEN`: App token de Slack (xapp-...).
        - `GROQ_API_KEY`: API Key de Groq.
    - En Railway (despliegue):
        - `SLACK_BOT_TOKEN`: Token de bot de Slack (xoxb-...).
        - `SLACK_APP_TOKEN`: App token de Slack (xapp-...).
        - `GROQ_API_KEY`: API Key de Groq.

## Configuración del Entorno de Despliegue en Railway
### Método de Despliegue
- **Desde Repositorio GitHub usando Dockerfile:**
    1. **Dockerfile:** Definir un Dockerfile en la raíz del proyecto para especificar el entorno de ejecución.
        - Imagen base: `python:3.11-slim-bookworm`
        - Directorio de trabajo: `/app`
        - Copiar `requirements.txt` e instalar dependencias con `pip install --no-cache-dir -r requirements.txt`
        - Copiar código fuente: `COPY . .`
        - Comando de inicio: `CMD ["python", "lucius_agent.py"]`
    2. **.dockerignore (opcional):**  Crear un archivo `.dockerignore` para excluir archivos innecesarios del Docker image.
    3. **Crear Proyecto en Railway:**  Crear un nuevo proyecto en Railway y seleccionar "Deploy from GitHub repo".
    4. **Seleccionar Repositorio:**  Conectar Railway al repositorio de GitHub del proyecto `lucius`.
    5. **Variables de Entorno en Railway:** Configurar variables de entorno en la configuración del servicio Railway:
        - `GROQ_API_KEY`: API Key de Groq.
        - `SLACK_APP_TOKEN`: App token de Slack (xapp-...).
        - `SLACK_BOT_TOKEN`: Token de bot de Slack (xoxb-...).
        - `PORT`: `8080`.
    6. **Exponer el servicio:** Habilitar "Public Networking" en la configuración del servicio Railway.

### Variables de Entorno
- `GROQ_API_KEY`: API Key para acceder a la API de Groq Llama.
- `SLACK_BOT_TOKEN`: Token de bot de Slack (xoxb-...).
- `SLACK_APP_TOKEN`: App token de Slack (xapp-...).
- `PORT`: Puerto en el que la aplicación escucha (por defecto 8080 para Railway).

## Dependencias Externas
### APIs
- **Groq Llama API:**
  - Propósito: Inferencias del modelo de lenguaje.
  - Endpoints clave: Endpoint de inferencia de Groq API.
  - Autenticación: API Key de Groq.
- **Slack API (Socket Mode):**
  - Propósito: Comunicación con Slack.
  - Endpoints clave:  Slack API methods para mensajería, usuarios, etc. (detalles según necesidad).
  - Autenticación: Tokens de Slack App y Bot.

### Servicios
- **Groq Cloud:** Servicio en la nube que aloja el modelo Groq Llama.
- **Railway:** Plataforma de despliegue y hosting.
- **GitHub:**  Plataforma de control de versiones y despliegue.
- **Slack Workspace:** Espacio de trabajo de Slack donde se integrará Lucius.

## Restricciones Técnicas
- **Limitaciones de la API de Groq:**  Dependencia de la disponibilidad y cuotas de la API de Groq.
- **Dependencia de Railway:**  Dependencia de la plataforma Railway para el despliegue y hosting.
- **Limitaciones de la API de Slack:** Restricciones de la API de Slack en cuanto a frecuencia de llamadas, permisos, etc.
- **Latencia de las APIs:**  Posible latencia en las respuestas de la API de Groq y Slack.

## Decisiones Técnicas
### 1. Uso de LangChain
- **Contexto:** Necesidad de un framework para orquestar el agente de IA.
- **Decisión:** Utilizar LangChain.
- **Justificación:** LangChain facilita la creación de agentes complejos, proporciona abstracciones y módulos útiles, y se integra bien con modelos de lenguaje y APIs.

### 2. Modelo de Lenguaje
- **Contexto:**  Requisito de usar Groq Llama.
- **Decisión:** Usar Groq Llama como modelo de lenguaje principal.
- **Justificación:** Groq Llama ofrece un buen equilibrio entre rendimiento y costo, y es compatible con LangChain.

### 3. Integración con Slack
- **Contexto:** Requisito de integrar con Slack.
- **Decisión:** Utilizar la Slack API con Socket Mode para la comunicación.
- **Justificación:** Socket Mode proporciona una conexión segura y en tiempo real con Slack, sin necesidad de exponer la aplicación a la red pública.

### 4. Base de Datos
- **Contexto:** Necesidad de persistencia para el contexto de conversación y configuraciones.
- **Decisión:**  Usar SQLite para almacenamiento local.
- **Justificación:** SQLite es simple, no requiere servidor, adecuado para las necesidades iniciales del proyecto.

### 5. Plataforma de Despliegue
- **Contexto:** Necesidad de una plataforma para desplegar la aplicación en la nube.
- **Decisión:** Utilizar Railway para el despliegue.
- **Justificación:** Railway es fácil de usar, soporta Dockerfile deployments, y ofrece una buena experiencia de desarrollo y despliegue.
