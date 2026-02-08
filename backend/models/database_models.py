"""Database models for storing plant analysis and history."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PlantAnalysis(db.Model):
    """Model to store individual plant analysis results."""
    
    __tablename__ = 'plant_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    plant_type = db.Column(db.String(100))
    disease_detected = db.Column(db.String(255))
    confidence_score = db.Column(db.Float)
    severity_level = db.Column(db.String(50))  # mild, moderate, severe
    analysis_details = db.Column(db.Text)  # JSON string with detailed analysis
    recommended_actions = db.Column(db.Text)  # JSON string with care advice
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlantAnalysis {self.id}: {self.disease_detected}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'image_filename': self.image_filename,
            'plant_type': self.plant_type,
            'disease_detected': self.disease_detected,
            'confidence_score': self.confidence_score,
            'severity_level': self.severity_level,
            'analysis_details': self.analysis_details,
            'recommended_actions': self.recommended_actions,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class AnalysisHistory(db.Model):
    """Model to store history of all analyses for a user/session."""
    
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('plant_analysis.id'), nullable=False)
    plant_location = db.Column(db.String(255))  # e.g., 'garden', 'indoor'
    plant_age_days = db.Column(db.Integer)
    weather_conditions = db.Column(db.String(100))  # e.g., 'sunny', 'rainy'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalysisHistory {self.id}: session {self.session_id}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'analysis_id': self.analysis_id,
            'plant_location': self.plant_location,
            'plant_age_days': self.plant_age_days,
            'weather_conditions': self.weather_conditions,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
