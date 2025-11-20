"""
天体定位路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.celestial_positioning_service import CelestialPositioningService
from utils.file_upload import save_uploaded_file

positioning_bp = Blueprint('positioning', __name__)
positioning_service = CelestialPositioningService()

@positioning_bp.route('/solve', methods=['POST'])
@jwt_required()
def solve():
    """解析天体定位"""
    try:
        user_id = get_jwt_identity()
        
        if 'image' not in request.files:
            return jsonify({'error': '请上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        # 保存文件
        image_path = save_uploaded_file(file, 'positioning')
        
        # 解析
        result = positioning_service.solve_field(image_path, user_id)
        
        return jsonify({
            'message': '解析成功',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@positioning_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """获取解析历史"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 20, type=int)
        
        history = positioning_service.get_history(user_id, limit)
        
        return jsonify({
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

