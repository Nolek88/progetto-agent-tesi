import sys
from langchain_ollama import OllamaLLM as Ollama
import os
import re

def leggi_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def analizza_complessita(metodo):
    """Analizza la complessità del metodo per generare test più accurati"""
    condizioni = len(re.findall(r"if\s*\(|else\s*|switch\s*\(", metodo))
    loop = len(re.findall(r"for\s*\(|while\s*\(", metodo))
    return condizioni, loop

def crea_prompt_semplificato(contenuto_file):
    # Estrae il metodo e gli eventuali test esistenti
    parti = contenuto_file.split("\n\n")
    metodo = parti[0].replace("Metodo:", "").strip()
    test_esempio = parti[1].replace("Test di esempio:", "").strip() if len(parti) > 1 else ""

    # Analizza la complessità
    condizioni, loop = analizza_complessita(metodo)
    
    # Crea la descrizione basata sulla complessità
    if condizioni > 0 or loop > 0:
        descrizione = f"Genera un set completo di test JUnit per coprire TUTTE le possibili branch del metodo. Includi test per ogni condizione e ciclo presente nel codice."
    else:
        descrizione = "Genera test JUnit completi per verificare tutte le funzionalità del metodo."

    prompt = f"""
    Metodo Java da testare:
    {metodo}

    {f"Test di esempio già esistenti (usali come riferimento):\n{test_esempio}" if test_esempio else ""}

    Requisiti:
    1. Genera SOLO codice di test JUnit (annotazioni @Test)
    2. Copri TUTTE le casistiche del metodo e tutti i relativi branch
    3. Non includere codice di produzione, solo test
    4. No commenti all'interno del test, spiegazioni alla fine
    5. Non generare test ridondanti o duplicati
    6. Usa nomi descrittivi per i metodi di test
    
    {descrizione}
    """
    
    return prompt

def invia_a_ollama(prompt):
    llm = Ollama(model="llama3.2")
    return llm.invoke(prompt)

def organizza_risposta(risposta):
    # Pulisce e formatta la risposta
    risposta = risposta.strip()
    if not risposta.startswith("@"):
        risposta = "// Test generati automaticamente\n\n" + risposta
    return risposta

def main():
    if len(sys.argv) < 2:
        print("Usage: python testgen.py <file_input>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    if not os.path.isfile(file_path):
        print(f"Errore: File '{file_path}' non trovato")
        sys.exit(1)
    
    contenuto = leggi_file(file_path)
    prompt = crea_prompt_semplificato(contenuto)
    
    print("Generazione test in corso...")
    risposta = invia_a_ollama(prompt)
    
    print("\n=== TEST GENERATI ===\n")
    print(organizza_risposta(risposta))

if __name__ == "__main__":
    main()