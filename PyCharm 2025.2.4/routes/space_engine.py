"""
太空引擎路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.space_engine_data import SpaceEngineData

space_engine_bp = Blueprint('space_engine', __name__)

@space_engine_bp.route('/save-view', methods=['POST'])
@jwt_required()
def save_view():
    """保存视图数据"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        view_data = SpaceEngineData(
            user_id=user_id,
            data_type=data.get('data_type'),
            source_id=data.get('source_id'),
            celestial_object=data.get('celestial_object'),
            ra=data.get('ra'),
            dec=data.get('dec'),
            distance=data.get('distance'),
            view_data=str(data.get('view_data', {}))
        )
        
        db.session.add(view_data)
        db.session.commit()
        
        return jsonify({
            'message': '保存成功',
            'data': view_data.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@space_engine_bp.route('/get-data', methods=['GET'])
@jwt_required()
def get_data():
    """获取数据用于太空引擎"""
    try:
        user_id = get_jwt_identity()
        data_type = request.args.get('data_type')
        
        query = SpaceEngineData.query.filter_by(user_id=user_id)
        if data_type:
            query = query.filter_by(data_type=data_type)
        
        data_list = query.order_by(
            SpaceEngineData.created_at.desc()
        ).limit(50).all()
        
        return jsonify({
            'data': [d.to_dict() for d in data_list]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

