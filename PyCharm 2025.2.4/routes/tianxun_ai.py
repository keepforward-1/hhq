"""
天巡AI路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.tianxun_ai_service import TianxunAIService

tianxun_ai_bp = Blueprint('tianxun_ai', __name__)
tianxun_ai_service = TianxunAIService()

@tianxun_ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """与AI对话"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = data.get('message')
        session_id = data.get('session_id')
        module_context = data.get('module_context')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        result = tianxun_ai_service.chat(user_id, message, session_id, module_context)
        
        return jsonify({
            'message': '对话成功',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tianxun_ai_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """获取聊天历史"""
    try:
        user_id = get_jwt_identity()
        session_id = request.args.get('session_id')
        limit = request.args.get('limit', 50, type=int)
        
        if not session_id:
            return jsonify({'error': '会话ID不能为空'}), 400
        
        history = tianxun_ai_service.get_chat_history(user_id, session_id, limit)
        
        return jsonify({
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tianxun_ai_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """获取所有会话"""
    try:
        user_id = get_jwt_identity()
        
        sessions = tianxun_ai_service.get_sessions(user_id)
        
        return jsonify({
            'sessions': sessions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

