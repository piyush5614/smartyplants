# Configuration Guide

## Overview

The Smart Plant Health Assistant uses a centralized configuration system based on environment variables. This ensures:

- **Security**: No hardcoded secrets
- **Flexibility**: Different settings for development, testing, and production
- **Simplicity**: Easy to manage across environments

## Quick Start

### 1. Setup Environment Variables

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your values
# Most importantly, add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Required Configuration

The following environment variables are **required**:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | `sk-...` |

### 3. Optional Configuration

All other variables have sensible defaults. Common optional variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | `development` | Environment mode |
| `DATABASE_URL` | `sqlite:///plant_health.db` | Database connection |
| `OPENAI_MODEL` | `gpt-4` | AI model to use |
| `MAX_UPLOAD_SIZE_MB` | `10` | Max file upload size |
| `AI_CONFIDENCE_THRESHOLD` | `50.0` | Confidence threshold (%) |

## Configuration Levels

### Development Environment

```bash
FLASK_ENV=development
DEBUG=True
OPENAI_API_KEY=your-dev-key
DATABASE_URL=sqlite:///plant_health.db
```

### Production Environment

```bash
FLASK_ENV=production
DEBUG=False
OPENAI_API_KEY=your-prod-key
DATABASE_URL=postgresql://user:pass@host/db
SESSION_COOKIE_SECURE=True
# Use environment variables from a secure vault
```

## Configuration Files

### `config.py`

Main configuration module. Key classes:

- **`Config`**: Base configuration with all settings
  - `validate_required_keys()`: Validates required environment variables
  - `init_directories()`: Creates required directories
  - `to_dict()`: Returns non-sensitive config as dictionary

### `app.py`

Flask application factory:

- `create_app(env)`: Creates configured Flask app
- `_configure_logging()`: Sets up logging
- `_register_blueprints()`: Registers API routes
- `_register_error_handlers()`: Sets up error handling

## Security Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore should include:
.env
*.key
*.pem
```

### 2. Use Strong Secret Keys

```bash
# Generate a secure key:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Different Credentials Per Environment

- Development: Test API keys
- Production: Real API keys from secure vault

### 4. Enable HTTPS in Production

```bash
SESSION_COOKIE_SECURE=True
```

## Environment Variable Categories

### Flask Configuration

```
FLASK_ENV              # development | testing | production
FLASK_HOST             # Server host (default: 0.0.0.0)
FLASK_PORT             # Server port (default: 5000)
SECRET_KEY             # Session encryption key
DEBUG                  # Enable debug mode
TESTING                # Enable testing mode
```

### Database Configuration

```
DATABASE_URL           # Connection string
                       # SQLite: sqlite:///plant_health.db
                       # PostgreSQL: postgresql://user:pass@host/db
```

### OpenAI Configuration

```
OPENAI_API_KEY         # Your OpenAI API key (REQUIRED)
OPENAI_MODEL           # Model to use (default: gpt-4)
OPENAI_TIMEOUT         # Request timeout in seconds
```

### File Upload Configuration

```
UPLOAD_FOLDER          # Where to store uploaded images
MAX_UPLOAD_SIZE_MB     # Maximum file size in MB
IMAGE_QUALITY          # JPEG quality (0-100)
ALLOWED_EXTENSIONS     # File extensions (set in code)
```

### AI Analysis Configuration

```
AI_CONFIDENCE_THRESHOLD    # Minimum confidence score (%)
AI_HEALTH_CRITICAL         # Critical health threshold (%)
AI_HEALTH_POOR             # Poor health threshold (%)
```

### Security & Session Configuration

```
SESSION_COOKIE_SECURE      # HTTPS only (True in production)
SESSION_COOKIE_HTTPONLY    # JavaScript cannot access (always True)
SESSION_COOKIE_SAMESITE    # CSRF protection (Lax | Strict)
PERMANENT_SESSION_LIFETIME # Session duration (seconds)
AUTH_ENABLED               # Enable authentication
GUEST_MODE_ENABLED         # Allow guest access
```

### Logging Configuration

```
LOG_LEVEL              # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FILE               # Path to log file
```

### API Configuration

```
API_TIMEOUT            # Request timeout (seconds)
CORS_ORIGINS           # Allowed CORS origins (comma-separated)
```

## Validation & Startup

When the application starts, it:

1. **Loads configuration** from environment variables
2. **Validates required settings** (raises error if missing)
3. **Creates required directories** (uploads, logs)
4. **Initializes database** (creates tables if needed)
5. **Logs configuration** (non-sensitive values only)

## Using Configuration in Code

### In Route Handlers

```python
from flask import current_app

@my_blueprint.route('/api/analyze')
def analyze():
    max_size = current_app.config['MAX_UPLOAD_SIZE']
    timeout = current_app.config['API_TIMEOUT']
    # Use configuration...
```

### In Services/Models

```python
from config import Config

class PlantAnalyzer:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
```

## Troubleshooting

### Error: "Missing required environment variables"

**Solution**: Add missing variables to `.env` file:

```bash
OPENAI_API_KEY=sk-your-key-here
```

### Error: "Cannot connect to database"

**Solution**: Verify `DATABASE_URL` is correct:

```bash
# For SQLite (must exist):
DATABASE_URL=sqlite:///plant_health.db

# For PostgreSQL:
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
```

### Error: "File upload fails"

**Solution**: Check `UPLOAD_FOLDER` exists and is writable:

```bash
# Create directory:
mkdir -p uploads
chmod 755 uploads
```

### Logging not appearing

**Solution**: Check `LOG_LEVEL` and `LOG_FILE`:

```bash
LOG_LEVEL=DEBUG        # More verbose logging
LOG_FILE=./logs/app.log
mkdir -p logs
```

## Configuration for Deployment

### Docker

```dockerfile
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://...
ENV OPENAI_API_KEY=...
```

### Heroku

```bash
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=sk-...
```

### AWS/Azure

Use their secret management services:
- AWS Secrets Manager
- Azure Key Vault
- Environment-specific configuration

## See Also

- [config.py](config.py) - Configuration implementation
- [app.py](app.py) - Application factory
- [.env.example](.env.example) - Environment template
