"""
太空引擎数据模型
"""
from models import db
from datetime import datetime

class SpaceEngineData(db.Model):
    """太空引擎数据表"""
    __tablename__ = 'space_engine_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    data_type = db.Column(db.String(50), nullable=False, comment='数据类型：galaxy/constellation/positioning')
    source_id = db.Column(db.Integer, nullable=True, comment='来源数据ID')
    celestial_object = db.Column(db.String(100), nullable=True, comment='天体对象名称')
    ra = db.Column(db.Float, nullable=True, comment='赤经（度）')
    dec = db.Column(db.Float, nullable=True, comment='赤纬（度）')
    distance = db.Column(db.Float, nullable=True, comment='距离（光年）')
    view_data = db.Column(db.Text, nullable=True, comment='视图数据（JSON格式）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    user = db.relationship('User', backref='space_engine_data')
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'data_type': self.data_type,
            'source_id': self.source_id,
            'celestial_object': self.celestial_object,
            'ra': self.ra,
            'dec': self.dec,
            'distance': self.distance,
            'view_data': json.loads(self.view_data) if self.view_data else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

