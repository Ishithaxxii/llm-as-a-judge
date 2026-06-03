# LLM as a Judge

Automated evaluation pipeline using Large Language Models to benchmark AI-generated responses for:

- Relevance
- Coherence
- Accuracy
- Completeness
- Safety

## Features

- Automated LLM evaluation
- Configurable rubric-based scoring
- OpenAI API integration
- Batch dataset evaluation
- JSON report generation
- REST API using FastAPI
- CLI evaluation support
- GitHub-ready structure

## Tech Stack

- Python 3.11+
- FastAPI
- OpenAI API
- Pydantic
- NLP evaluation workflows
- Prompt Engineering
- JSON
- Git

## Project Structure

```bash
llm_as_a_judge/
├── app/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── prompts/
│   ├── schemas/
│   └── main.py
├── datasets/
├── reports/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/llm-as-a-judge.git
cd llm-as-a-judge
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create `.env`

```env
OPENAI_API_KEY=your_api_key_here
```

## Run API

```bash
uvicorn app.main:app --reload
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

## Run Evaluation

```bash
python run_evaluation.py
```

## Example Dataset

```json
[
  {
    "question": "What is machine learning?",
    "reference_answer": "Machine learning is a subset of AI...",
    "model_answer": "Machine learning enables systems to learn from data..."
  }
]
```

## Example Output

```json
{
  "relevance": 9,
  "coherence": 8,
  "accuracy": 9,
  "completeness": 8,
  "overall_score": 8.5,
  "feedback": "Strong response with accurate explanation."
}
```

## Future Improvements

- Multi-model benchmarking
- Human evaluation comparison
- LangChain integration
- Vector database support
- Dashboard analytics
- RAG evaluation support

## License

MIT
# llm-as-a-judge
