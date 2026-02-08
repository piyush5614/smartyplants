# Quick Reference Guide

## Getting Started (60 seconds)

```bash
# 1. Navigate to backend
cd backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run server
python app.py
```

✅ Server now running at `http://localhost:5000`

## Configuration Quick Reference

### Must Set
```env
OPENAI_API_KEY=sk-your-key-here
```

### Development Defaults (already set)
```env
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///plant_health.db
LOG_LEVEL=INFO
```

### Common Configuration
```env
# Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database
DATABASE_URL=sqlite:///plant_health.db
# or PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/plant_health

# File uploads
MAX_UPLOAD_SIZE_MB=10

# AI analysis
AI_CONFIDENCE_THRESHOLD=50.0
```

## API Quick Reference

### Check Status
```bash
curl http://localhost:5000/
curl http://localhost:5000/api/v1/status
```

### Response Format
```json
{
  "success": true,
  "data": { /* endpoint-specific data */ }
}

// Error response
{
  "success": false,
  "error": "Error type",
  "message": "Error description"
}
```

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad request (invalid input)
- `401` - Unauthorized (login required)
- `404` - Not found
- `500` - Server error

## Development Commands

### Run Application
```bash
python app.py                    # Development mode
FLASK_ENV=production python app.py    # Production mode
```

### Run Tests
```bash
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest --cov                     # With coverage
```

### Format Code
```bash
black .                          # Auto-format
pylint routes/                   # Lint check
flake8 .                         # Style check
```

### Database
```bash
python -c "from app import create_app, db; app = create_app(); \
  with app.app_context(): db.create_all()"    # Create tables
```

## File Locations

### Configuration
- `config.py` - Configuration class
- `.env` - Environment variables (git-ignored)
- `.env.example` - Template
- `CONFIGURATION.md` - Configuration guide

### Application
- `app.py` - Flask factory
- `models/database_models.py` - Database models
- `routes/` - API endpoints
- `services/` - Business logic

### Logs
- `logs/app.log` - Application log

### Data
- `uploads/` - Uploaded files
- `plant_health.db` - SQLite database

## Common Tasks

### Add Environment Variable
1. Add to `.env`:
   ```env
   MY_VAR=value
   ```
2. Use in code:
   ```python
   from config import Config
   my_var = Config.MY_VAR
   ```

### Create New Route
1. Create in `routes/my_routes.py`:
   ```python
   from flask import Blueprint
   my_bp = Blueprint('my', __name__)
   
   @my_bp.route('/endpoint')
   def my_endpoint():
       return {'success': True}
   ```

2. Register in `app.py`:
   ```python
   from routes.my_routes import my_bp
   app.register_blueprint(my_bp, url_prefix='/api/v1')
   ```

### Add Database Model
1. Create in `models/database_models.py`:
   ```python
   class MyModel(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(255))
   ```

2. Create tables:
   ```python
   with app.app_context():
       db.create_all()
   ```

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"
```bash
# Check .env file has the key
cat .env | grep OPENAI_API_KEY

# Or set directly
export OPENAI_API_KEY=sk-...
```

### Port 5000 already in use
```bash
# Kill process using port
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
FLASK_PORT=5001 python app.py
```

### Database locked/corrupted
```bash
# Remove and recreate
rm plant_health.db
python app.py  # Will recreate on startup
```

### Log file issues
```bash
# Create logs directory
mkdir -p logs
chmod 755 logs
```

## Environment Variables by Use Case

### Local Development
```env
FLASK_ENV=development
DEBUG=True
OPENAI_API_KEY=sk-dev-key
DATABASE_URL=sqlite:///plant_health.db
LOG_LEVEL=DEBUG
```

### Testing
```env
FLASK_ENV=testing
TESTING=True
DATABASE_URL=sqlite:///:memory:
LOG_LEVEL=WARNING
```

### Production
```env
FLASK_ENV=production
DEBUG=False
OPENAI_API_KEY=sk-prod-key
DATABASE_URL=postgresql://user:pass@host/db
SESSION_COOKIE_SECURE=True
LOG_LEVEL=WARNING
```

## Important Classes & Functions

### Config Class
```python
from config import Config

Config.OPENAI_API_KEY          # Get API key
Config.validate_required_keys() # Validate setup
Config.init_directories()       # Create folders
Config.to_dict()               # Get non-sensitive config
```

### Create App
```python
from app import create_app

app = create_app('development')  # Create Flask app
app = create_app('production')   # Production version
```

### Database
```python
from models.database_models import db, User, Plant

db.session.query(User).all()              # Get all users
db.session.add(user)                      # Add object
db.session.commit()                       # Save changes
db.session.rollback()                     # Undo changes
```

## Useful Links

- [Configuration Guide](CONFIGURATION.md) - Detailed config options
- [Deployment Guide](DEPLOYMENT.md) - How to deploy
- [README](README.md) - Full project overview
- [Flask Docs](https://flask.palletsprojects.com/) - Flask documentation
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/) - Database ORM

## Performance Tips

1. **Use database indices** for frequently searched fields
2. **Enable caching** for expensive operations
3. **Limit log verbosity** (DEBUG only in development)
4. **Use connection pooling** for databases
5. **Set appropriate timeouts** for external APIs

## Security Reminders

⚠️ **Never commit .env files**  
⚠️ **Never log sensitive data**  
⚠️ **Always validate user input**  
⚠️ **Use parameterized queries**  
⚠️ **Enable HTTPS in production**  
⚠️ **Rotate API keys regularly**  

## Getting Help

1. Check logs: `tail -f logs/app.log`
2. Test API: `curl http://localhost:5000/api/v1/status`
3. Check config: `curl http://localhost:5000/api/v1/config`
4. Read docs: See README.md, CONFIGURATION.md, DEPLOYMENT.md
5. Enable debug: `LOG_LEVEL=DEBUG` in .env

## Next Steps

After setup:
1. ✅ Read [README.md](README.md) - Project overview
2. ✅ Check [CONFIGURATION.md](CONFIGURATION.md) - All options
3. ⚙️ Review [DEPLOYMENT.md](DEPLOYMENT.md) - For production
4. ⚙️ Integrate routes and services
5. 🚀 Deploy to production
