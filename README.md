# 基于多源星图识别的天文观测辅助系统

## 项目简介

这是一个综合性的天文观测辅助系统，集成了星系分类、星座识别、天体定位、太空引擎和天巡AI等多个功能模块。

## 技术栈

### 后端
- **框架**: Flask (Python)
- **数据库**: MySQL
- **缓存**: Redis
- **AI模型**: TensorFlow/Keras (星系分类)
- **API集成**: 
  - DeepSeek API (天巡AI)
  - Roboflow API (星座识别)
  - Astrometry.net (天体定位)

### 前端
- **框架**: React + Vite
- **UI库**: Ant Design
- **3D引擎**: Three.js + SpaceKit (太空引擎)

### 部署
- **后端服务器**: Python Flask
- **Astrometry.net**: CentOS 7.8 (VMware Workstation Pro 16)

## 项目结构

```
基于多源星图识别的天文观测辅助系统的设计与实现/
├── PyCharm 2025.2.4/          # 后端代码
│   ├── app.py                 # Flask主应用
│   ├── models/                # 数据库模型
│   ├── routes/                # API路由
│   ├── services/              # 业务逻辑服务
│   ├── utils/                 # 工具函数
│   ├── train_galaxy_model.py  # 星系分类模型训练脚本
│   └── requirements.txt       # Python依赖
├── Visual Studio Code/         # 前端代码
│   ├── src/
│   │   ├── pages/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   ├── contexts/          # React Context
│   │   └── App.jsx            # 主应用组件
│   └── package.json           # 前端依赖
├── CentOS 7.8/                # Astrometry.net部署
│   ├── deploy_astrometry.sh   # 部署脚本
│   └── astrometry_api_server.py # API服务器
└── Navicat Premium 16（MySQL）/ # 数据库脚本
    └── create_database.sql    # 数据库创建脚本
```

## 核心功能模块

### 1. 星系分类
- 使用Galaxy10 DECaLS数据集训练CNN模型
- 目标精度：89%
- 支持10种星系类型分类
- 训练脚本：`PyCharm 2025.2.4/train_galaxy_model.py`

### 2. 星座识别
- 集成Roboflow API
- 实时识别图片中的星座
- 支持多星座检测

### 3. 天体定位
- 基于Astrometry.net 0.80
- 自动解析天体坐标（RA/Dec）
- 支持FITS和常见图片格式

### 4. 太空引擎
- 基于SpaceKit的高仿真3D宇宙模拟
- 支持从其他模块导入数据
- 实时渲染和交互

### 5. 天巡AI
- 集成DeepSeek API
- 支持多轮对话
- 可联动其他模块
- 提供天文知识问答

## 安装和部署

### 1. 数据库设置

在Navicat Premium 16中执行：
```sql
-- 运行 create_database.sql
```

### 2. 后端部署

```bash
cd "PyCharm 2025.2.4"
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入配置信息

# 训练星系分类模型（需要先下载Galaxy10数据集）
python train_galaxy_model.py

# 启动后端服务
python app.py
```

### 3. Astrometry.net部署（CentOS 7.8）

在VMware Workstation Pro 16的CentOS 7.8虚拟机中：

```bash
cd "CentOS 7.8"
chmod +x deploy_astrometry.sh
sudo ./deploy_astrometry.sh

# 启动API服务器
python3 astrometry_api_server.py
```

### 4. 前端部署

```bash
cd "Visual Studio Code"
npm install
npm run dev
```

## 环境变量配置

### 后端 (.env)
```
DATABASE_URI=mysql+pymysql://root:password@localhost:3306/astronomy_system
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
REDIS_HOST=localhost
REDIS_PORT=6379
DEEPSEEK_API_KEY=your-deepseek-api-key
ROBOFLOW_API_KEY=your-roboflow-api-key
ASTROMETRY_API_URL=http://your-centos-server:5000
```

## API文档

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 星系分类
- `POST /api/galaxy/classify` - 分类星系图片
- `GET /api/galaxy/history` - 获取分类历史

### 星座识别
- `POST /api/constellation/recognize` - 识别星座
- `GET /api/constellation/history` - 获取识别历史

### 天体定位
- `POST /api/positioning/solve` - 解析天体定位
- `GET /api/positioning/history` - 获取解析历史

### 太空引擎
- `POST /api/space-engine/save-view` - 保存视图数据
- `GET /api/space-engine/get-data` - 获取数据

### 天巡AI
- `POST /api/tianxun-ai/chat` - 与AI对话
- `GET /api/tianxun-ai/history` - 获取聊天历史
- `GET /api/tianxun-ai/sessions` - 获取所有会话

## 数据集下载

### Galaxy10 DECaLS数据集
从以下链接下载：
https://astronn.readthedocs.io/en/latest/galaxy10.html

下载后放在项目根目录，命名为 `Galaxy10_DECals.h5`

## 注意事项

1. **星系分类模型训练**：需要先下载Galaxy10数据集，训练时间可能较长（取决于硬件）
2. **Astrometry.net部署**：需要在CentOS 7.8虚拟机上部署，确保网络连接正常以下载索引文件
3. **API密钥**：需要申请DeepSeek和Roboflow的API密钥
4. **数据库**：确保MySQL服务运行正常
5. **Redis**：可选，用于缓存（如果未配置Redis，部分功能可能受影响）

## 开发工具

- **后端**: PyCharm 2025.2.4
- **前端**: Visual Studio Code
- **数据库**: Navicat Premium 16
- **虚拟机**: VMware Workstation Pro 16 (CentOS 7.8)

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题，请查看项目文档或提交Issue。

