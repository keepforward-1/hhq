"""
星座识别路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.constellation_recognition_service import ConstellationRecognitionService
from utils.file_upload import save_uploaded_file

constellation_bp = Blueprint('constellation', __name__)
constellation_service = ConstellationRecognitionService()

@constellation_bp.route('/recognize', methods=['POST'])
@jwt_required()
def recognize():
    """识别星座"""
    try:
        user_id = get_jwt_identity()
        
        if 'image' not in request.files:
            return jsonify({'error': '请上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        # 保存文件
        image_path = save_uploaded_file(file, 'constellation')
        
        # 识别
        result = constellation_service.recognize(image_path, user_id)
        
        return jsonify({
            'message': '识别成功',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@constellation_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """获取识别历史"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 20, type=int)
        
        history = constellation_service.get_history(user_id, limit)
        
        return jsonify({
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

