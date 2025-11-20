"""
星座识别模型
"""
from models import db
from datetime import datetime

class ConstellationRecognition(db.Model):
    """星座识别记录表"""
    __tablename__ = 'constellation_recognitions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    image_path = db.Column(db.String(255), nullable=False, comment='图片路径')
    detected_constellations = db.Column(db.Text, nullable=True, comment='检测到的星座（JSON格式）')
    confidence = db.Column(db.Float, nullable=True, comment='置信度')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    user = db.relationship('User', backref='constellation_recognitions')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'detected_constellations': json.loads(self.detected_constellations) if self.detected_constellations else None,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

