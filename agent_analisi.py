from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

# Inizializza il modello Ollama con Llama3
llm = ChatOllama(model="llama3", temperature=0.3, max_tokens=256)

# Funzione per generare il prompt
def generate_analysis_prompt(java_code, test_code, question):
    prompts = {
        "1": "Descrivi la funzionalità del metodo Java fornito in base al caso di test associato. in italiano.",
        "2": "Spiega perché il metodo non è completamente coperto dai casi di test associati. in italiano.",
        "3": "Suggerisci una soluzione per migliorare la copertura dei test. in italiano.",
    }

    if question not in prompts:
        return "Scelta non valida."

    template = PromptTemplate(
        input_variables=["java_code", "test_code"],
        template=(
            "Ecco un metodo Java:\n{java_code}\n\n"
            "Ecco i test associati:\n{test_code}\n\n"
            f"{prompts[question]}"
        )
    )
    response = llm.invoke(template.format(java_code=java_code, test_code=test_code))

    # Estrarre il contenuto testuale dalla risposta
    return response.content if response and hasattr(response, 'content') else "Errore nella generazione dell'analisi."

# Funzione per acquisire codice multi-linea
def get_multiline_input(prompt_text):
    print(prompt_text)
    lines = []
    while True:
        line = input()
        if line == "":  # L'utente preme Invio su una riga vuota per terminare
            break
        lines.append(line)
    return "\n".join(lines)

# Programma principale
if __name__ == "__main__":
    print("### Analizzatore di codice Java e test ###")

    # Acquisizione del codice con supporto multi-linea
    java_code = get_multiline_input("Inserisci il metodo Java (premi Invio su una riga vuota per terminare):")
    test_code = get_multiline_input("Inserisci il codice del test (premi Invio su una riga vuota per terminare):")

    while True:
        print("\nScegli un'analisi da eseguire:")
        print("1. Descrivere la funzionalità del metodo Java")
        print("2. Verificare la copertura dei test")
        print("3. Suggerire miglioramenti per i test")
        print("4. Esci")

        choice = input("Inserisci il numero della tua scelta: ")

        if choice == "4":
            print("Chiusura del programma...")
            break

        print("\nAnalisi in corso...\n")
        try:
            analysis = generate_analysis_prompt(java_code, test_code, choice)
            print("\n### Risultato dell'analisi ###\n")
            print(analysis)

            # Scrive l'analisi in un file txt
            with open("analisi_risultato.txt", "a", encoding="utf-8") as file:
                file.write("### Risultato dell'analisi ###\n\n")
                file.write(analysis + "\n")

            print("\nL'analisi è stata salvata in 'analisi_risultato.txt'.")
        except Exception as e:
            print(f"Errore durante l'analisi: {e}")