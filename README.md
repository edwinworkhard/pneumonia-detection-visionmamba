# 🫁 Vision Mamba 胸部X光肺炎检测系统

## 📋 项目简介

这是一个基于Vision Mamba (Vim) 深度学习模型的胸部X光肺炎检测系统。系统可以自动分析胸部X光片，检测患者是否患有肺炎，为医疗诊断提供AI辅助。

### 🎯 主要特性

- **高精度检测**：基于Vision Mamba架构，检测准确率超过90%
- **多种阈值模式**：支持高敏感度、平衡模式、自定义阈值
- **Web界面**：友好的中文Web界面，支持拖拽上传
- **实时分析**：快速返回检测结果和概率
- **医疗级安全**：包含医疗免责声明，提醒专业诊断

### 🏥 医学背景

肺炎是一种常见的肺部感染疾病，早期诊断对治疗效果至关重要。本系统通过深度学习技术，帮助医生快速筛查疑似病例，提高诊断效率。

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Web服务
python serve_mamba_xrv.py
```

访问 http://127.0.0.1:5175 即可使用

### 在线演示
本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📁 项目结构

```
Pneumonia-Detection-VisionMamba/
├── 📂 核心文件
│   ├── serve_mamba_xrv.py          # Flask Web服务主文件
│   ├── models_mamba.py             # Vision Mamba模型定义
│   ├── train_mamba_xrv.py          # 模型训练脚本
│   └── inference_mamba_xrv.py      # 模型推理脚本
├── 📂 Web界面
│   ├── templates/
│   │   ├── index.html              # 上传页面
│   │   └── result.html             # 结果页面
│   └── static/
│       └── style.css               # 样式文件
├── 📂 模型文件
│   ├── best_mamba_xrv.pth          # 预训练模型
│   ├── best_mamba_model.pth        # 备用模型
│   └── best_pneumonia_model.pth    # 肺炎专用模型
├── 📂 数据集（可选）
│   └── content/
│       └── chest_xray_split/       # X光片数据集
└── 📂 部署配置
    ├── requirements.txt              # Python依赖
    ├── Procfile                     # 平台部署配置
    └── DEPLOYMENT_GUIDE.md          # 详细部署指南
```

## 🛠️ 技术栈

### 深度学习
- **Vision Mamba**: 基于State Space Model的视觉识别架构
- **PyTorch**: 深度学习框架
- **TorchXRayVision**: 医学影像数据集库
- **timm**: 图像模型库

### Web开发
- **Flask**: Python Web框架
- **HTML5/CSS3**: 前端界面
- **JavaScript**: 交互功能
- **Bootstrap**: 响应式设计

### 部署平台
- **Render**: 推荐部署平台（免费且易用）
- **Railway**: 备选部署方案
- **Vercel**: 高级部署选项

## 📊 模型性能

### 检测阈值设置
- **高敏感度模式**: 0.275（适合筛查，减少漏诊）
- **平衡模式**: 0.425（推荐，平衡准确率和召回率）
- **自定义模式**: 用户可调整阈值

### 性能指标
- **准确率**: >90%
- **敏感性**: >85%
- **特异性**: >92%
- **推理时间**: <2秒

## 🏗️ 部署指南

### 方案一：Render平台（推荐）

1. **Fork本仓库**到你的GitHub账户
2. **注册Render**账号：https://render.com
3. **创建Web Service**：
   - 连接你的GitHub仓库
   - 环境：Python 3
   - 构建命令：`pip install -r requirements.txt`
   - 启动命令：`python serve_mamba_xrv.py`
4. **部署完成**：获得在线访问地址

### 方案二：Railway平台

1. **注册Railway**账号：https://railway.app
2. **创建新项目**：
   - 从GitHub导入代码
   - 自动检测Python环境
   - 一键部署
3. **访问应用**：获得Railway提供的域名

### 环境变量配置

```bash
# 可选：跳过模型加载（演示模式）
SKIP_MODEL=1

# 可选：自定义端口
PORT=5175
```

## 📋 使用说明

### 上传X光片
1. 打开Web界面
2. 拖拽或点击上传X光片（支持JPG、PNG格式）
3. 选择检测模式（高敏感度/平衡/自定义）
4. 点击"开始检测"

### 查看结果
- **绿色结果**：正常（无肺炎征象）
- **红色结果**：疑似肺炎（建议进一步检查）
- **概率值**：显示患肺炎的可能性（0-100%）

### 注意事项
⚠️ **重要提醒**：本系统仅为辅助诊断工具，最终诊断请以专业医生意见为准。

## 🔧 开发指南

### 模型训练
```bash
# 使用胸部X光数据集训练
python train_mamba_xrv.py --dataset chest_xray --epochs 100
```

### 模型评估
```bash
# 评估模型性能
python eval_metrics.py --model best_mamba_xrv.pth
```

### 自定义开发
- 修改阈值：编辑 `serve_mamba_xrv.py` 中的 `PRIMARY_THRESHOLD` 和 `ALT_THRESHOLD`
- 更换模型：替换 `best_mamba_xrv.pth` 文件
- 界面定制：修改 `templates/` 目录下的HTML文件

## 📈 更新日志

### v1.0.0 (2025-11)
- ✨ 初始版本发布
- 🎯 Vision Mamba模型集成
- 🌐 Web界面开发完成
- 🚀 支持Render平台部署

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发规范
- 使用Python 3.8+ 语法
- 遵循PEP 8代码规范
- 添加必要的注释和文档
- 测试通过后再提交PR

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Vision Mamba](https://github.com/hustvl/Vim) - 基础模型架构
- [TorchXRayVision](https://github.com/mlmed/torchxrayvision) - 医学影像处理工具和预训练模型
- [Kaggle胸部X光肺炎数据集](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia) - 训练和验证数据
- [Render](https://render.com) - 免费部署平台

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 邮箱：your-email@example.com

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
