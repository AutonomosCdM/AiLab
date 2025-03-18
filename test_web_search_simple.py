#!/usr/bin/env python
"""
Script simplificado para probar la funcionalidad de búsqueda web.
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

# Importar directamente el gestor de herramientas
from src.modules.tool_manager import ToolManager

def main():
    # Inicializar el gestor de herramientas
    print("Inicializando Tool Manager...")
    tool_manager = ToolManager()
    
    # Verificar herramientas disponibles
    print(f"\nHerramientas disponibles: {tool_manager.list_tools()}")
    
    # Simular consultas de búsqueda web
    test_queries = [
        "¿Qué es la inteligencia artificial?",
        "Busca información sobre tendencias tecnológicas en 2025",
        "Avances en IA generativa"
    ]
    
    # Procesar cada consulta
    for query in test_queries:
        print("\n" + "="*50)
        print(f"Consulta: {query}")
        print("="*50)
        
        # Ejecutar la búsqueda
        print("Ejecutando búsqueda web...")
        results = tool_manager.search_web(query, count=3)
        
        # Generar resumen
        summary = tool_manager.summarize_search_results(results)
        
        print("\nResultado:")
        print(summary)
    
    print("\nPrueba completada.")

if __name__ == "__main__":
    main()
