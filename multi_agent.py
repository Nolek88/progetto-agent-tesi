import os
import sys
from langgraph.graph import StateGraph
from langchain.schema import HumanMessage
from langchain_ollama import ChatOllama

# Modello Llama 3.2 tramite Ollama
llm = ChatOllama(model="llama3.2")

# Funzione per leggere il contenuto del file
def read_file_content(file_name):
    if not os.path.exists(file_name):
        print(f"Errore: Il file '{file_name}' non è stato trovato.")
        sys.exit(1)

    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

# Agent 1: Suggerisce parametri per migliorare la copertura
def agent_stage(state):
    description = state.get("description", "").strip()
    additional_context = f"\n\nInformazioni aggiuntive fornite dall'utente:\n{description}" if description else ""

    prompt = f"""
    Analizza i seguenti metodi:

    {state.get("methods_content", "Nessun metodo disponibile.")}

    Il tuo compito è **solo** quello di identificare **parametri di input** 
    che coprano il maggior numero di scenari possibili per questi metodi. 
    Includi sia input validi che, eventualmente, casi che generano eccezioni.  
    **Non generare test, limitati solo ai parametri.**{additional_context}
    """
    response = llm.invoke([HumanMessage(content=prompt)])

    return {**state, "parameters": response.content}

# Agent 2: Analizza il metodo e i test esistenti
def agent_analysis(state):
    description = state.get("description", "").strip()
    additional_context = f"\n\nInformazioni aggiuntive fornite dall'utente:\n{description}" if description else ""

    prompt = f"""
    Analizza i seguenti metodi:

    {state.get("methods_content", "Nessun metodo disponibile.")}

    Il tuo compito è verificare la funzionalità del metodo in base al caso di test associato e spiega perché il metodo non è completamente coperto dai casi di test associati.  
    **Non generare test ed esempi di test.**  
    Includi sia casi di input validi che, eventualmente, situazioni che generano eccezioni.{additional_context}
    """
    response = llm.invoke([HumanMessage(content=prompt)])

    return {**state, "analysis": response.content}

# Agent 3: Genera test completi, non solo eccezioni
def agent_test_generation(state):
    prompt = f"""
    Genera test per il seguente metodo:

    {state.get("methods_content", "Nessun metodo disponibile.")}

    Parametri suggeriti:
    {state.get("parameters", "Nessun parametro fornito.")}

    Analisi della copertura attuale:
    {state.get("analysis", "Nessuna analisi disponibile.")}

    I test devono coprire **tutte** le seguenti casistiche:
    - Input validi e attesi
    - Gestione degli errori (eccezioni), solo se necessario 

    **Non generare solo test che lanciano eccezioni.**  
    Scrivi test in JUnit con nomi chiari e assert significativi.  
    """
    response = llm.invoke([HumanMessage(content=prompt)])

    return {**state, "generated_tests": response.content}

# Agent 4: Revisiona e migliora i test generati
def agent_review_tests(state):
    prompt = f"""
    Rivedi i seguenti test JUnit generati per il metodo:

    {state.get("methods_content", "Nessun metodo disponibile.")}

    Analisi della copertura:
    {state.get("analysis", "Nessuna analisi disponibile.")}

    Parametri suggeriti:
    {state.get("parameters", "Nessun parametro disponibile.")}

    Test generati (da correggere e migliorare se necessario):
    {state.get("generated_tests", "Nessun test generato.")}

    Il tuo compito è:
    - Correggere errori concettuali e di sintassi nei test
    - Assicurarti che i test siano coerenti con l'analisi e i parametri
    - Migliorare la qualità e chiarezza dei nomi dei metodi di test e degli assert

    Fornisci solo i test JUnit migliorati come output.
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "generated_tests": response.content}  # Sovrascrive i test generati con quelli revisionati

# Creazione del grafo con stato basato su dizionario
workflow = StateGraph(dict)

# Definizione dei nodi (agenti)
workflow.add_node("stage", agent_stage)
workflow.add_node("analysis", agent_analysis)
workflow.add_node("test_generation", agent_test_generation)
workflow.add_node("review_tests", agent_review_tests)

# Definizione delle transizioni
workflow.set_entry_point("stage")
workflow.add_edge("stage", "analysis")
workflow.add_edge("analysis", "test_generation")
workflow.add_edge("test_generation", "review_tests")

# Compilazione del workflow
app = workflow.compile()

# Lettura del file specificato dall'utente
file_name = input("Inserisci il nome del file contenente i metodi da analizzare: ").strip()
methods_content = read_file_content(file_name)

# Chiedere all'utente se vuole aggiungere una descrizione
use_description = input("Vuoi aggiungere una descrizione per dare un contesto ulteriore? (s/n): ").strip().lower()

while use_description not in ["s", "n"]:
    print("Opzione non valida. Inserisci 's' per sì o 'n' per no.")
    use_description = input("Vuoi aggiungere una descrizione per dare un contesto ulteriore? (s/n): ").strip().lower()

if use_description == "s":
    description = input("Inserisci la descrizione: ").strip()
elif use_description == "n":
    description = ""

print("\nGenerazione in corso...")

# Stato iniziale come dizionario
initial_state = {
    "methods_content": methods_content,
    "description": description,
    "parameters": None,
    "analysis": None,
    "generated_tests": None
}

# Esecuzione del workflow
final_state = app.invoke(initial_state)

# Output dei risultati
print("\n### Parametri suggeriti ###")
print(final_state.get("parameters", "Nessun parametro generato."))

print("\n### Analisi ###")
print(final_state.get("analysis", "Nessuna analisi disponibile."))

print("\n### Test Generati e Revisionati ###")
print(final_state.get("generated_tests", "Nessun test disponibile."))