# Agentic Tour Planner - Nepal

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-2D3748?style=flat&logo=langchain)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, agentic travel orchestration system designed to provide a premium tour planning experience in Nepal. Leveraging **LangGraph** for sophisticated task routing and **Gemini 2.0 Flash** for semantic reasoning, this platform transforms complex travel requests into actionable, structured itineraries.

---

## System Demonstration

Explore the end-to-end user journey, showcasing intent classification, RAG-based policy retrieval, and dynamic itinerary generation.



https://github.com/user-attachments/assets/019784e6-67ee-4f20-831d-c7d905dcd70e



---

## Key Value Propositions

*   **Seamless Orchestration**: A custom LangGraph workflow manages conversation state, routing user queries between specialized nodes (Policy, Planning, Booking, and General).
*   **Hybrid RAG Engine**: Combines dense and sparse vector search via **Pinecone** to retrieve precise hotel data, travel logistics, and corporate policies.
*   **One-Click Integration**: A self-bootstrapping architecture where the **Streamlit** frontend automatically manages the lifecycle of the **FastAPI** backend.
*   **Curated Local Intelligence**: Integrated datasets for Kathmandu, Pokhara, Chitwan, Lumbini, and Nagarkot, ensuring high-fidelity local recommendations.
*   **Transactional Integrity**: Simulated booking workflows with automated confirmation IDs and agency follow-up triggers.

---

## Architecture & Workflow

The system operates as a **Multi-Node Directed Acyclic Graph (DAG)**:

1.  **Classify Node**: Analyzes user intent using LLM-based few-shot classification.
2.  **Router**: Directs state to the appropriate specialized service.
3.  **Specialized Nodes**:
    *   `Planner`: Extracts constraints and generates time-blocked itineraries.
    *   `Policy`: Answers compliance/refund queries using re-ranked RAG results.
    *   `Booking`: Executes booking logic and returns transactional status.
    *   `General`: Handles chitchat and out-of-scope interactions politely.

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Logic Orchestration** | LangGraph, LangChain |
| **LLM Core** | Google Gemini 2.5 Flash |
| **Backend Framework** | FastAPI (Asynchronous) |
| **Frontend UI** | Streamlit (Custom CSS) |
| **Vector Search** | Pinecone (Hybrid Search) |
| **Caching/Memory** | Redis |
| **Data Models** | Pydantic V2 |

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- Redis Server (local or cloud)
- Pinecone & Google Gemini API Credentials

### Environment Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=tour-planner
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Deployment
```bash
# Clone the repository
git clone https://github.com/your-username/tour_planner.git
cd tour_planner

# Install dependencies
pip install -r requirements.txt

# Launch the unified application
streamlit run app.py
```

---

## Repository Structure

```text
├── alembic/                # Database migration scripts
├── database/               # Database connection and setup
├── dependencies/           # FastAPI dependency injection logic
├── documents/              # Knowledge base (JSON/TXT) for RAG
├── models/                 # SQLAlchemy database models
├── prompts/                # Centralized AI system prompts
├── public/                 # Demo assets and media
├── routes/                 # FastAPI endpoint definitions
├── schemas/                # Pydantic data validation schemas
├── services/               # Core business logic and AI services
├── utils/                  # Shared utility functions (logging, etc.)
├── workflow/               # LangGraph state and node definitions
├── app.py                  # Streamlit frontend & backend controller
├── main.py                 # FastAPI application entry point
├── config.py               # Global configuration and settings
└── requirements.txt        # Project dependencies
```

---

## Evaluation metrics

```text
{
  "ask_booking": {
    "precision": 1.0,
    "recall": 1.0,
    "f1-score": 1.0,
    "support": 14.0
  },
  "cancel_booking": {
    "precision": 1.0,
    "recall": 1.0,
    "f1-score": 1.0,
    "support": 5.0
  },
  "confirm_booking": {
    "precision": 1.0,
    "recall": 1.0,
    "f1-score": 1.0,
    "support": 3.0
  },
  "general": {
    "precision": 0.9230769230769231,
    "recall": 0.96,
    "f1-score": 0.9411764705882353,
    "support": 25.0
  },
  "planning": {
    "precision": 1.0,
    "recall": 1.0,
    "f1-score": 1.0,
    "support": 25.0
  },
  "policy": {
    "precision": 0.9629629629629629,
    "recall": 0.9285714285714286,
    "f1-score": 0.9454545454545454,
    "support": 28.0
  },
  "accuracy": 0.97,
  "macro avg": {
    "precision": 0.9810066476733144,
    "recall": 0.9814285714285714,
    "f1-score": 0.9811051693404634,
    "support": 100.0
  },
  "weighted avg": {
    "precision": 0.9703988603988605,
    "recall": 0.97,
    "f1-score": 0.9700213903743315,
    "support": 100.0
  }
}
```

---

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
