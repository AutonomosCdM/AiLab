#!/usr/bin/env python
"""
Script para probar la integración de la búsqueda web con Lucius.
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Asegurarse de que la API key está disponible
if not os.environ.get('BRAVE_SEARCH_API_KEY'):
    print("ERROR: BRAVE_SEARCH_API_KEY no está configurada en el entorno.")
    print("Establezca esta variable de entorno antes de ejecutar este script.")
    sys.exit(1)

# Importar el agente Lucius
from src.lucius_agent import LuciusAgent

def main():
    # Inicializar el agente
    print("Inicializando Lucius Agent...")
    agent = LuciusAgent()
    
    # Verificar herramientas disponibles
    print(f"\nHerramientas generales disponibles: {agent.tool_manager.list_tools()}")
    
    # Simular una consulta que requiera búsqueda web
    test_queries = [
        "¿Qué es la inteligencia artificial?",
        "Busca información sobre tendencias tecnológicas en 2025",
        "Necesito saber sobre avances en IA generativa"
    ]
    
    # Procesar cada consulta
    for query in test_queries:
        print("\n" + "="*50)
        print(f"Consulta: {query}")
        print("="*50)
        
        # Simular respuesta del modelo que sugiere usar la herramienta web_search
        tool_code = f"""```tool_code
<tool_code>
web_search: {query}
</tool_code>
```"""
        
        # Ejecutar la herramienta
        print("Ejecutando búsqueda web...")
        result = agent.tool_manager.execute_tool("web_search", query)
        print("\nResultado:")
        print(result)
    
    print("\nPrueba completada.")

if __name__ == "__main__":
    main()
