"""
星座识别服务
"""
import os
import requests
import json
from models import db
from models.constellation_recognition import ConstellationRecognition

class ConstellationRecognitionService:
    """星座识别服务类（使用Roboflow API）"""
    
    def __init__(self, api_key=None, model_id=None):
        """初始化服务"""
        self.api_key = api_key or os.getenv('ROBOFLOW_API_KEY')
        self.model_id = model_id or os.getenv('ROBOFLOW_MODEL_ID', 'ws-qwbuh/constellation-dsphi/1')
        self.base_url = f"https://detect.roboflow.com/{self.model_id}"
    
    def recognize(self, image_path, user_id):
        """识别星座"""
        if not self.api_key:
            raise Exception("Roboflow API密钥未配置")
        
        try:
            # 读取图片
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 调用Roboflow API
            response = requests.post(
                self.base_url,
                params={'api_key': self.api_key},
                files={'file': image_data},
                data={'overlap': 30, 'confidence': 40}
            )
            
            if response.status_code != 200:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # 解析结果
            detections = result.get('predictions', [])
            detected_constellations = []
            
            for detection in detections:
                detected_constellations.append({
                    'class': detection.get('class', ''),
                    'confidence': detection.get('confidence', 0),
                    'x': detection.get('x', 0),
                    'y': detection.get('y', 0),
                    'width': detection.get('width', 0),
                    'height': detection.get('height', 0)
                })
            
            # 计算平均置信度
            avg_confidence = sum(d['confidence'] for d in detected_constellations) / len(detected_constellations) if detected_constellations else 0
            
            # 保存记录
            record = ConstellationRecognition(
                user_id=user_id,
                image_path=image_path,
                detected_constellations=json.dumps(detected_constellations, ensure_ascii=False),
                confidence=avg_confidence
            )
            db.session.add(record)
            db.session.commit()
            
            return {
                'detected_constellations': detected_constellations,
                'count': len(detected_constellations),
                'confidence': avg_confidence
            }
            
        except Exception as e:
            raise Exception(f"星座识别失败: {e}")
    
    def get_history(self, user_id, limit=20):
        """获取用户历史记录"""
        records = ConstellationRecognition.query.filter_by(
            user_id=user_id
        ).order_by(
            ConstellationRecognition.created_at.desc()
        ).limit(limit).all()
        
        return [record.to_dict() for record in records]

