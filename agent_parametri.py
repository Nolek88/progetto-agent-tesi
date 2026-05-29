import os
import sys
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage

def read_file_content(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Errore durante la lettura del file {file_name}: {e}")
        return None

def main():
    methods_file_name = input("Inserisci il nome del file contenente i metodi da considerare: ").strip()
    if not os.path.exists(methods_file_name):
        print(f"Errore: Il file {methods_file_name} non è stato trovato.")
        sys.exit(1)
    
    methods_content = read_file_content(methods_file_name)
    methods = [line.strip() for line in methods_content.splitlines() if line.strip()]

    description = input("Inserisci una descrizione per fornire ulteriori dettagli(opzionale): ").strip()

    prompt = f"""
    Metodi forniti da file:
    {methods_content}

    Descrizione: {description if description else 'Nessuna descrizione inserita.'}

    Linee guida:
    1. Fornisci una lista numerata di parametri interessanti per aumentare la copertura del metodo testato.
    2. Per ciascuno dei parametri elencati, genera test che coprano:
        - Casi di funzionamento corretto con input validi ma che non lanciano eccezioni (per capire quali sono degli input che non lanciano eccezioni osserva attentamente le variabili).
        - Gestione delle eccezioni con input non validi (qui devi perforza usare dei try catch) o situazioni impreviste. 
        - Queste due situazioni, funzionamento corretto e gestione delle eccezioni, devono essere separate in test distinti.
    3. Evita la semplice replica della struttura o delle casistiche dei test esistenti. Concentrati sulla creazione di test che rivelino nuovi comportamenti o potenziali problemi nel codice.
    4. Non usare assert di alcun tipo nei test generati (quindi non usare nulla appartenente a org.junit.Assert.*).
    """

    print("\n----- Prompt generato -----")
    print(prompt)
    print("---------------------------------\n")

    print("Risposta :")
    chat = ChatOllama(model="llama3.2")
    response = chat.invoke([HumanMessage(content=prompt)])
    print(response.content)

if __name__ == "__main__":
    main()
