"""
天体定位服务（Astrometry.net）
"""
import os
import requests
import time
from models import db
from models.celestial_positioning import CelestialPositioning

class CelestialPositioningService:
    """天体定位服务类（使用Astrometry.net API）"""
    
    def __init__(self, api_url=None, api_key=None):
        """初始化服务"""
        self.api_url = api_url or os.getenv('ASTROMETRY_API_URL', 'http://localhost:5000')
        self.api_key = api_key or os.getenv('ASTROMETRY_API_KEY')
    
    def solve_field(self, image_path, user_id):
        """解析天体定位"""
        try:
            # 上传图片到Astrometry.net
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {}
                if self.api_key:
                    data['apikey'] = self.api_key
                
                # 提交任务
                upload_url = f"{self.api_url}/upload"
                response = requests.post(upload_url, files=files, data=data)
                
                if response.status_code != 200:
                    raise Exception(f"上传失败: {response.status_code} - {response.text}")
                
                result = response.json()
                job_id = result.get('job_id')
                
                if not job_id:
                    raise Exception("未获取到任务ID")
                
                # 等待任务完成
                max_wait_time = 300  # 最多等待5分钟
                start_time = time.time()
                
                while time.time() - start_time < max_wait_time:
                    status_url = f"{self.api_url}/jobs/{job_id}"
                    status_response = requests.get(status_url)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'success':
                            # 获取结果
                            result_url = f"{self.api_url}/jobs/{job_id}/info"
                            result_response = requests.get(result_url)
                            
                            if result_response.status_code == 200:
                                solve_result = result_response.json()
                                
                                # 解析结果
                                calibration = solve_result.get('calibration', {})
                                ra = calibration.get('ra')
                                dec = calibration.get('dec')
                                field_width = calibration.get('field_width')
                                field_height = calibration.get('field_height')
                                orientation = calibration.get('orientation')
                                
                                # 保存记录
                                record = CelestialPositioning(
                                    user_id=user_id,
                                    image_path=image_path,
                                    ra=ra,
                                    dec=dec,
                                    field_width=field_width,
                                    field_height=field_height,
                                    orientation=orientation,
                                    solved=True,
                                    solve_time=time.time() - start_time
                                )
                                db.session.add(record)
                                db.session.commit()
                                
                                return {
                                    'solved': True,
                                    'ra': ra,
                                    'dec': dec,
                                    'field_width': field_width,
                                    'field_height': field_height,
                                    'orientation': orientation,
                                    'solve_time': time.time() - start_time
                                }
                        
                        elif status == 'failure':
                            raise Exception("解析失败")
                    
                    time.sleep(2)  # 等待2秒后重试
                
                raise Exception("解析超时")
                
        except Exception as e:
            # 保存失败记录
            record = CelestialPositioning(
                user_id=user_id,
                image_path=image_path,
                solved=False
            )
            db.session.add(record)
            db.session.commit()
            
            raise Exception(f"天体定位失败: {e}")
    
    def get_history(self, user_id, limit=20):
        """获取用户历史记录"""
        records = CelestialPositioning.query.filter_by(
            user_id=user_id
        ).order_by(
            CelestialPositioning.created_at.desc()
        ).limit(limit).all()
        
        return [record.to_dict() for record in records]

