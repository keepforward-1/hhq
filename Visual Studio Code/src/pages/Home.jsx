import React, { useState, useEffect } from 'react'
import { Layout, Carousel, Card, Row, Col, Button, Typography, Space } from 'antd'
import { useNavigate } from 'react-router-dom'
import { 
  StarOutlined, 
  GlobalOutlined, 
  CompassOutlined, 
  RocketOutlined,
  UserOutlined,
  LogoutOutlined
} from '@ant-design/icons'
import { useAuth } from '../contexts/AuthContext'
import TianxunAI from '../components/TianxunAI'
import axios from 'axios'
import './Home.css'

const { Header, Content, Footer } = Layout
const { Title, Paragraph } = Typography

const Home = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [carouselImages, setCarouselImages] = useState([])
  const [updates, setUpdates] = useState([])
  const [knowledge, setKnowledge] = useState([])

  useEffect(() => {
    loadHomepageContent()
  }, [])

  const loadHomepageContent = async () => {
    try {
      // 加载轮播图
      const carouselRes = await axios.get('/api/homepage/content?type=carousel')
      setCarouselImages(carouselRes.data.contents || [])

      // 加载平台更新
      const updateRes = await axios.get('/api/homepage/content?type=update')
      setUpdates(updateRes.data.contents || [])

      // 加载天文科普
      const knowledgeRes = await axios.get('/api/homepage/content?type=knowledge')
      setKnowledge(knowledgeRes.data.contents || [])
    } catch (error) {
      console.error('加载首页内容失败:', error)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <Layout className="home-layout">
      <Header className="home-header">
        <div className="header-left">
          <Title level={3} style={{ color: '#fff', margin: 0 }}>
            <StarOutlined /> 你的专属天文台
          </Title>
        </div>
        <div className="header-right">
          <Space>
            <Button 
              type="text" 
              icon={<UserOutlined />}
              style={{ color: '#fff' }}
            >
              {user?.nickname || user?.username}
            </Button>
            <Button 
              type="text" 
              icon={<LogoutOutlined />}
              onClick={handleLogout}
              style={{ color: '#fff' }}
            >
              退出
            </Button>
          </Space>
        </div>
      </Header>

      <Content className="home-content">
        <div className="content-wrapper">
          {/* 轮播图 */}
          <div className="carousel-section">
            <Carousel autoplay>
              {carouselImages.map((item, index) => (
                <div key={index}>
                  <div 
                    className="carousel-item"
                    style={{
                      backgroundImage: `url(${item.image_url || '/default-bg.jpg'})`,
                      backgroundSize: 'cover',
                      backgroundPosition: 'center',
                      height: '400px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#fff'
                    }}
                  >
                    <div style={{ textAlign: 'center' }}>
                      <Title level={2} style={{ color: '#fff' }}>{item.title}</Title>
                      <Paragraph style={{ color: '#fff', fontSize: '18px' }}>
                        {item.content}
                      </Paragraph>
                    </div>
                  </div>
                </div>
              ))}
            </Carousel>
          </div>

          {/* 功能模块导航 */}
          <div className="modules-section">
            <Row gutter={[24, 24]}>
              <Col xs={24} sm={12} md={6}>
                <Card
                  className="module-card"
                  hoverable
                  cover={
                    <div className="module-icon">
                      <GlobalOutlined style={{ fontSize: '64px', color: '#1890ff' }} />
                    </div>
                  }
                  onClick={() => navigate('/galaxy')}
                >
                  <Card.Meta
                    title="星系分类"
                    description="使用AI模型识别和分类星系类型"
                  />
                </Card>
              </Col>

              <Col xs={24} sm={12} md={6}>
                <Card
                  className="module-card"
                  hoverable
                  cover={
                    <div className="module-icon">
                      <StarOutlined style={{ fontSize: '64px', color: '#fadb14' }} />
                    </div>
                  }
                  onClick={() => navigate('/constellation')}
                >
                  <Card.Meta
                    title="星座识别"
                    description="识别图片中的星座"
                  />
                </Card>
              </Col>

              <Col xs={24} sm={12} md={6}>
                <Card
                  className="module-card"
                  hoverable
                  cover={
                    <div className="module-icon">
                      <CompassOutlined style={{ fontSize: '64px', color: '#52c41a' }} />
                    </div>
                  }
                  onClick={() => navigate('/positioning')}
                >
                  <Card.Meta
                    title="天体定位"
                    description="精确计算天体的坐标位置"
                  />
                </Card>
              </Col>

              <Col xs={24} sm={12} md={6}>
                <Card
                  className="module-card"
                  hoverable
                  cover={
                    <div className="module-icon">
                      <RocketOutlined style={{ fontSize: '64px', color: '#eb2f96' }} />
                    </div>
                  }
                  onClick={() => navigate('/space-engine')}
                >
                  <Card.Meta
                    title="太空引擎"
                    description="高仿真3D宇宙模拟"
                  />
                </Card>
              </Col>
            </Row>
          </div>

          {/* 天巡AI和内容区域 */}
          <Row gutter={24} style={{ marginTop: '24px' }}>
            <Col xs={24} lg={6}>
              <TianxunAI />
            </Col>
            <Col xs={24} lg={18}>
              <Row gutter={[16, 16]}>
                <Col xs={24} md={12}>
                  <Card title="平台更新" className="content-card">
                    {updates.map((item, index) => (
                      <div key={index} style={{ marginBottom: '16px' }}>
                        <Title level={5}>{item.title}</Title>
                        <Paragraph>{item.content}</Paragraph>
                      </div>
                    ))}
                  </Card>
                </Col>
                <Col xs={24} md={12}>
                  <Card title="天文科普" className="content-card">
                    {knowledge.map((item, index) => (
                      <div key={index} style={{ marginBottom: '16px' }}>
                        <Title level={5}>{item.title}</Title>
                        <Paragraph>{item.content}</Paragraph>
                      </div>
                    ))}
                  </Card>
                </Col>
              </Row>
            </Col>
          </Row>
        </div>
      </Content>

      <Footer style={{ textAlign: 'center', background: '#001529', color: '#fff' }}>
        基于多源星图识别的天文观测辅助系统 ©2025
      </Footer>
    </Layout>
  )
}

export default Home

