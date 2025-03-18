#!/usr/bin/env python
"""
CLI para probar la herramienta de búsqueda de Brave.
Uso: python brave_search_cli.py "consulta de búsqueda" [--count=N]
"""

import argparse
import os
import json
from brave_search_tool import BraveSearchTool

def main():
    parser = argparse.ArgumentParser(description='Realizar búsquedas web usando Brave Search API')
    parser.add_argument('query', help='Consulta de búsqueda')
    parser.add_argument('--count', type=int, default=5, help='Número de resultados (1-20, predeterminado: 5)')
    parser.add_argument('--offset', type=int, default=0, help='Desplazamiento para paginación')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Formato de salida')
    parser.add_argument('--api-key', help='Clave API de Brave Search (opcional, por defecto usa BRAVE_SEARCH_API_KEY)')
    
    args = parser.parse_args()
    
    # Usar la clave API proporcionada o la variable de entorno
    api_key = args.api_key or os.environ.get('BRAVE_SEARCH_API_KEY')
    
    if not api_key:
        print("Error: Se requiere una clave API de Brave Search.")
        print("Proporcione --api-key o establezca la variable de entorno BRAVE_SEARCH_API_KEY")
        return 1
    
    try:
        # Inicializar la herramienta de búsqueda
        search_tool = BraveSearchTool(api_key)
        
        # Realizar la búsqueda
        results = search_tool.search(args.query, count=args.count, offset=args.offset)
        
        # Mostrar resultados según el formato solicitado
        if args.format == 'json':
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            # Formato de texto
            if results['status'] == 'success':
                summary = search_tool.summarize_results(results)
                print(summary)
                
                print("\nResultados detallados:")
                for i, result in enumerate(results['results'], 1):
                    print(f"\n{i}. {result['title']}")
                    print(f"   URL: {result['url']}")
                    print(f"   {result['description']}")
            else:
                print(f"Error: {results.get('error', 'Búsqueda fallida')}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
