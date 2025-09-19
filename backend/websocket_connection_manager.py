# backend/websocket_connection_manager.py
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserSession:
    session_id: str
    socket_id: str
    user_id: Optional[str]
    connected_at: datetime
    last_activity: datetime
    is_active: bool = True
    metadata: Dict = None

class WebSocketConnectionManager:
    def __init__(self):
        self.active_sessions: Dict[str, UserSession] = {}
        self.socket_to_session: Dict[str, str] = {}
        self.user_to_sessions: Dict[str, List[str]] = {}
        self.max_connections_per_user = 5
        self.session_timeout = 3600  # 1小时
        
    async def create_session(self, socket_id: str, user_id: Optional[str] = None) -> UserSession:
        """创建新的用户会话"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = UserSession(
            session_id=session_id,
            socket_id=socket_id,
            user_id=user_id,
            connected_at=now,
            last_activity=now,
            metadata={}
        )
        
        self.active_sessions[session_id] = session
        self.socket_to_session[socket_id] = session_id
        
        if user_id:
            if user_id not in self.user_to_sessions:
                self.user_to_sessions[user_id] = []
            self.user_to_sessions[user_id].append(session_id)
            
            # 检查用户连接数限制
            await self._enforce_user_connection_limit(user_id)
        
        logger.info(f"创建新会话: {session_id} for socket: {socket_id}")
        return session
    
    async def get_session(self, socket_id: str) -> Optional[UserSession]:
        """获取会话信息"""
        session_id = self.socket_to_session.get(socket_id)
        if session_id:
            return self.active_sessions.get(session_id)
        return None
    
    async def update_activity(self, socket_id: str):
        """更新会话活动时间"""
        session = await self.get_session(socket_id)
        if session:
            session.last_activity = datetime.now()
    
    async def remove_session(self, socket_id: str):
        """移除会话"""
        session_id = self.socket_to_session.get(socket_id)
        if session_id:
            session = self.active_sessions.get(session_id)
            if session:
                # 从用户会话列表中移除
                if session.user_id and session.user_id in self.user_to_sessions:
                    self.user_to_sessions[session.user_id].remove(session_id)
                    if not self.user_to_sessions[session.user_id]:
                        del self.user_to_sessions[session.user_id]
                
                # 清理会话
                del self.active_sessions[session_id]
                del self.socket_to_session[socket_id]
                
                logger.info(f"移除会话: {session_id}")
    
    async def _enforce_user_connection_limit(self, user_id: str):
        """强制用户连接数限制"""
        if user_id in self.user_to_sessions:
            sessions = self.user_to_sessions[user_id]
            if len(sessions) > self.max_connections_per_user:
                # 移除最旧的连接
                oldest_session_id = min(sessions, 
                    key=lambda sid: self.active_sessions[sid].connected_at)
                oldest_session = self.active_sessions[oldest_session_id]
                
                logger.warning(f"用户 {user_id} 超过连接限制，断开最旧连接: {oldest_session_id}")
                await self.remove_session(oldest_session.socket_id)
    
    async def get_user_sessions(self, user_id: str) -> List[UserSession]:
        """获取用户的所有会话"""
        if user_id in self.user_to_sessions:
            session_ids = self.user_to_sessions[user_id]
            return [self.active_sessions[sid] for sid in session_ids if sid in self.active_sessions]
        return []
    
    async def cleanup_inactive_sessions(self):
        """清理非活跃会话"""
        now = datetime.now()
        inactive_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if (now - session.last_activity).seconds > self.session_timeout:
                inactive_sessions.append(session.socket_id)
        
        for socket_id in inactive_sessions:
            await self.remove_session(socket_id)
            logger.info(f"清理非活跃会话: {socket_id}")
    
    def get_stats(self) -> Dict:
        """获取连接统计信息"""
        return {
            "total_sessions": len(self.active_sessions),
            "total_users": len(self.user_to_sessions),
            "sessions_per_user": {
                user_id: len(sessions) 
                for user_id, sessions in self.user_to_sessions.items()
            }
        }

# 全局连接管理器实例
connection_manager = WebSocketConnectionManager()
