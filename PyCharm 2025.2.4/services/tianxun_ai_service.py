"""
天巡AI服务（DeepSeek API）
"""
import os
from openai import OpenAI
from models import db
from models.tianxun_ai_chat import TianxunAIChat
import uuid

class TianxunAIService:
    """天巡AI服务类（使用DeepSeek API）"""
    
    def __init__(self, api_key=None, base_url=None):
        """初始化服务"""
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = base_url or os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
    
    def chat(self, user_id, message, session_id=None, module_context=None):
        """与AI对话"""
        if not self.client:
            raise Exception("DeepSeek API密钥未配置")
        
        try:
            # 如果没有session_id，创建新的会话
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # 获取历史对话
            history = self.get_chat_history(user_id, session_id, limit=10)
            
            # 构建消息列表
            messages = []
            
            # 添加系统提示
            system_prompt = self._build_system_prompt(module_context)
            if system_prompt:
                messages.append({
                    'role': 'system',
                    'content': system_prompt
                })
            
            # 添加历史对话
            for chat in history:
                messages.append({
                    'role': chat['role'],
                    'content': chat['content']
                })
            
            # 添加当前用户消息
            messages.append({
                'role': 'user',
                'content': message
            })
            
            # 保存用户消息
            user_chat = TianxunAIChat(
                user_id=user_id,
                session_id=session_id,
                role='user',
                content=message,
                module_context=module_context
            )
            db.session.add(user_chat)
            db.session.commit()
            
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model='deepseek-chat',
                messages=messages,
                temperature=1.0,
                stream=False
            )
            
            assistant_message = response.choices[0].message.content
            
            # 保存AI回复
            assistant_chat = TianxunAIChat(
                user_id=user_id,
                session_id=session_id,
                role='assistant',
                content=assistant_message,
                module_context=module_context
            )
            db.session.add(assistant_chat)
            db.session.commit()
            
            return {
                'session_id': session_id,
                'message': assistant_message,
                'role': 'assistant'
            }
            
        except Exception as e:
            raise Exception(f"AI对话失败: {e}")
    
    def _build_system_prompt(self, module_context):
        """构建系统提示"""
        base_prompt = """你是一个专业的天文观测助手，名为"天巡AI"。你的任务是帮助用户进行天文观测和探索。

你可以：
1. 回答天文相关的问题
2. 解释星系分类、星座识别、天体定位等模块的结果
3. 提供天文观测建议
4. 协助用户操作各个功能模块

请用中文回答，语言要专业但易懂。"""
        
        if module_context == 'galaxy':
            return base_prompt + "\n\n当前用户正在使用星系分类模块，你可以帮助解释分类结果。"
        elif module_context == 'constellation':
            return base_prompt + "\n\n当前用户正在使用星座识别模块，你可以帮助识别和解释星座。"
        elif module_context == 'positioning':
            return base_prompt + "\n\n当前用户正在使用天体定位模块，你可以帮助解释定位结果。"
        elif module_context == 'space_engine':
            return base_prompt + "\n\n当前用户正在使用太空引擎模块，你可以帮助导航和探索宇宙。"
        
        return base_prompt
    
    def get_chat_history(self, user_id, session_id, limit=50):
        """获取聊天历史"""
        chats = TianxunAIChat.query.filter_by(
            user_id=user_id,
            session_id=session_id
        ).order_by(
            TianxunAIChat.created_at.asc()
        ).limit(limit).all()
        
        return [chat.to_dict() for chat in chats]
    
    def get_sessions(self, user_id):
        """获取用户的所有会话"""
        sessions = db.session.query(
            TianxunAIChat.session_id
        ).filter_by(
            user_id=user_id
        ).distinct().all()
        
        return [s[0] for s in sessions]

