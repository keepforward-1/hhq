"""
基于多源星图识别的天文观测辅助系统 - 后端主程序
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 可以根据需要设置过期时间

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'mysql+pymysql://root:password@localhost:3306/astronomy_system?charset=utf8mb4'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis配置
app.config['REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
app.config['REDIS_PORT'] = int(os.getenv('REDIS_PORT', 6379))
app.config['REDIS_DB'] = int(os.getenv('REDIS_DB', 0))

# 初始化扩展
CORS(app)
jwt = JWTManager(app)

# 注册蓝图
from routes.auth import auth_bp
from routes.galaxy_classification import galaxy_bp
from routes.constellation_recognition import constellation_bp
from routes.celestial_positioning import positioning_bp
from routes.space_engine import space_engine_bp
from routes.tianxun_ai import tianxun_ai_bp
from routes.user import user_bp
from routes.homepage import homepage_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(galaxy_bp, url_prefix='/api/galaxy')
app.register_blueprint(constellation_bp, url_prefix='/api/constellation')
app.register_blueprint(positioning_bp, url_prefix='/api/positioning')
app.register_blueprint(space_engine_bp, url_prefix='/api/space-engine')
app.register_blueprint(tianxun_ai_bp, url_prefix='/api/tianxun-ai')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(homepage_bp, url_prefix='/api/homepage')

@app.route('/')
def index():
    return {'message': '天文观测辅助系统API服务运行中', 'version': '1.0.0'}

if __name__ == '__main__':
    from models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)

