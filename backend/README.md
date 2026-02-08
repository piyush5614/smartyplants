# Smart Plant Health Assistant - Backend API

Professional, secure, and scalable backend for plant health analysis using AI.

## Features

✅ **AI-Powered Analysis** - Uses OpenAI GPT-4 for plant disease detection and health assessment  
✅ **Secure Configuration** - All sensitive data from environment variables, no hardcoded secrets  
✅ **RESTful API** - Clean, well-documented API endpoints  
✅ **Database Models** - SQLAlchemy ORM for data persistence  
✅ **Authentication** - JWT-based user authentication system  
✅ **File Handling** - Secure image upload and processing  
✅ **Error Handling** - Comprehensive error handlers and logging  
✅ **Production Ready** - Deployable to cloud platforms  

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Run

```bash
python app.py
# API available at http://localhost:5000
```

### 3. Test

```bash
# Check health
curl http://localhost:5000/

# Check status
curl http://localhost:5000/api/v1/status
```

## Project Structure

```
backend/
├── app.py                      # Flask application factory
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── CONFIGURATION.md            # Configuration guide
├── DEPLOYMENT.md               # Deployment guide
│
├── models/
│   └── database_models.py      # SQLAlchemy ORM models
│
├── routes/
│   ├── __init__.py
│   ├── health_routes.py        # Health check endpoints
│   ├── analysis_routes.py      # Plant analysis endpoints
│   └── auth_routes.py          # Authentication endpoints
│
├── services/
│   ├── image_processor.py      # Image handling
│   ├── ai_analyzer.py          # OpenAI integration
│   ├── disease_detector.py     # Disease detection logic
│   └── plant_analyzer.py       # Plant analysis engine
│
├── utils/
│   ├── validators.py           # Input validation
│   ├── helpers.py              # Utility functions
│   └── constants.py            # Application constants
│
├── logs/                       # Application logs
└── uploads/                    # User-uploaded images
```

## Configuration

### Required Environment Variables

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

### Optional Environment Variables

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///plant_health.db
MAX_UPLOAD_SIZE_MB=10
AI_CONFIDENCE_THRESHOLD=50.0
```

See [CONFIGURATION.md](CONFIGURATION.md) for complete configuration details.

## API Endpoints

### Status Endpoints

```
GET /                      # API root info
GET /api/v1/status        # API health status
GET /api/v1/config        # Configuration info (non-sensitive)
```

### Authentication Endpoints

```
POST /api/v1/auth/register    # Register new user
POST /api/v1/auth/login       # Login user
POST /api/v1/auth/logout      # Logout user
GET  /api/v1/auth/profile     # Get user profile
```

### Plant Analysis Endpoints

```
POST /api/v1/analyze/image         # Analyze plant image
GET  /api/v1/analyze/history       # Get analysis history
GET  /api/v1/analyze/{id}          # Get specific analysis
```

### Health & Disease Endpoints

```
GET /api/v1/plants                 # List user's plants
POST /api/v1/plants                # Create new plant
PUT  /api/v1/plants/{id}           # Update plant
GET  /api/v1/diseases              # List common diseases
GET  /api/v1/health-status/{id}    # Get plant health status
```

## Development

### Install Development Dependencies

```bash
pip install pytest pytest-cov black pylint flake8
```

### Run Tests

```bash
pytest
pytest --cov=.  # With coverage
```

### Code Style

```bash
black .          # Format code
pylint routes/   # Lint code
flake8 .         # Check style
```

### Enable Debug Mode

```bash
FLASK_ENV=development python app.py
# Debug mode automatically enabled with detailed error messages
```

## Production Deployment

### Prerequisites

- Generate secure SECRET_KEY
- Use PostgreSQL database
- Enable HTTPS
- Set up environment variables

### Deployment Steps

```bash
# 1. Install production server
pip install gunicorn gevent

# 2. Set production variables
export FLASK_ENV=production
export OPENAI_API_KEY=sk-...
export DATABASE_URL=postgresql://...

# 3. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Database

### Models

- **User** - User accounts and authentication
- **Plant** - Plant entries for users
- **Analysis** - Plant analysis results
- **Disease** - Disease information and treatments

### Migrations

Database tables are created automatically on app startup.

For manual database operations:

```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()  # Create tables
    db.session.query(User).all()  # Query data
```

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Human-readable error message",
  "status": 400
}
```

### Common Status Codes

- `200` - Success
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (access denied)
- `404` - Not Found
- `413` - Payload Too Large (file too big)
- `500` - Server Error

## Logging

Logs are saved to `logs/app.log`:

```
2024-01-15 10:30:45 - INFO - Flask app initialized for development environment
2024-01-15 10:30:46 - INFO - Blueprints registered successfully
2024-01-15 10:30:47 - INFO - POST request to /api/v1/analyze/image
```

Change log level with `LOG_LEVEL` environment variable:

```env
LOG_LEVEL=DEBUG    # Verbose logging
LOG_LEVEL=INFO     # Standard logging
LOG_LEVEL=WARNING  # Warnings and errors only
```

## Security Features

✅ **No Hardcoded Secrets** - All sensitive data from environment variables  
✅ **CORS Protection** - Configurable allowed origins  
✅ **CSRF Protection** - Session cookies with SameSite attribute  
✅ **Secure Headers** - HTTP security headers configured  
✅ **Input Validation** - All inputs validated and sanitized  
✅ **Rate Limiting** - Optional rate limiting (configurable)  
✅ **Database Security** - Parameterized queries to prevent SQL injection  

## Performance

- **Image Processing** - Optimized with Pillow and OpenCV
- **Database** - Indexed queries and connection pooling
- **Caching** - Optional response caching
- **Worker Processes** - Multi-worker setup with Gunicorn

## Troubleshooting

### OpenAI API Error

```bash
# Verify API key
echo $OPENAI_API_KEY

# Check API key validity
python -c "
import openai
openai.api_key = 'sk-...'
response = openai.ChatCompletion.create(
    model='gpt-4',
    messages=[{'role': 'user', 'content': 'test'}]
)
"
```

### Database Connection Error

```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
python -c "from sqlalchemy import create_engine; create_engine('your-url').connect()"
```

### Port Already in Use

```bash
# Kill process using port 5000
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
FLASK_PORT=5001 python app.py
```

## Performance Monitoring

### Database Queries

```python
# Enable query logging
app.config['SQLALCHEMY_ECHO'] = True
```

### Request Logging

```python
# Check request log
tail -f logs/app.log
```

### Resource Usage

```bash
# Monitor memory and CPU
watch -n 1 'ps aux | grep gunicorn'
```

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test: `pytest`
3. Format code: `black .`
4. Commit: `git commit -am "Add feature"`
5. Push: `git push origin feature/name`

## Documentation

- [Configuration Guide](CONFIGURATION.md) - Environment variables and settings
- [Deployment Guide](DEPLOYMENT.md) - Production deployment steps
- [API Documentation](API.md) - Detailed endpoint documentation (if available)

## License

MIT License - See LICENSE file for details

## Support

- Check [CONFIGURATION.md](CONFIGURATION.md) for configuration issues
- Review logs in `logs/app.log`
- Test endpoints with `curl` or Postman
- Enable DEBUG mode for detailed error messages

## Next Steps

1. ✅ Review configuration in [CONFIGURATION.md](CONFIGURATION.md)
2. ✅ Setup deployment in [DEPLOYMENT.md](DEPLOYMENT.md)
3. ⚙️ Customize database models in `models/`
4. ⚙️ Implement custom routes in `routes/`
5. ⚙️ Add business logic in `services/`
6. 🚀 Deploy to production
