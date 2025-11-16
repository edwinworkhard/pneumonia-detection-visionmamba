# 肺炎检测系统部署指南

## 项目概述
基于Vision Mamba的胸部X光肺炎检测系统，支持在线上传X光片进行肺炎检测。

## 部署步骤（Render平台）

### 1. 准备工作
- 注册GitHub账号（如果还没有）
- 注册Render账号：https://render.com

### 2. 上传代码到GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin [你的GitHub仓库地址]
git push -u origin main
```

### 3. 在Render上部署
1. 登录Render控制台
2. 点击 "New Web Service"
3. 连接你的GitHub仓库
4. 配置环境：
   - Name: pneumonia-detection
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn serve_mamba_xrv:app

### 4. 环境变量设置（可选）
- SKIP_MODEL: 设置为1可以跳过模型加载（演示模式）

## 访问地址
部署完成后，你会得到一个类似 https://pneumonia-detection-xxx.onrender.com 的访问地址

## 注意事项
- 免费账户有15分钟的休眠时间
- 上传文件大小限制为100MB
- 建议使用压缩后的模型文件以提高加载速度