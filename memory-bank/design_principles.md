# Principios de Diseño de Lucius

## Principio de Responsabilidad Única (SRP)

### Definición
El Principio de Responsabilidad Única establece que una clase o módulo debe tener una única razón para cambiar. Cada componente debe tener una responsabilidad bien definida y acotada.

### Objetivos en el Proyecto Lucius
- Crear un sistema modular y mantenible
- Facilitar la extensión y modificación de componentes
- Mejorar la comprensión y testabilidad del código

### Implementación en Lucius

#### Ejemplos de Aplicación

1. **Gestor de Herramientas (`tool_manager.py`)**
```python
class ToolManager:
    def __init__(self):
        # Única responsabilidad: gestionar herramientas disponibles
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        # Carga de herramientas
        pass
    
    def list_tools(self):
        # Listar herramientas disponibles
        pass
    
    def search_web(self, query):
        # Búsqueda web delegada a herramienta específica
        pass
```

2. **Herramienta de Búsqueda Web (`brave_search_tool.py`)**
```python
class BraveSearchTool:
    def __init__(self, api_key):
        # Única responsabilidad: gestionar búsquedas web
        self._validate_api_key(api_key)
        self.api_key = api_key
    
    def search(self, query):
        # Realizar búsqueda
        pass
    
    def _validate_api_key(self, api_key):
        # Validación de API key
        pass
    
    def summarize_results(self, results):
        # Generar resumen de resultados
        pass
```

### Beneficios Observados

1. **Modularidad**
   - Componentes independientes
   - Fácil reemplazo de herramientas
   - Menor acoplamiento entre módulos

2. **Mantenibilidad**
   - Cambios localizados
   - Menor probabilidad de efectos secundarios
   - Código más predecible

3. **Testabilidad**
   - Pruebas unitarias más simples
   - Cobertura de código más efectiva
   - Aislamiento de funcionalidades

### Guía de Implementación

#### Reglas Generales
- Cada clase tiene una única responsabilidad
- Métodos cortos y enfocados (< 20 líneas)
- Nombres descriptivos que expliquen la acción

#### Anti-Patrones a Evitar
- Clases "omnipotentes"
- Métodos con múltiples niveles de abstracción
- Clases con nombres vagos como "Manager" o "Handler"

### Herramientas de Apoyo
- Linters (pylint, flake8)
- Revisiones de código
- Documentación de diseño

### Excepciones
- Permitidas en casos de rendimiento crítico
- Siempre documentar y justificar

### Evolución Continua
- Revisiones periódicas
- Capacitación del equipo
- Mejora continua de la arquitectura

## Conclusión
SRP no es una regla rígida, sino una guía para crear código de alta calidad, mantenible y extensible.
