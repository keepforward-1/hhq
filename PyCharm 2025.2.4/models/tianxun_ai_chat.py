"""
天巡AI聊天模型
"""
from models import db
from datetime import datetime

class TianxunAIChat(db.Model):
    """天巡AI聊天记录表"""
    __tablename__ = 'tianxun_ai_chats'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    session_id = db.Column(db.String(100), nullable=False, comment='会话ID')
    role = db.Column(db.String(20), nullable=False, comment='角色：user/assistant')
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    module_context = db.Column(db.String(50), nullable=True, comment='关联模块：galaxy/constellation/positioning/space_engine')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    user = db.relationship('User', backref='tianxun_ai_chats')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'role': self.role,
            'content': self.content,
            'module_context': self.module_context,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

