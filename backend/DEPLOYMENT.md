# Deployment & Startup Guide

## Overview

This guide covers setting up, configuring, and deploying the Smart Plant Health Assistant backend.

## Prerequisites

- Python 3.8+
- pip or conda
- OpenAI API key
- PostgreSQL (optional, for production)

## Local Development Setup

### 1. Clone and Navigate

```bash
cd smart-plant-health-assistant/backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 5. Initialize Database

```bash
# The app will auto-create tables on startup
# To verify database setup:
python -c "from app import create_app; app = create_app(); print('Database ready')"
```

### 6. Run Development Server

```bash
python app.py
# Server runs at http://localhost:5000
```

## Testing the API

### Health Check

```bash
curl http://localhost:5000/
# Returns API status
```

### API Status

```bash
curl http://localhost:5000/api/v1/status
# Returns database health and timestamp
```

### Configuration Info (Non-sensitive)

```bash
curl http://localhost:5000/api/v1/config
# Returns public configuration
```

## Environment Variables

### Development

```env
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=True
OPENAI_API_KEY=sk-your-dev-key
DATABASE_URL=sqlite:///plant_health.db
LOG_LEVEL=DEBUG
```

### Production

```env
FLASK_ENV=production
DEBUG=False
OPENAI_API_KEY=sk-your-prod-key
DATABASE_URL=postgresql://user:pass@prod-host/db
SESSION_COOKIE_SECURE=True
LOG_LEVEL=WARNING
```

## Production Deployment

### 1. Security Checklist

- [ ] Change SECRET_KEY to a secure random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set DEBUG=False
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Use environment variables from secure vault
- [ ] Enable HTTPS on web server
- [ ] Configure CORS properly
- [ ] Setup database backups
- [ ] Enable logging and monitoring

### 2. Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env
```

### 3. Setup PostgreSQL Database

```bash
# Create database
createdb plant_health

# Set DATABASE_URL
DATABASE_URL=postgresql://username:password@localhost:5432/plant_health
```

### 4. Install Production Dependencies

```bash
pip install gunicorn gevent
```

### 5. Run with Gunicorn

```bash
# Basic
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()

# With Gevent
gunicorn -w 4 -k gevent -b 0.0.0.0:5000 app:create_app()

# With worker restart on code change
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 60 --access-logfile - app:create_app()
```

## Docker Deployment

### Build Docker Image

```bash
# Create Dockerfile
docker build -t plant-health-assistant:latest .

# Run container
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  -e DATABASE_URL=postgresql://... \
  -e FLASK_ENV=production \
  plant-health-assistant:latest
```

## Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create plant-health-assistant

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set DATABASE_URL=postgresql://...
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### AWS EC2

```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Install Python and dependencies
sudo yum install python3 python3-pip
pip install -r requirements.txt

# Setup environment
nano .env

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Azure App Service

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create app service plan
az appservice plan create --name myPlan --resource-group myResourceGroup --sku B1 --is-linux

# Create web app
az webapp create --resource-group myResourceGroup --plan myPlan --name plant-health-assistant --runtime "PYTHON|3.11"

# Deploy
git push azure main
```

## Monitoring & Logging

### Check Application Logs

```bash
# Development
tail -f logs/app.log

# Heroku
heroku logs --tail

# Docker
docker logs container-id
```

### Enable Debug Logging

```env
LOG_LEVEL=DEBUG
```

### Monitor Database

```bash
# SQLite size
ls -lh plant_health.db

# PostgreSQL connections
psql -U username -d plant_health -c "SELECT * FROM pg_stat_activity;"
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 PID

# Or use different port
FLASK_PORT=5001 python app.py
```

### Database Connection Error

```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test PostgreSQL connection
psql $DATABASE_URL -c "SELECT 1;"
```

### OpenAI API Error

```bash
# Verify API key
echo $OPENAI_API_KEY

# Test OpenAI connection
python -c "
import openai
openai.api_key = 'sk-...'
print(openai.Model.list())
"
```

### Import Errors

```bash
# Verify all dependencies installed
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## Performance Optimization

### 1. Database Indexing

For production, add database indices:

```python
# In models/database_models.py
class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    name = db.Column(db.String(255), index=True)
```

### 2. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/plants')
@cache.cached(timeout=300)
def get_plants():
    # Cached for 5 minutes
    pass
```

### 3. Increase Worker Count

```bash
# For CPU-bound tasks
gunicorn -w $(nproc) app:create_app()
```

## Backup & Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump plant_health > backup.sql

# Restore
psql plant_health < backup.sql

# SQLite backup
cp plant_health.db plant_health.db.backup
```

### File Backup

```bash
# Backup uploads
tar -czf uploads_backup.tar.gz uploads/

# Restore
tar -xzf uploads_backup.tar.gz
```

## Next Steps

1. Read [CONFIGURATION.md](CONFIGURATION.md) for detailed configuration
2. Check API documentation for available endpoints
3. Setup monitoring and alerting
4. Configure automated backups
5. Setup CI/CD pipeline

## Support

For issues:
1. Check logs: `tail -f logs/app.log`
2. Verify configuration: `curl http://localhost:5000/api/v1/config`
3. Test connectivity: `curl http://localhost:5000/api/v1/status`
