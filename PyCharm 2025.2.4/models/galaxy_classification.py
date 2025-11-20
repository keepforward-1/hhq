"""
星系分类模型
"""
from models import db
from datetime import datetime

class GalaxyClassification(db.Model):
    """星系分类记录表"""
    __tablename__ = 'galaxy_classifications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    image_path = db.Column(db.String(255), nullable=False, comment='图片路径')
    predicted_class = db.Column(db.Integer, nullable=False, comment='预测类别')
    confidence = db.Column(db.Float, nullable=False, comment='置信度')
    class_name = db.Column(db.String(50), nullable=True, comment='类别名称')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    user = db.relationship('User', backref='galaxy_classifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'predicted_class': self.predicted_class,
            'confidence': self.confidence,
            'class_name': self.class_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

