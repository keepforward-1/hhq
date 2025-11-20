import React, { useRef, useEffect } from 'react'
import { Layout, Card, Space, Button, Row, Col } from 'antd'
import { ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars, PerspectiveCamera } from '@react-three/drei'
import TianxunAI from '../components/TianxunAI'
import './ModulePage.css'

const { Header, Content } = Layout

const SpaceEngine = () => {
  const navigate = useNavigate()

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
          <h2 style={{ color: '#fff', margin: 0 }}>太空引擎</h2>
        </Space>
      </Header>

      <Content className="module-content">
        <div className="module-wrapper">
          <Row gutter={24}>
            <Col xs={24} lg={18}>
              <Card title="3D宇宙模拟" className="module-card" style={{ height: '600px' }}>
                <Canvas style={{ width: '100%', height: '500px', background: '#000' }}>
                  <PerspectiveCamera makeDefault position={[0, 0, 5]} />
                  <ambientLight intensity={0.5} />
                  <pointLight position={[10, 10, 10]} />
                  <Stars radius={300} depth={60} count={20000} factor={7} fade speed={1} />
                  <OrbitControls enableDamping dampingFactor={0.05} />
                </Canvas>
                <p style={{ marginTop: '16px', color: '#fff' }}>
                  使用鼠标拖拽旋转视角，滚轮缩放
                </p>
              </Card>
            </Col>

            <Col xs={24} lg={6}>
              <TianxunAI moduleContext="space_engine" />
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  )
}

export default SpaceEngine

