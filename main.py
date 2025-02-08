from src.chatbot.query_handler import QueryHandler

def main():
    handler = QueryHandler()
    print("\nWelcome to the Company Database Assistant!")
    print("Type 'help' for available commands or 'exit' to quit.")
    
    while True:
        query = input("\nWhat would you like to know? ").strip()
        
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        elif query.lower() == 'help':
            print(handler.process_query("help"))
        else:
            print(handler.process_query(query))

if __name__ == "__main__":
    main()