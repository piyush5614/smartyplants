"""Database manager for data operations."""

from typing import List, Dict, Optional
from datetime import datetime
import json
from models.database_models import db, PlantAnalysis, AnalysisHistory


class DatabaseManager:
    """Manager for database operations."""
    
    @staticmethod
    def save_analysis(analysis_result: Dict, care_plan: Dict = None) -> PlantAnalysis:
        """
        Save analysis result to database.
        
        Args:
            analysis_result: Analysis result dictionary
            care_plan: Optional care plan dictionary
            
        Returns:
            PlantAnalysis database record
        """
        try:
            analysis = PlantAnalysis(
                plant_type=analysis_result.get('plant_type', 'unknown'),
                disease_detected=analysis_result['disease_detection']['primary_disease'],
                confidence_score=analysis_result['disease_detection']['confidence'],
                severity_level=analysis_result['disease_detection']['severity'],
                analysis_details=json.dumps(analysis_result),
                recommended_actions=json.dumps(care_plan) if care_plan else None
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            return analysis
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to save analysis: {str(e)}")
    
    @staticmethod
    def save_analysis_history(session_id: str, analysis_id: int, 
                             plant_location: str = None, 
                             plant_age_days: int = None,
                             weather_conditions: str = None,
                             notes: str = None) -> AnalysisHistory:
        """
        Save analysis to history.
        
        Args:
            session_id: Session identifier
            analysis_id: PlantAnalysis ID
            plant_location: Plant location info
            plant_age_days: Plant age in days
            weather_conditions: Weather conditions
            notes: Additional notes
            
        Returns:
            AnalysisHistory database record
        """
        try:
            history = AnalysisHistory(
                session_id=session_id,
                analysis_id=analysis_id,
                plant_location=plant_location,
                plant_age_days=plant_age_days,
                weather_conditions=weather_conditions,
                notes=notes
            )
            
            db.session.add(history)
            db.session.commit()
            
            return history
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to save history: {str(e)}")
    
    @staticmethod
    def get_analysis(analysis_id: int) -> Optional[PlantAnalysis]:
        """Get analysis by ID."""
        return PlantAnalysis.query.get(analysis_id)
    
    @staticmethod
    def get_session_history(session_id: str, limit: int = 50) -> List[AnalysisHistory]:
        """
        Get analysis history for session.
        
        Args:
            session_id: Session identifier
            limit: Maximum results
            
        Returns:
            List of AnalysisHistory records
        """
        return AnalysisHistory.query.filter_by(
            session_id=session_id
        ).order_by(AnalysisHistory.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_recent_analyses(limit: int = 10) -> List[PlantAnalysis]:
        """Get recently saved analyses."""
        return PlantAnalysis.query.order_by(
            PlantAnalysis.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_analyses_by_disease(disease_name: str, limit: int = 50) -> List[PlantAnalysis]:
        """Get analyses by disease type."""
        return PlantAnalysis.query.filter_by(
            disease_detected=disease_name
        ).order_by(PlantAnalysis.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_disease_statistics() -> Dict:
        """Get statistics about detected diseases."""
        try:
            analyses = PlantAnalysis.query.all()
            
            disease_counts = {}
            severity_counts = {}
            avg_confidence = 0
            
            total = len(analyses)
            
            for analysis in analyses:
                # Count diseases
                disease = analysis.disease_detected
                disease_counts[disease] = disease_counts.get(disease, 0) + 1
                
                # Count severity levels
                severity = analysis.severity_level
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
                # Accumulate confidence
                avg_confidence += analysis.confidence_score or 0
            
            if total > 0:
                avg_confidence = avg_confidence / total
            
            return {
                'total_analyses': total,
                'disease_distribution': disease_counts,
                'severity_distribution': severity_counts,
                'average_confidence': round(avg_confidence, 3),
                'most_common_disease': max(disease_counts, key=disease_counts.get) if disease_counts else 'unknown'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def delete_analysis(analysis_id: int) -> bool:
        """Delete analysis record."""
        try:
            analysis = PlantAnalysis.query.get(analysis_id)
            if analysis:
                db.session.delete(analysis)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete analysis: {str(e)}")
    
    @staticmethod
    def clear_old_analyses(days: int = 30) -> int:
        """
        Delete analyses older than specified days.
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of deleted records
        """
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            count = PlantAnalysis.query.filter(
                PlantAnalysis.created_at < cutoff_date
            ).delete()
            
            db.session.commit()
            return count
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to clear old analyses: {str(e)}")
