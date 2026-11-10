
# ABIA — Autonomous Business Intelligence Agent

An agentic AI-powered Sales Intelligence system that transforms raw sales data into actionable business insights using local LLM reasoning, Python execution, evidence validation, and automated reporting.

## Project Overview

ABIA allows users to upload sales CSV files and ask business questions in natural language.

Instead of relying on a single LLM response, ABIA follows a structured workflow:

**Plan → Execute → Observe → Critique → Report**

The LLM plans the analysis, approved Python tools perform deterministic calculations, and a critic reviews the evidence before the final report is generated.

## Key Features

- CSV upload through a Streamlit dashboard.
- Automatic detection of common sales column names.
- Sales analytics using Pandas.
- Natural-language business questions using Qwen3.
- Structured analysis planning.
- Approved tool execution.
- Evidence-based critic validation.
- Business report generation.
- Local model execution using Ollama.

## Architecture

```text
             User
              |
              v
       Streamlit Dashboard
              |
              v
       Sales Orchestrator
              |
              v
       Analysis Planner
          (Qwen3)
              |
              v
       Tool Executor
       (Python/Pandas)
              |
              v
       Analysis Results
              |
              v
        Critic Review
              |
        +-----+-----+
        |           |
     Approved    Rejected
        |           |
        v           v
   Report       Stop with
  Generator      Error
        |
        v
   Business Report
```

## Agent Execution Loop

1. **Plan:** Qwen3 interprets the business question and selects approved analysis tools.
2. **Execute:** Python and Pandas execute deterministic calculations.
3. **Observe:** The orchestrator collects structured execution results.
4. **Critique:** The critic validates the available evidence and derives supported findings.
5. **Report:** The report generator checks product revenue conclusions against the underlying results before producing a report.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Local LLM | Qwen3 4B |
| Model runtime | Ollama |
| Data processing | Pandas |
| Numerical computing | NumPy |
| User interface | Streamlit |
| Version control | Git |
| Repository hosting | GitHub |

## Project Structure

```text
autonomous-bi-agent/
|
├── app.py
├── data/
│   └── sales.csv
|
├── src/
│   └── bi_agent/
│       ├── analysis_planner.py
│       ├── critic.py
│       ├── data_analyzer.py
│       ├── orchestrator.py
│       ├── report_generator.py
│       └── tool_executor.py
|
├── test_analysis_planner.py
├── test_critic.py
├── test_data_analyzer.py
├── test_orchestrator.py
├── test_report_generator.py
├── test_report_validation.py
├── test_tool_executor.py
|
├── .gitignore
└── README.md
```

## Local Setup

### Prerequisites

- Python installed.
- Git installed.
- Ollama installed.
- Qwen3 4B model downloaded.

### 1. Clone the repository

```bash
git clone https://github.com/chaitukotaru12/ABIA-Sales-Intelligence-Agent.git

cd ABIA-Sales-Intelligence-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the local model

```bash
ollama pull qwen3:4b
```

Ensure Ollama is running.

### 5. Launch ABIA

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## Example Business Questions

- Which product generated the highest revenue?
- Which region contributed the most revenue?
- What is the monthly revenue trend?
- What is the total sales revenue?
- How many units were sold?

## Validation and Testing

Run the analyzer tests:

```bash
python -m unittest test_data_analyzer -v
```

Run the report validation tests:

```bash
python test_report_validation.py
```

The current validation suite includes tests for:
- Incorrect highest-revenue conclusions.
- Correct highest-revenue conclusions.
- Tied highest-revenue products.

## Engineering Principles

- Deterministic calculations instead of LLM-generated arithmetic.
- Approved tools instead of arbitrary generated code execution.
- Structured planning and execution.
- Evidence validation before report generation.
- Local-first model execution.
- Human-readable business reporting.

## Current Limitations

ABIA is an evolving prototype.

- Automatic column detection supports common aliases, not every possible CSV format.
- The critic currently performs specific product-revenue validation rather than comprehensive validation of every possible business conclusion.
- Broader evaluation across different datasets and business questions is ongoing.
- Production-grade security, deployment and monitoring have not yet been implemented.

## Roadmap

- [x] Initial sales intelligence agent.
- [x] Local LLM integration.
- [x] Structured analysis planning.
- [x] Approved Python tool execution.
- [x] Initial critic validation.
- [x] Business report generation.
- [x] GitHub repository setup.
- [ ] Flexible CSV evaluation across external datasets.
- [ ] Expanded evidence validation.
- [ ] Professional dashboard refinement.
- [ ] Comprehensive evaluation suite.
- [ ] Version 1.0 release.

## Author

**Chaitanya Kotaru**

Building practical Agentic AI systems using LLMs, tools, structured workflows, and evidence-based validation.

GitHub: https://github.com/chaitukotaru12
