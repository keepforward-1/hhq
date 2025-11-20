"""
首页内容路由
"""
from flask import Blueprint, request, jsonify
from models import db
from models.homepage_content import HomepageContent

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/content', methods=['GET'])
def get_content():
    """获取首页内容"""
    try:
        content_type = request.args.get('type')
        
        query = HomepageContent.query.filter_by(is_active=True)
        if content_type:
            query = query.filter_by(content_type=content_type)
        
        contents = query.order_by(
            HomepageContent.sort_order.asc(),
            HomepageContent.created_at.desc()
        ).all()
        
        return jsonify({
            'contents': [c.to_dict() for c in contents]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

