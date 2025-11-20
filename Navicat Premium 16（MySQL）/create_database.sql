-- 基于多源星图识别的天文观测辅助系统数据库
-- MySQL数据库创建脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS astronomy_system 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE astronomy_system;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(80) UNIQUE NOT NULL COMMENT '用户名',
    email VARCHAR(120) UNIQUE NOT NULL COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    nickname VARCHAR(80) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 星系分类记录表
CREATE TABLE IF NOT EXISTS galaxy_classifications (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    image_path VARCHAR(255) NOT NULL COMMENT '图片路径',
    predicted_class INT NOT NULL COMMENT '预测类别',
    confidence FLOAT NOT NULL COMMENT '置信度',
    class_name VARCHAR(50) COMMENT '类别名称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='星系分类记录表';

-- 星座识别记录表
CREATE TABLE IF NOT EXISTS constellation_recognitions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    image_path VARCHAR(255) NOT NULL COMMENT '图片路径',
    detected_constellations TEXT COMMENT '检测到的星座（JSON格式）',
    confidence FLOAT COMMENT '置信度',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='星座识别记录表';

-- 天体定位记录表
CREATE TABLE IF NOT EXISTS celestial_positionings (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    image_path VARCHAR(255) NOT NULL COMMENT '图片路径',
    ra FLOAT COMMENT '赤经（度）',
    dec FLOAT COMMENT '赤纬（度）',
    field_width FLOAT COMMENT '视场宽度（度）',
    field_height FLOAT COMMENT '视场高度（度）',
    orientation FLOAT COMMENT '方向角（度）',
    solved BOOLEAN DEFAULT FALSE COMMENT '是否成功解析',
    solve_time FLOAT COMMENT '解析耗时（秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_solved (solved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='天体定位记录表';

-- 太空引擎数据表
CREATE TABLE IF NOT EXISTS space_engine_data (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    data_type VARCHAR(50) NOT NULL COMMENT '数据类型：galaxy/constellation/positioning',
    source_id INT COMMENT '来源数据ID',
    celestial_object VARCHAR(100) COMMENT '天体对象名称',
    ra FLOAT COMMENT '赤经（度）',
    dec FLOAT COMMENT '赤纬（度）',
    distance FLOAT COMMENT '距离（光年）',
    view_data TEXT COMMENT '视图数据（JSON格式）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_data_type (data_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='太空引擎数据表';

-- 天巡AI聊天记录表
CREATE TABLE IF NOT EXISTS tianxun_ai_chats (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    session_id VARCHAR(100) NOT NULL COMMENT '会话ID',
    role VARCHAR(20) NOT NULL COMMENT '角色：user/assistant',
    content TEXT NOT NULL COMMENT '消息内容',
    module_context VARCHAR(50) COMMENT '关联模块：galaxy/constellation/positioning/space_engine',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='天巡AI聊天记录表';

-- 首页内容表
CREATE TABLE IF NOT EXISTS homepage_contents (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    content_type VARCHAR(50) NOT NULL COMMENT '内容类型：background/carousel/update/knowledge',
    title VARCHAR(200) COMMENT '标题',
    content TEXT COMMENT '内容',
    image_url VARCHAR(255) COMMENT '图片URL',
    link_url VARCHAR(255) COMMENT '链接URL',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_content_type (content_type),
    INDEX idx_is_active (is_active),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='首页内容表';

-- 插入示例数据
-- 首页轮播图
INSERT INTO homepage_contents (content_type, title, content, image_url, link_url, sort_order) VALUES
('carousel', '探索宇宙', '发现星系的奥秘', '/images/carousel1.jpg', '#', 1),
('carousel', '星座识别', '识别夜空中的星座', '/images/carousel2.jpg', '#', 2),
('carousel', '天体定位', '精确定位天体位置', '/images/carousel3.jpg', '#', 3);

-- 平台更新
INSERT INTO homepage_contents (content_type, title, content, sort_order) VALUES
('update', '系统上线', '天文观测辅助系统正式上线，欢迎使用！', 1),
('update', '新增功能', '新增太空引擎模块，可以探索整个宇宙', 2);

-- 天文科普
INSERT INTO homepage_contents (content_type, title, content, sort_order) VALUES
('knowledge', '什么是星系？', '星系是由恒星、行星、气体、尘埃和暗物质组成的巨大系统。', 1),
('knowledge', '星座的起源', '星座是人类为了识别和记忆星空而划分的区域。', 2);

-- 登录页背景
INSERT INTO homepage_contents (content_type, title, image_url, sort_order) VALUES
('background', '登录背景', '/images/login_bg.jpg', 1);

