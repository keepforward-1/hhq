"""
星系分类服务
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from models import db
from models.galaxy_classification import GalaxyClassification

class GalaxyClassificationService:
    """星系分类服务类"""
    
    # Galaxy10类别映射（根据astroNN文档）
    GALAXY10_CLASSES = {
        0: '圆盘星系（Disk, Face-on, No Spiral）',
        1: '圆盘星系（Disk, Face-on, Tight Spiral）',
        2: '圆盘星系（Disk, Face-on, Medium Spiral）',
        3: '圆盘星系（Disk, Face-on, Loose Spiral）',
        4: '圆盘星系（Disk, Edge-on, No Bulge）',
        5: '圆盘星系（Disk, Edge-on, Red Bulge）',
        6: '椭圆星系（Smooth, Completely round）',
        7: '椭圆星系（Smooth, In-between）',
        8: '椭圆星系（Smooth, Cigar shaped）',
        9: '恒星（Star）'
    }
    
    def __init__(self, model_path='models/galaxy_classification_model.h5'):
        """初始化服务"""
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """加载模型"""
        if os.path.exists(self.model_path):
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"模型加载成功: {self.model_path}")
            except Exception as e:
                print(f"模型加载失败: {e}")
                self.model = None
        else:
            print(f"模型文件不存在: {self.model_path}")
            self.model = None
    
    def preprocess_image(self, image_path):
        """预处理图片"""
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((69, 69))  # Galaxy10数据集图片尺寸
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            return img_array
        except Exception as e:
            raise Exception(f"图片预处理失败: {e}")
    
    def classify(self, image_path, user_id):
        """分类星系图片"""
        if not self.model:
            raise Exception("模型未加载，请先训练模型")
        
        try:
            # 预处理图片
            img_array = self.preprocess_image(image_path)
            
            # 预测
            predictions = self.model.predict(img_array, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            # 获取类别名称
            class_name = self.GALAXY10_CLASSES.get(predicted_class, '未知类别')
            
            # 保存记录
            record = GalaxyClassification(
                user_id=user_id,
                image_path=image_path,
                predicted_class=int(predicted_class),
                confidence=confidence,
                class_name=class_name
            )
            db.session.add(record)
            db.session.commit()
            
            return {
                'predicted_class': int(predicted_class),
                'class_name': class_name,
                'confidence': confidence,
                'all_predictions': {
                    self.GALAXY10_CLASSES[i]: float(predictions[0][i])
                    for i in range(len(self.GALAXY10_CLASSES))
                }
            }
            
        except Exception as e:
            raise Exception(f"分类失败: {e}")
    
    def get_history(self, user_id, limit=20):
        """获取用户历史记录"""
        records = GalaxyClassification.query.filter_by(
            user_id=user_id
        ).order_by(
            GalaxyClassification.created_at.desc()
        ).limit(limit).all()
        
        return [record.to_dict() for record in records]

