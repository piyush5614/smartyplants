# Copilot Instructions - Smart Plant Health Assistant

## Architecture Overview

Flask monolith with layered architecture: **Routes → Services → Models**. AI-powered plant disease detection using Google Gemini API with internet search grounding.

```
backend/
├── routes/          # API endpoints (Flask Blueprints)
├── services/        # Business logic (analyzers, processors, advisors)
├── models/          # SQLAlchemy ORM + PlantDiseaseDetector
├── prompts/         # AI system/user prompts (keep separate from logic)
├── utils/           # Validators, helpers
└── config.py        # Centralized config from env vars
```

## Key Patterns

### Service Layer Pattern
Services are initialized at module level in routes, not per-request:
```python
# backend/routes/analysis_routes.py
plant_analyzer = PlantAnalyzer()  # Module-level singleton
care_advisor = CareAdvisor()
```

### Two-Step AI Analysis (Gemini)
The `GeminiAnalyzer` uses a two-step process with Google Search grounding:
1. **Image Analysis**: Identify plant species and disease from image
2. **Search Grounding**: Query internet for real treatment/cure information

See [backend/services/gemini_analyzer.py](backend/services/gemini_analyzer.py) for implementation.

### Validator Return Format
All validators return `{'valid': bool, 'error'?: str, ...extra_fields}`:
```python
def validate_file_upload(file) -> dict:
    if not file: return {'valid': False, 'error': 'No file'}
    return {'valid': True}
```

### API Response Format
All API responses include `success` boolean:
```python
return jsonify({'success': True, 'data': ...})
return jsonify({'success': False, 'error': '...'}), 400
```

## Development Commands

```bash
# Start server (from project root)
python run.py                    # Uses .env file automatically

# Run tests
python -m pytest tests/          # From project root

# Install dependencies
pip install -r backend/requirements.txt
```

## Environment Variables

Required for AI features:
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` - Gemini API key for AI analysis
- `OPENAI_API_KEY` - Optional fallback for OpenAI

See [backend/config.py](backend/config.py) for all options.

## Critical Files

| Purpose | File |
|---------|------|
| App factory | [backend/app.py](backend/app.py) - `create_app()` |
| Main API route | [backend/routes/analysis_routes.py](backend/routes/analysis_routes.py) - `/api/v1/analyze` |
| AI prompts | [backend/services/gemini_analyzer.py](backend/services/gemini_analyzer.py) - `IMAGE_ANALYSIS_PROMPT` |
| Care database | [backend/services/care_advisor.py](backend/services/care_advisor.py) - `CARE_DATABASE` dict |
| Config | [backend/config.py](backend/config.py) - All env vars centralized |

## Conventions

- **Imports**: Backend modules use top-level imports (`from config import Config`, not `from backend.config`)
- **Path handling**: Use `pathlib.Path` for all file paths
- **Logging**: Use `logging.getLogger(__name__)` per module
- **Database**: SQLAlchemy models in `models/database_models.py`, use `db.Model` base class
- **API versioning**: All routes under `/api/v1/` via Blueprint prefix
- **File uploads**: Validate with both `validate_file_upload()` AND `validate_image_file()` before processing
