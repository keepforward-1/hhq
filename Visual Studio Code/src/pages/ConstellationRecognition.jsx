import React, { useState, useEffect } from 'react'
import { Layout, Card, Upload, Button, message, Table, Tag, Space, Row, Col } from 'antd'
import { UploadOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import TianxunAI from '../components/TianxunAI'
import axios from 'axios'
import './ModulePage.css'

const { Header, Content } = Layout

const ConstellationRecognition = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  const handleUpload = async (file) => {
    setLoading(true)
    const formData = new FormData()
    formData.append('image', file)

    try {
      const response = await axios.post('/api/constellation/recognize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResult(response.data.result)
      message.success('识别成功！')
      loadHistory()
    } catch (error) {
      message.error(error.response?.data?.error || '识别失败')
    } finally {
      setLoading(false)
    }
  }

  const loadHistory = async () => {
    try {
      const response = await axios.get('/api/constellation/history')
      setHistory(response.data.history || [])
    } catch (error) {
      console.error('加载历史失败:', error)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  return (
    <Layout className="module-layout">
      <Header className="module-header">
        <Space>
          <Button
            type="text"
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/')}
            style={{ color: '#fff' }}
          >
            返回首页
          </Button>
          <h2 style={{ color: '#fff', margin: 0 }}>星座识别</h2>
        </Space>
      </Header>

      <Content className="module-content">
        <div className="module-wrapper">
          <Row gutter={24}>
            <Col xs={24} lg={18}>
              <Card title="上传星座图片" className="module-card">
                <Upload
                  beforeUpload={(file) => {
                    handleUpload(file)
                    return false
                  }}
                  accept="image/*"
                  showUploadList={false}
                >
                  <Button
                    type="primary"
                    icon={<UploadOutlined />}
                    loading={loading}
                    size="large"
                    block
                  >
                    选择图片
                  </Button>
                </Upload>

                {result && (
                  <div style={{ marginTop: '24px' }}>
                    <h3>识别结果</h3>
                    <p><strong>检测到星座数量：</strong>{result.count}</p>
                    <p><strong>平均置信度：</strong>{(result.confidence * 100).toFixed(2)}%</p>
                    {result.detected_constellations && (
                      <div>
                        <h4>检测到的星座：</h4>
                        {result.detected_constellations.map((item, index) => (
                          <Tag key={index} color="green">
                            {item.class} ({(item.confidence * 100).toFixed(1)}%)
                          </Tag>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </Card>
            </Col>

            <Col xs={24} lg={6}>
              <TianxunAI moduleContext="constellation" />
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  )
}

export default ConstellationRecognition

