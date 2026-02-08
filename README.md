# Smart Plant Health Assistant

**AI-Powered Plant Disease Detection & Care Advisory System**

---

## 🌱 Project Overview

Smart Plant Health Assistant is a comprehensive solution that helps farmers and gardeners identify plant diseases using AI image analysis and provides personalized, actionable care recommendations.

### Key Features

✨ **Disease Detection**
- AI-powered image analysis for accurate disease identification
- Multi-prediction results with confidence scores
- Supports 8+ plant diseases and healthy plant detection

✨ **Intelligent Care Advisory**
- Personalized treatment recommendations (organic & chemical)
- Watering and fertilizing guides
- Recovery timeline and monitoring schedule

✨ **User-Friendly Interface**
- Drag-and-drop image upload
- Real-time analysis results
- Responsive design (mobile & desktop)

✨ **Professional Backend**
- RESTful API architecture
- Database history tracking
- Batch image analysis

---

## 📁 Project Structure

```
smart-plant-health-assistant/
├── backend/                      # Flask API Backend
│   ├── app.py                   # Flask application factory
│   ├── config.py                # Configuration management
│   ├── requirements.txt          # Python dependencies
│   │
│   ├── models/                  # AI/ML & Database Models
│   │   ├── plant_disease_detector.py  # Disease detection engine
│   │   └── database_models.py         # SQLAlchemy models
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── image_processor.py   # Image validation & preprocessing
│   │   ├── plant_analyzer.py    # Analysis orchestration
│   │   └── care_advisor.py      # Care recommendation engine
│   │
│   ├── routes/                  # API Endpoints
│   │   ├── health_routes.py     # Health check endpoints
│   │   └── analysis_routes.py   # Analysis & detection endpoints
│   │
│   ├── database/                # Database Management
│   │   └── db_manager.py        # Database operations
│   │
│   └── utils/                   # Utilities
│       ├── validators.py         # Input validation
│       └── helpers.py            # Helper functions
│
├── frontend/                     # Web UI
│   ├── index.html               # Main interface
│   ├── js/
│   │   └── app.js               # Frontend logic
│   ├── css/
│   │   └── styles.css           # Styling
│   └── assets/                  # Images, icons
│
├── tests/                       # Test Suite
│   ├── test_detector.py         # Detector tests
│   └── test_validators.py       # Validator tests
│
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file

```

### Architecture Highlights

**Separation of Concerns:**
- **Models**: AI/ML logic and database schemas
- **Services**: Business logic (image processing, analysis, recommendations)
- **Routes**: API endpoints
- **Utils**: Reusable validators and helpers
- **Frontend**: Clean UI with vanilla JavaScript

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Backend Setup

1. **Clone/Navigate to project:**
   ```bash
   cd smart-plant-health-assistant/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Flask application:**
   ```bash
   python app.py
   ```
   
   Server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd smart-plant-health-assistant/frontend
   ```

2. **Open in browser:**
   - Simply open `index.html` in your web browser
   - Or use a local server: `python -m http.server 8000`
   - Access at `http://localhost:8000`

---

## 📖 API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Endpoints

#### 1. Health Check
```
GET /health
```
Returns service status and information.

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart Plant Health Assistant",
  "version": "1.0.0"
}
```

#### 2. Analyze Plant Image
```
POST /analyze
```
Analyze a plant image for disease detection.

**Parameters:**
- `file` (required): Image file (PNG, JPG, GIF, WEBP)
- `confidence_threshold` (optional): Float between 0.0-1.0 (default: 0.7)

**Example:**
```bash
curl -X POST \
  -F "file=@plant.jpg" \
  -F "confidence_threshold=0.7" \
  http://localhost:5000/api/v1/analyze
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "disease_detection": {
      "primary_disease": "leaf_spot",
      "confidence": 0.89,
      "severity": "moderate",
      "description": "Circular or irregular brown/black spots on leaves"
    },
    "predictions": [...]
  },
  "care_plan": {
    "immediate_actions": [...],
    "treatment": {...},
    "watering": {...}
  }
}
```

#### 3. Get Disease List
```
GET /diseases
```
Get all detectable diseases and their characteristics.

#### 4. Analysis History
```
GET /history/<session_id>
```
Retrieve analysis history for a session.

---

## 🎯 How to Use

### For Users

1. **Upload Image**
   - Click upload zone or drag & drop a plant image
   - Ensure image is clear and well-lit

2. **Analyze**
   - Click "Analyze Plant" button
   - Wait for AI analysis (5-10 seconds)

3. **Review Results**
   - See disease detection with confidence score
   - View severity level and common causes
   - Check all alternative predictions

4. **Follow Care Plan**
   - Read priority actions
   - Follow watering/fertilizing schedule
   - Monitor plant based on timeline

### For Developers

1. **Extend Models**
   - Add new diseases to `DISEASE_DATABASE` in `plant_disease_detector.py`
   - Update `CARE_DATABASE` in `care_advisor.py`

2. **Customize Analysis**
   - Modify feature extraction in `image_processor.py`
   - Adjust disease classification in `plant_analyzer.py`

3. **Add Features**
   - Create new routes in `routes/`
   - Add services in `services/`
   - Update database models as needed

---

## 🧪 Testing

Run tests:
```bash
cd backend
python -m pytest tests/
```

Or run specific test:
```bash
python -m pytest tests/test_detector.py -v
```

---

## 🔧 Configuration

Edit `.env` file to customize:

```ini
FLASK_ENV=development              # Environment
SECRET_KEY=your-secret-key         # Flask secret
DATABASE_URL=sqlite:///plant_health.db  # Database
CONFIDENCE_THRESHOLD=0.7           # Default confidence
MAX_UPLOAD_SIZE=5242880            # Max file size (5MB)
```

---

## 📊 Supported Diseases

| Disease | Severity | Confidence |
|---------|----------|-----------|
| Healthy | None | Variable |
| Leaf Spot | Moderate | 0.75-0.95 |
| Powdery Mildew | Moderate | 0.70-0.90 |
| Rust | Moderate | 0.70-0.90 |
| Blight | Severe | 0.80-0.99 |
| Yellowing | Mild | 0.65-0.85 |
| Wilting | Severe | 0.70-0.90 |
| Pest Damage | Moderate | 0.60-0.85 |

---

## 🛠️ Technology Stack

**Backend:**
- Flask (Web framework)
- SQLAlchemy (ORM)
- OpenCV (Image processing)
- NumPy (Numerical computation)
- TensorFlow/Keras (AI/ML - optional for advanced models)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript
- Bootstrap 5
- FontAwesome Icons

**Database:**
- SQLite (default, easily switch to PostgreSQL)

---

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 📝 Future Enhancements

- [ ] Integration with external ML models (TensorFlow, PyTorch)
- [ ] User authentication and personalization
- [ ] Mobile app (React Native/Flutter)
- [ ] Plant growth tracking over time
- [ ] Community disease reporting
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Integration with garden management features

---

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created for the Hackathon Practice Challenge - Smart Plant Health Assistant

---

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Check documentation in README
- Review code comments for implementation details

---

## 🙏 Acknowledgments

- Built with ❤️ for plant lovers
- Inspired by agricultural technology innovations
- Special thanks to the open-source community

---

**Made with 🌱 by AI Developers**
