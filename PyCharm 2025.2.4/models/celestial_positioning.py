"""
天体定位模型
"""
from models import db
from datetime import datetime

class CelestialPositioning(db.Model):
    """天体定位记录表"""
    __tablename__ = 'celestial_positionings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    image_path = db.Column(db.String(255), nullable=False, comment='图片路径')
    ra = db.Column(db.Float, nullable=True, comment='赤经（度）')
    dec = db.Column(db.Float, nullable=True, comment='赤纬（度）')
    field_width = db.Column(db.Float, nullable=True, comment='视场宽度（度）')
    field_height = db.Column(db.Float, nullable=True, comment='视场高度（度）')
    orientation = db.Column(db.Float, nullable=True, comment='方向角（度）')
    solved = db.Column(db.Boolean, default=False, comment='是否成功解析')
    solve_time = db.Column(db.Float, nullable=True, comment='解析耗时（秒）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    user = db.relationship('User', backref='celestial_positionings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'ra': self.ra,
            'dec': self.dec,
            'field_width': self.field_width,
            'field_height': self.field_height,
            'orientation': self.orientation,
            'solved': self.solved,
            'solve_time': self.solve_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

