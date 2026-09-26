# Multi-Agent Framework for Automated Java Test Generation

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://github.com/langchain-ai/langchain)
[![Ollama](https://img.shields.io/badge/Inference-Ollama%20(Llama%203.2)-purple.svg)](https://ollama.com/)

An automated unit test generation engine that analyzes Java source code, evaluates edge cases and branch coverage, and generates refined JUnit test suites using a multi-agent architecture powered by local LLMs.

Developed as a Curricular Internship & B.Sc. Thesis research project at the **University of Milano-Bicocca**.

---

## 📌 Key Features

- **Multi-Agent Orchestration:** Coordinated state-machine workflow built with LangGraph (`StateGraph`) to decompose test generation into distinct, verifiable stages.
- **Local Inference via Ollama:** Offline execution running Meta's `Llama 3.2` without external API dependencies or cloud data egress.
- **Branch & Complexity Analysis:** Explicit heuristic parsing of cyclomatic conditions (`if`, `switch`, loops) to guide the LLM toward complete branch execution.
- **Autonomous Reviewer Loop:** Built-in validation node dedicated to catching conceptual flaws, duplicate test cases, and assertion mismatches before final output.
- **Target Benchmark:** Validated and benchmarked against real-world bytecode components from the open-source **Apache BCEL** library.

---

## 🏗 Pipeline Architecture

The execution follows a sequential directed graph passing shared state across four specialized agent nodes:

```text
┌───────────────────────────────┐
│    Input: Java Method Code    │
│    + Optional Context Desc    │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│     1. Parameter Extractor    │
│   Identifies valid bounds &   │
│   exception-triggering inputs │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│     2. Coverage Analyzer      │
│   Inspects uncovered logic &  │
│   missing edge-case paths     │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      3. Test Generator        │
│   Produces complete JUnit     │
│   test methods (@Test)        │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│     4. Inspector & Reviewer   │
│   Fixes syntax errors, trims  │
│   redundancy & checks asserts │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│    Final JUnit Test Suite     │
└───────────────────────────────┘
```

---

## 📂 Repository Layout

- `multi_agent.py` – Core workflow script orchestrating the full LangGraph pipeline.
- `agent_test.py` – Dedicated test generator driven by cyclomatic complexity evaluation.
- `agent_analisi.py` – Interactive single-agent script for targeted analysis of methods and companion tests.
- `agent_parametri.py` – Standalone module focused on input boundary space exploration.
- `funzionamento_agenti.txt` – Step-by-step operational guide and CLI input specifications.

---

## 🚀 Quickstart

### Prerequisites

1. Install and start [Ollama](https://ollama.com/):

```bash
ollama run llama3.2
```

2. Clone this repository:

```bash
git clone https://github.com/Nolek88/progetto-agent-tesi.git
cd progetto-agent-tesi
```

3. Install required dependencies:

```bash
pip install langgraph langchain langchain-ollama
```

### Execution

Place the Java method and any existing tests into a text file (e.g., `input_method.txt`) within the root directory, then execute the multi-agent graph:

```bash
python multi_agent.py
```

Follow the CLI prompts to input the file path and any optional context. The pipeline will process the source code and print the parameters, the coverage report, and the validated JUnit tests.

---

## 👥 Authors

- **Alessandro Romeo**
- **Simone Abate**
- **Alessandro Nappi**
