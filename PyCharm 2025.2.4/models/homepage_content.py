"""
首页内容模型
"""
from models import db
from datetime import datetime

class HomepageContent(db.Model):
    """首页内容表"""
    __tablename__ = 'homepage_contents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content_type = db.Column(db.String(50), nullable=False, comment='内容类型：background/carousel/update/knowledge')
    title = db.Column(db.String(200), nullable=True, comment='标题')
    content = db.Column(db.Text, nullable=True, comment='内容')
    image_url = db.Column(db.String(255), nullable=True, comment='图片URL')
    link_url = db.Column(db.String(255), nullable=True, comment='链接URL')
    sort_order = db.Column(db.Integer, default=0, comment='排序顺序')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content_type': self.content_type,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

