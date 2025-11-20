import React, { useState } from 'react'
import { Layout, Card, Upload, Button, message, Table, Tag, Space } from 'antd'
import { UploadOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import TianxunAI from '../components/TianxunAI'
import axios from 'axios'
import './ModulePage.css'

const { Header, Content } = Layout

const GalaxyClassification = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  const handleUpload = async (file) => {
    setLoading(true)
    const formData = new FormData()
    formData.append('image', file)

    try {
      const response = await axios.post('/api/galaxy/classify', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResult(response.data.result)
      message.success('分类成功！')
      loadHistory()
    } catch (error) {
      message.error(error.response?.data?.error || '分类失败')
    } finally {
      setLoading(false)
    }
  }

  const loadHistory = async () => {
    try {
      const response = await axios.get('/api/galaxy/history')
      setHistory(response.data.history || [])
    } catch (error) {
      console.error('加载历史失败:', error)
    }
  }

  React.useEffect(() => {
    loadHistory()
  }, [])

  const columns = [
    {
      title: '图片',
      dataIndex: 'image_path',
      key: 'image_path',
      render: (text) => (
        <img src={`/${text}`} alt="galaxy" style={{ width: '80px', height: '80px', objectFit: 'cover' }} />
      )
    },
    {
      title: '类别',
      dataIndex: 'class_name',
      key: 'class_name',
      render: (text) => <Tag color="blue">{text}</Tag>
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (value) => `${(value * 100).toFixed(2)}%`
    },
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text) => new Date(text).toLocaleString('zh-CN')
    }
  ]

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
          <h2 style={{ color: '#fff', margin: 0 }}>星系分类</h2>
        </Space>
      </Header>

      <Content className="module-content">
        <div className="module-wrapper">
          <Row gutter={24}>
            <Col xs={24} lg={18}>
              <Card title="上传星系图片" className="module-card">
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
                    <h3>分类结果</h3>
                    <p><strong>类别：</strong>{result.class_name}</p>
                    <p><strong>置信度：</strong>{(result.confidence * 100).toFixed(2)}%</p>
                  </div>
                )}

                <div style={{ marginTop: '24px' }}>
                  <h3>历史记录</h3>
                  <Table
                    columns={columns}
                    dataSource={history}
                    rowKey="id"
                    pagination={{ pageSize: 10 }}
                  />
                </div>
              </Card>
            </Col>

            <Col xs={24} lg={6}>
              <TianxunAI moduleContext="galaxy" />
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  )
}

export default GalaxyClassification

