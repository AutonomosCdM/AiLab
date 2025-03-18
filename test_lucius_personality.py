from lucius_agent import LuciusAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_personality_test():
    lucius_agent = LuciusAgent()
    personality_manager = lucius_agent.personality_manager

    print("Lucius Personality Test CLI")
    print("--------------------------")
    print("Personalidades disponibles:", personality_manager.list_available_personalities())
    
    print("\nPersonalidad actual:", personality_manager.active_personality_name)
    
    print("\nInteractúa con Lucius. Comandos especiales:")
    print("- 'resumen': Ver resumen de la conversación")
    print("- 'exit': Salir del CLI")

    while True:
        try:
            user_input = input("User: ")
            
            if user_input.lower() == 'exit':
                print("Saliendo del CLI de Lucius...")
                break
            
            if user_input.lower() == 'resumen':
                summary = personality_manager.get_conversation_summary()
                print("\nResumen de la Conversación:")
                print(f"Temas: {', '.join(summary['topics'])}")
                print(f"Sentimiento: {summary['sentiment']}")
                print(f"Longitud del contexto: {summary['context_length']} interacciones")
                continue
                        
            response = lucius_agent.handle_message(user_input)
            print(f"Lucius: {response}")
        
        except KeyboardInterrupt:
            print("\nSaliendo del CLI de Lucius...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_personality_test()
