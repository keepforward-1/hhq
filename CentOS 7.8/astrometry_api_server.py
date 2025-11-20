#!/usr/bin/env python3
"""
Astrometry.net API服务器
在CentOS 7.8上运行，提供HTTP API接口
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import tempfile
import shutil
import time
from threading import Thread
import json

app = Flask(__name__)
CORS(app)

# 配置
ASTROMETRY_BIN = '/usr/local/astrometry/bin/solve-field'
UPLOAD_FOLDER = '/tmp/astrometry_uploads'
RESULTS_FOLDER = '/tmp/astrometry_results'
JOBS = {}  # 存储任务状态

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    """上传图片并开始解析"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        # 保存文件
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 生成任务ID
        job_id = str(int(time.time() * 1000))
        
        # 创建结果目录
        job_dir = os.path.join(RESULTS_FOLDER, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # 初始化任务状态
        JOBS[job_id] = {
            'status': 'processing',
            'filename': filename,
            'start_time': time.time()
        }
        
        # 在后台运行解析
        thread = Thread(target=solve_field, args=(job_id, filepath, job_dir))
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'processing',
            'message': '任务已提交'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def solve_field(job_id, filepath, output_dir):
    """执行solve-field命令"""
    try:
        # 构建命令
        cmd = [
            ASTROMETRY_BIN,
            filepath,
            '--out', os.path.join(output_dir, 'output'),
            '--overwrite',
            '--no-plots',
            '--no-verify',
            '--cpulimit', '300'  # 5分钟超时
        ]
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 检查结果
        output_file = os.path.join(output_dir, 'output.wcs')
        if os.path.exists(output_file):
            # 解析成功，读取WCS信息
            wcs_info = parse_wcs_file(output_file)
            
            JOBS[job_id] = {
                'status': 'success',
                'filename': JOBS[job_id]['filename'],
                'start_time': JOBS[job_id]['start_time'],
                'solve_time': time.time() - JOBS[job_id]['start_time'],
                'calibration': wcs_info
            }
        else:
            JOBS[job_id] = {
                'status': 'failure',
                'filename': JOBS[job_id]['filename'],
                'start_time': JOBS[job_id]['start_time'],
                'error': result.stderr
            }
            
    except subprocess.TimeoutExpired:
        JOBS[job_id] = {
            'status': 'failure',
            'filename': JOBS[job_id]['filename'],
            'start_time': JOBS[job_id]['start_time'],
            'error': '解析超时'
        }
    except Exception as e:
        JOBS[job_id] = {
            'status': 'failure',
            'filename': JOBS[job_id]['filename'],
            'start_time': JOBS[job_id]['start_time'],
            'error': str(e)
        }

def parse_wcs_file(wcs_file):
    """解析WCS文件，提取坐标信息"""
    try:
        from astropy import wcs
        from astropy.io import fits
        
        with fits.open(wcs_file) as hdul:
            w = wcs.WCS(hdul[0].header)
            
            # 获取中心坐标
            center = w.wcs_pix2world([[w.naxis1/2, w.naxis2/2]], 0)[0]
            ra = float(center[0])
            dec = float(center[1])
            
            # 获取视场大小
            corners = [
                [0, 0],
                [w.naxis1, 0],
                [w.naxis1, w.naxis2],
                [0, w.naxis2]
            ]
            world_corners = w.wcs_pix2world(corners, 0)
            
            # 计算视场宽度和高度
            ra_range = max([c[0] for c in world_corners]) - min([c[0] for c in world_corners])
            dec_range = max([c[1] for c in world_corners]) - min([c[1] for c in world_corners])
            
            # 获取方向角
            orientation = float(hdul[0].header.get('CROTA2', 0))
            
            return {
                'ra': ra,
                'dec': dec,
                'field_width': ra_range,
                'field_height': dec_range,
                'orientation': orientation
            }
    except Exception as e:
        return {
            'ra': None,
            'dec': None,
            'field_width': None,
            'field_height': None,
            'orientation': None,
            'error': str(e)
        }

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """获取任务状态"""
    if job_id not in JOBS:
        return jsonify({'error': '任务不存在'}), 404
    
    return jsonify(JOBS[job_id]), 200

@app.route('/jobs/<job_id>/info', methods=['GET'])
def get_job_info(job_id):
    """获取任务详细信息"""
    if job_id not in JOBS:
        return jsonify({'error': '任务不存在'}), 404
    
    job = JOBS[job_id]
    
    if job['status'] == 'success':
        return jsonify({
            'status': 'success',
            'calibration': job.get('calibration', {}),
            'solve_time': job.get('solve_time', 0)
        }), 200
    elif job['status'] == 'failure':
        return jsonify({
            'status': 'failure',
            'error': job.get('error', '未知错误')
        }), 200
    else:
        return jsonify({
            'status': 'processing',
            'message': '任务处理中'
        }), 200

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'astrometry_bin': ASTROMETRY_BIN,
        'bin_exists': os.path.exists(ASTROMETRY_BIN)
    }), 200

if __name__ == '__main__':
    print("Astrometry.net API服务器启动...")
    print(f"Astrometry二进制路径: {ASTROMETRY_BIN}")
    app.run(host='0.0.0.0', port=5000, debug=True)

