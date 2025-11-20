# 后端服务说明

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

3. 训练星系分类模型
```bash
# 需要先下载Galaxy10数据集
python train_galaxy_model.py
```

4. 启动服务
```bash
python app.py
```

## 模型训练

星系分类模型训练脚本会：
1. 加载Galaxy10 DECaLS数据集
2. 数据预处理和增强
3. 构建深度CNN模型
4. 训练模型（目标精度89%）
5. 保存最佳模型

训练完成后，模型会保存在 `models/galaxy_classification_model.h5`

## API端点

所有API端点都需要JWT认证（除了注册和登录）

在请求头中添加：
```
Authorization: Bearer <token>
```

