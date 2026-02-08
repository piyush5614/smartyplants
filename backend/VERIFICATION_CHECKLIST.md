# Setup Verification Checklist

Use this checklist to verify your setup is working correctly.

## ✅ Installation Verification

### Python & Virtual Environment
- [ ] Python 3.8+ installed: `python --version`
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Pip up to date: `pip install --upgrade pip`

### Dependencies
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Flask installed: `pip show Flask`
- [ ] SQLAlchemy installed: `pip show SQLAlchemy`
- [ ] All requirements installed: `pip list | wc -l`

## ✅ Configuration Verification

### Environment Setup
- [ ] `.env` file created from `.env.example`
- [ ] `OPENAI_API_KEY` is set in `.env`
- [ ] `OPENAI_API_KEY` is valid (test with `python -c "import openai; openai.api_key='sk-...'; print('Valid')"`
- [ ] Other important variables set (DATABASE_URL, etc.)

### Configuration Loading
- [ ] Config loads without errors:
  ```bash
  python -c "from config import Config; print('Config OK')"
  ```
- [ ] Required keys validated:
  ```bash
  python -c "from config import Config; Config.validate_required_keys(); print('Validation OK')"
  ```
- [ ] Directories created:
  ```bash
  python -c "from config import Config; Config.init_directories(); print('Directories OK')"
  ```

## ✅ Flask Application Verification

### App Creation
- [ ] App creates without errors:
  ```bash
  python -c "from app import create_app; app = create_app('development'); print('App created OK')"
  ```
- [ ] App configuration loads:
  ```bash
  python -c "from app import create_app; app = create_app(); print(app.config.get('DEBUG'))"
  ```

### Database
- [ ] Database initializes:
  ```bash
  python -c "from app import create_app; app = create_app(); print('DB OK')"
  ```
- [ ] Database tables exist:
  ```bash
  # Check for .db file (SQLite) or verify connection (PostgreSQL)
  ls -la plant_health.db
  ```

### Logging
- [ ] Log directory exists: `ls -la logs/`
- [ ] Logging configured: `python -c "from app import create_app; app = create_app(); print(app.logger.level)"`

## ✅ API Verification

### Server Startup
- [ ] Server starts: `python app.py`
- [ ] Server accessible: `curl http://localhost:5000/`
- [ ] API version returned: Check response includes `"status": "operational"`

### Status Endpoints
- [ ] Root endpoint works:
  ```bash
  curl http://localhost:5000/
  ```
- [ ] Status endpoint works:
  ```bash
  curl http://localhost:5000/api/v1/status
  ```
- [ ] Config endpoint works:
  ```bash
  curl http://localhost:5000/api/v1/config
  ```

### Health Checks
- [ ] Response format is JSON
- [ ] Status code is 200
- [ ] All expected fields present
- [ ] Timestamp is current

## ✅ Error Handling Verification

### Test 400 Error
```bash
curl -X POST http://localhost:5000/api/v1/analyze -H "Content-Type: application/json"
# Should return 400 with proper error message
```

### Test 404 Error
```bash
curl http://localhost:5000/api/nonexistent
# Should return 404 with proper error message
```

### Test Error Format
- [ ] Error responses have `"success": false`
- [ ] Error responses include error message
- [ ] Error responses include status code

## ✅ File Structure Verification

### Required Files Present
- [ ] `app.py` exists
- [ ] `config.py` exists
- [ ] `requirements.txt` exists
- [ ] `.env` exists (created from `.env.example`)

### Required Directories
- [ ] `models/` directory exists
- [ ] `routes/` directory exists
- [ ] `services/` directory exists
- [ ] `utils/` directory exists
- [ ] `logs/` directory exists (created on startup)
- [ ] `uploads/` directory exists (created on startup)

### Documentation Files
- [ ] `README.md` exists
- [ ] `CONFIGURATION.md` exists
- [ ] `DEPLOYMENT.md` exists
- [ ] `QUICK_REFERENCE.md` exists

## ✅ Security Verification

### Secrets Management
- [ ] `.env` is in `.gitignore` (not committed)
- [ ] `OPENAI_API_KEY` not in any source files
- [ ] No secrets logged: `grep -r "sk-" logs/`
- [ ] Environment-based configuration working

### Database Security
- [ ] Using environment variable for `DATABASE_URL`
- [ ] Not using hardcoded credentials
- [ ] Connection string not in logs

## ✅ Feature Verification

### Configuration Features
- [ ] `Config.validate_required_keys()` works
- [ ] `Config.init_directories()` creates folders
- [ ] `Config.to_dict()` returns non-sensitive config
- [ ] Environment variables read correctly

### Flask Features
- [ ] App factory pattern working
- [ ] CORS configured
- [ ] Error handlers registered
- [ ] Status endpoints available

### Database Features
- [ ] SQLAlchemy initialized
- [ ] Database models defined
- [ ] Tables created on startup

## ✅ Development Verification

### Code Quality
- [ ] Code follows Python conventions
- [ ] No obvious syntax errors
- [ ] Proper error handling in place
- [ ] Logging used appropriately

### Testing
- [ ] Can run `pytest` (if installed)
- [ ] Test endpoints respond correctly
- [ ] Error scenarios handled properly

## ✅ Documentation Verification

### README
- [ ] Features listed
- [ ] Quick start included
- [ ] Configuration section present
- [ ] Deployment information included

### CONFIGURATION.md
- [ ] All settings documented
- [ ] Examples provided
- [ ] Troubleshooting section included
- [ ] Best practices explained

### DEPLOYMENT.md
- [ ] Deployment steps clear
- [ ] Multiple platforms covered
- [ ] Security checklist included
- [ ] Troubleshooting included

### QUICK_REFERENCE.md
- [ ] Quick start guide (60 seconds)
- [ ] Common commands documented
- [ ] Troubleshooting tips included
- [ ] Environment variable templates provided

## ✅ Integration Points Ready

### Routes Ready For Integration
- [ ] `routes/health_routes.py` (can be imported)
- [ ] `routes/analysis_routes.py` (can be imported)
- [ ] `routes/auth_routes.py` (can be imported)

### Services Ready For Integration
- [ ] `services/ai_analyzer.py` (can import Config)
- [ ] `services/image_processor.py` (has dependencies)
- [ ] `services/disease_detector.py` (ready to use)

### Models Ready
- [ ] `models/database_models.py` (db initialized)
- [ ] Can query and add models
- [ ] Relationships defined

## Verification Commands Summary

```bash
# Quick verification script
echo "=== Python ==="
python --version

echo "=== Virtual Env ==="
which python

echo "=== Config ==="
python -c "from config import Config; Config.validate_required_keys(); print('✓ Config OK')"

echo "=== App ==="
python -c "from app import create_app; create_app(); print('✓ App OK')"

echo "=== API ==="
# In another terminal:
python app.py &
sleep 2
curl http://localhost:5000/api/v1/status
echo "✓ API OK"

echo "=== All Checks Complete ==="
```

## Troubleshooting

### If Config fails
1. Check `.env` file exists: `ls -la .env`
2. Verify `OPENAI_API_KEY` is set: `grep OPENAI_API_KEY .env`
3. Check file is readable: `file .env`

### If App fails
1. Check Flask installed: `pip show Flask`
2. Check config loads: `python -c "from config import Config"`
3. Check database directory: `ls -la logs/`

### If API fails
1. Check port not in use: `lsof -i :5000`
2. Check server started: `python app.py` (in debug mode)
3. Check logs: `tail -f logs/app.log`

### If Documentation missing
1. Check files exist: `ls -la *.md`
2. Verify paths in files
3. Check markdown formatting

## Next Steps After Verification

- [ ] Read [README.md](README.md) - Full overview
- [ ] Study [CONFIGURATION.md](CONFIGURATION.md) - All options
- [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md) - Production steps
- [ ] Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Daily reference
- [ ] Integrate routes and services
- [ ] Add custom business logic
- [ ] Deploy to production

## Success Criteria

You have successfully completed Phase 9 when:

✅ All files and directories exist  
✅ Configuration loads without errors  
✅ Flask app creates successfully  
✅ API endpoints respond (status, config)  
✅ Error handling works correctly  
✅ Documentation is complete  
✅ Environment variables are secure  
✅ Database is initialized  
✅ Logging is configured  
✅ Ready for integration testing  

## Support Resources

- [README.md](README.md) - Project overview
- [CONFIGURATION.md](CONFIGURATION.md) - Detailed config guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Daily reference
- [PHASE_9_SUMMARY.md](../PHASE_9_SUMMARY.md) - What was completed
