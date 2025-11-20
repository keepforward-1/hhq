"""
星系分类路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.galaxy_classification_service import GalaxyClassificationService
from utils.file_upload import save_uploaded_file
import os

galaxy_bp = Blueprint('galaxy', __name__)
galaxy_service = GalaxyClassificationService()

@galaxy_bp.route('/classify', methods=['POST'])
@jwt_required()
def classify():
    """分类星系图片"""
    try:
        user_id = get_jwt_identity()
        
        if 'image' not in request.files:
            return jsonify({'error': '请上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        # 保存文件
        image_path = save_uploaded_file(file, 'galaxy')
        
        # 分类
        result = galaxy_service.classify(image_path, user_id)
        
        return jsonify({
            'message': '分类成功',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@galaxy_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """获取分类历史"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 20, type=int)
        
        history = galaxy_service.get_history(user_id, limit)
        
        return jsonify({
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

