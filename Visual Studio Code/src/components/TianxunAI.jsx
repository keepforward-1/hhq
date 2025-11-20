import React, { useState, useEffect, useRef } from 'react'
import { Card, Input, Button, List, Avatar, Space } from 'antd'
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons'
import axios from 'axios'
import { useAuth } from '../contexts/AuthContext'
import './TianxunAI.css'

const { TextArea } = Input

const TianxunAI = ({ moduleContext }) => {
  const { user } = useAuth()
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // 创建新会话
    const newSessionId = `session_${Date.now()}`
    setSessionId(newSessionId)
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const sendMessage = async () => {
    if (!message.trim() || loading) return

    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setMessage('')
    setLoading(true)

    try {
      const response = await axios.post('/api/tianxun-ai/chat', {
        message: userMessage.content,
        session_id: sessionId,
        module_context: moduleContext
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.result.message,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('发送消息失败:', error)
      const errorMessage = {
        role: 'assistant',
        content: '抱歉，发生了错误，请稍后重试。',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card
      title={
        <Space>
          <RobotOutlined />
          <span>天巡AI</span>
        </Space>
      }
      className="tianxun-ai-card"
      style={{ height: '600px', display: 'flex', flexDirection: 'column' }}
      bodyStyle={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '16px' }}
    >
      <div className="messages-container">
        <List
          dataSource={messages}
          renderItem={(item) => (
            <List.Item style={{ border: 'none', padding: '8px 0' }}>
              <Space align="start" style={{ width: '100%' }}>
                <Avatar
                  icon={item.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
                  style={{
                    backgroundColor: item.role === 'user' ? '#1890ff' : '#52c41a'
                  }}
                />
                <div className="message-content">
                  <div className="message-text">{item.content}</div>
                </div>
              </Space>
            </List.Item>
          )}
        />
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <TextArea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onPressEnter={(e) => {
            if (!e.shiftKey) {
              e.preventDefault()
              sendMessage()
            }
          }}
          placeholder="输入消息..."
          rows={3}
          style={{ marginBottom: '8px' }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={sendMessage}
          loading={loading}
          block
        >
          发送
        </Button>
      </div>
    </Card>
  )
}

export default TianxunAI

