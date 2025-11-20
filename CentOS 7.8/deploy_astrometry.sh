#!/bin/bash
# Astrometry.net 0.80 在 CentOS 7.8 上的部署脚本
# 基于 https://plaidhat.com/code/astrometry080-centos78.php

set -e

echo "=========================================="
echo "开始部署 Astrometry.net 0.80"
echo "=========================================="

# 1. 系统准备
echo "1. 系统准备..."
sudo yum -y update

# 安装基础开发工具
sudo yum -y groupinstall "Development Tools"
sudo yum -y install epel-release

# 2. 安装依赖
echo "2. 安装依赖包..."
sudo yum -y install \
    cairo cairo-devel \
    libpng libpng-devel \
    libjpeg-turbo libjpeg-turbo-devel \
    zlib zlib-devel \
    bzip2-libs bzip2-devel \
    python3 python3-devel python3-pip \
    netpbm netpbm-devel netpbm-progs \
    pyfits pyfits-tools \
    cfitsio cfitsio-devel \
    swig \
    wget

# 安装Python包
echo "3. 安装Python包..."
sudo pip3 install numpy
sudo pip3 install astropy

# 3. 下载并编译Astrometry.net
echo "4. 下载Astrometry.net..."
cd /tmp
wget http://astrometry.net/downloads/astrometry.net-0.80.tar.gz
tar zxvf astrometry.net-0.80.tar.gz
cd astrometry.net-0.80

# 4. 配置NetPBM
echo "5. 配置NetPBM..."
cd util/
cat > makefile.netpbm << 'EOF'
NETPBM_INC ?= -I/usr/include/netpbm
NETPBM_LIB ?= -L/usr/lib64 -lnetpbm
EOF
cd ..

# 5. 编译
echo "6. 编译Astrometry.net..."
make
make py
make extra

# 6. 安装
echo "7. 安装Astrometry.net..."
sudo make install

# 7. 设置环境变量
echo "8. 设置环境变量..."
export PATH=${PATH}:/usr/local/astrometry/bin
echo 'export PATH=${PATH}:/usr/local/astrometry/bin' >> ~/.bashrc

# 8. 创建数据目录
echo "9. 创建数据目录..."
sudo mkdir -p /usr/local/astrometry/data
sudo chmod 755 /usr/local/astrometry/data

# 9. 下载索引文件（宽视场，约400MB）
echo "10. 下载索引文件（宽视场）..."
cd /usr/local/astrometry/data
for i in $(seq -w 7 19); do
    echo "下载 index-41$i.fits..."
    sudo wget -q http://data.astrometry.net/4100/index-41$i.fits
done

# 10. 测试
echo "11. 测试安装..."
/usr/local/astrometry/bin/solve-field --version

echo "=========================================="
echo "Astrometry.net 0.80 部署完成！"
echo "=========================================="
echo ""
echo "安装路径：/usr/local/astrometry"
echo "数据路径：/usr/local/astrometry/data"
echo ""
echo "测试命令："
echo "  /usr/local/astrometry/bin/solve-field <image_file>"
echo ""

