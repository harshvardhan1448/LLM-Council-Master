# LLM Council

![llmcouncil](header.jpg)

A sophisticated multi-stage deliberation system where multiple LLMs collaborate to answer questions better than any single model. Instead of asking one LLM provider, group multiple models into a "Council" for more comprehensive, well-reasoned responses. This is a modern web app (similar to ChatGPT) that uses OpenRouter to orchestrate parallel queries, peer review, and synthesis.

## How It Works

When you submit a question, the Council deliberates in 3 stages:

1. **Stage 1: First Opinions**
   - Query all council models in parallel
   - Each model responds independently
   - Responses displayed in tabs for side-by-side comparison

2. **Stage 2: Peer Review & Ranking**
   - Models anonymously evaluate each other's responses (no favoritism)
   - Models rank responses by accuracy and insight
   - Aggregate rankings computed across all peer evaluations
   - Anonymous labels (A, B, C) shown to models; real names shown to users

3. **Stage 3: Chairman Synthesis**
   - Designated chairman model synthesizes all responses and rankings
   - Produces a final, comprehensive answer
   - **Resilient fallback**: If chairman fails, automatically uses next-best council member or highest-ranked Stage 1 response

## Recent Improvements

- **Robust Stage 3 Synthesis**: Multi-level fallback ensures users always get an answer
- **Efficient Token Usage**: Max token limits respect API credit budgets
- **Better Error Handling**: Graceful degradation when models fail
- **Real Working Models**: Updated to working OpenRouter endpoints (llama-3.3, mistral-nemo)

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

Get your API key at [openrouter.ai](https://openrouter.ai/). Make sure to purchase the credits you need, or sign up for automatic top up.

### 3. Configure Models (Optional)

Edit `backend/config.py` to customize the council. Default models are optimized for cost/quality on OpenRouter:

```python
COUNCIL_MODELS = [
    "meta-llama/llama-3.3-70b-instruct",
    "mistralai/mistral-nemo",
]

CHAIRMAN_MODEL = "meta-llama/llama-3.3-70b-instruct"
```

**Tips for model selection:**
- Use proven working model IDs from [OpenRouter's model directory](https://openrouter.ai/)
- Council should have 2-4 diverse models for best results
- Chairman can be same as or different from council members
- Note: Max tokens is set to 8000 to manage API costs

## Running the Application

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Run manually**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx for concurrent API calls
- **Frontend:** React + Vite, React-Markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
- **API Provider:** OpenRouter (unified interface to 200+ LLMs)

## Architecture Details

### Backend (`backend/`)

- **`config.py`**: Model configuration and API keys
- **`openrouter.py`**: HTTP client for OpenRouter API with error handling and token limits
- **`council.py`**: 3-stage orchestration logic
  - `stage1_collect_responses()`: Parallel queries with graceful fallback
  - `stage2_collect_rankings()`: Anonymized peer review and ranking
  - `stage3_synthesize_final()`: **Multi-level fallback synthesis** 
    - Tries chairman → council members → best available Stage 1 response
  - `_pick_best_available_response()`: Intelligent response selection based on rankings
- **`storage.py`**: Conversation persistence as JSON
- **`main.py`**: FastAPI endpoints with streaming support (SSE)

### Frontend (`frontend/src/`)

- **Streaming UI**: Real-time updates as each stage completes
- **Tab-based Views**: Side-by-side model comparison
- **Anonymous Display**: Original evaluations used anonymous labels, real names shown to user
- **Aggregate Rankings**: Visual summary of peer evaluation consensus

### Resilience Features

✅ **Stage 1**: Continues if individual models fail (graceful degradation)  
✅ **Stage 2**: Handles malformed rankings with regex fallback  
✅ **Stage 3**: Multi-tier fallback ensures response even if all synthesis attempts fail  
✅ **Tokens**: Max 8000 tokens per request limits costs  
✅ **Validation**: Token count checked against available credits before API calls

## Troubleshooting

### "All models failed to respond"
- Check `.env` has valid `OPENROUTER_API_KEY`
- Verify OpenRouter account has credits
- Confirm model IDs in `backend/config.py` are valid on OpenRouter
- Check model IDs don't use `:free` suffix if endpoints don't support it

### Backend won't start on port 8001
```powershell
# Kill process using port 8001
Get-NetTCPConnection -LocalPort 8001 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Restart backend
python -m backend.main
```

### Models timing out
- Increase `timeout` parameter in `query_model()` calls (default 120 seconds)
- Use faster models for testing
- Check OpenRouter status page for outages

## Example Conversations

The app stores conversations in `data/conversations/` as JSON files with full Stage 1/2/3 outputs, allowing you to:
- Review how each model performed
- Analyze peer rankings and consensus
- Compare synthesized answers across different model combinations

## Contributing & Customization

This project is designed to be easily customizable:
- **Swap models**: Edit `backend/config.py`
- **Adjust prompts**: Modify Stage 2 ranking prompt in `council.py:stage2_collect_rankings()`
- **Change styling**: Edit `frontend/src/*.css`
- **Add features**: Backend is FastAPI, frontend is React—both extensible

## Project Philosophy

LLM Council explores a key insight: **no single LLM is best for all questions**. By combining multiple models and letting them review each other (anonymously), you get:

- **Better answers** through diverse perspectives
- **Higher confidence** from consensus-based rankings
- **Transparency** in how each model evaluated others
- **Cost-effectiveness** by choosing right-sized models

Originally inspired by the idea of reading books and documents collaboratively with multiple LLMs to get richer analysis and insights.

## License

This project is provided as-is for inspiration and educational purposes. Feel free to fork, modify, and build upon it for your own needs.
