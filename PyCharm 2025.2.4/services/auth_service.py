"""
用户认证服务
"""
from models import db
from models.user import User
import bcrypt

class AuthService:
    """认证服务类"""
    
    @staticmethod
    def create_user(username, email, password, nickname=None):
        """创建用户"""
        # 加密密码
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            nickname=nickname or username
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(username, password):
        """验证用户"""
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return None
        
        if not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        ):
            return None
        
        return user

