import React, { useState, useEffect } from 'react'
import { Layout, Card, Upload, Button, message, Space, Row, Col, Spin } from 'antd'
import { UploadOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import TianxunAI from '../components/TianxunAI'
import axios from 'axios'
import './ModulePage.css'

const { Header, Content } = Layout

const CelestialPositioning = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleUpload = async (file) => {
    setLoading(true)
    setResult(null)
    const formData = new FormData()
    formData.append('image', file)

    try {
      const response = await axios.post('/api/positioning/solve', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 300000 // 5分钟超时
      })

      setResult(response.data.result)
      if (response.data.result.solved) {
        message.success('解析成功！')
      } else {
        message.warning('解析失败，请检查图片')
      }
    } catch (error) {
      message.error(error.response?.data?.error || '解析失败')
    } finally {
      setLoading(false)
    }
  }

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
          <h2 style={{ color: '#fff', margin: 0 }}>天体定位</h2>
        </Space>
      </Header>

      <Content className="module-content">
        <div className="module-wrapper">
          <Row gutter={24}>
            <Col xs={24} lg={18}>
              <Card title="上传天体图片" className="module-card">
                <Upload
                  beforeUpload={(file) => {
                    handleUpload(file)
                    return false
                  }}
                  accept="image/*,.fits,.fit"
                  showUploadList={false}
                >
                  <Button
                    type="primary"
                    icon={<UploadOutlined />}
                    loading={loading}
                    size="large"
                    block
                    disabled={loading}
                  >
                    {loading ? '解析中...' : '选择图片'}
                  </Button>
                </Upload>

                {loading && (
                  <div style={{ textAlign: 'center', marginTop: '24px' }}>
                    <Spin size="large" />
                    <p style={{ marginTop: '16px' }}>正在解析，请稍候...</p>
                  </div>
                )}

                {result && result.solved && (
                  <div style={{ marginTop: '24px' }}>
                    <h3>解析结果</h3>
                    <p><strong>赤经（RA）：</strong>{result.ra?.toFixed(6)}°</p>
                    <p><strong>赤纬（Dec）：</strong>{result.dec?.toFixed(6)}°</p>
                    <p><strong>视场宽度：</strong>{result.field_width?.toFixed(4)}°</p>
                    <p><strong>视场高度：</strong>{result.field_height?.toFixed(4)}°</p>
                    <p><strong>方向角：</strong>{result.orientation?.toFixed(2)}°</p>
                    <p><strong>解析耗时：</strong>{result.solve_time?.toFixed(2)}秒</p>
                  </div>
                )}

                {result && !result.solved && (
                  <div style={{ marginTop: '24px' }}>
                    <p style={{ color: '#ff4d4f' }}>解析失败，请检查图片是否符合要求</p>
                  </div>
                )}
              </Card>
            </Col>

            <Col xs={24} lg={6}>
              <TianxunAI moduleContext="positioning" />
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  )
}

export default CelestialPositioning

