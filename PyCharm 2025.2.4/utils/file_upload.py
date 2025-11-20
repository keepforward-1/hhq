"""
文件上传工具
"""
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'fits', 'fit'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder='uploads'):
    """保存上传的文件"""
    if not allowed_file(file.filename):
        raise Exception('不支持的文件类型')
    
    # 创建上传目录
    upload_dir = os.path.join('uploads', subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一文件名
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    return file_path

