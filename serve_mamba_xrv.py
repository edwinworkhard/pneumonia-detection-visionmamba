import os
import io
import time
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
try:
    import torch
    import torch.nn.functional as F
    TORCH_OK = True
except Exception:
    TORCH_OK = False


APP_TITLE = 'Pneumonia Detection - Threshold Switchable'
PRIMARY_THRESHOLD = 0.275  # high sensitivity
ALT_THRESHOLD = 0.425      # balanced F1
CKPT_PATH = 'best_mamba_xrv.pth'
UPLOAD_DIR = 'uploads'
SKIP_MODEL = os.getenv('SKIP_MODEL', '0') == '1'
if SKIP_MODEL:
    TORCH_OK = False

app = Flask(__name__, static_folder='static', template_folder='templates')
os.makedirs(UPLOAD_DIR, exist_ok=True)


def build_model(device):
    try:
        from models_mamba import VisionMamba
        model = VisionMamba(
            img_size=224,
            patch_size=16,
            stride=8,
            depth=24,
            embed_dim=192,
            d_state=16,
            channels=1,
            num_classes=2,
            final_pool_type='mean',
            if_abs_pos_embed=True,
            if_rope=False,
            if_cls_token=True,
            use_middle_cls_token=True,
            if_divide_out=True,
        ).to(device)
        used_simple = False
    except Exception:
        from train_mamba_simple import SimpleVisionMamba
        model = SimpleVisionMamba(
            img_size=224,
            patch_size=16,
            in_chans=1,
            num_classes=2,
            embed_dim=192,
            depth=12,
        ).to(device)
        used_simple = True
    return model, used_simple


def get_transform():
    from torchvision import transforms
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])


if not TORCH_OK:
    device = 'disabled'
    model = None
    used_simple = False
    tfm = None
else:
    try:
        # Global model state
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model, used_simple = build_model(device)
        state_dict = torch.load(CKPT_PATH, map_location=device, weights_only=False)
        state_dict = state_dict.get('model_state') or state_dict.get('model') or state_dict
        try:
            model.load_state_dict(state_dict)
        except Exception:
            if not used_simple:
                from train_mamba_simple import SimpleVisionMamba
                model = SimpleVisionMamba(img_size=224, patch_size=16, in_chans=1, num_classes=2, embed_dim=192, depth=12).to(device)
                model.load_state_dict(state_dict)
            else:
                raise
        model.eval()
        tfm = get_transform()
    except Exception as e:
        print(f"Warning: Could not load model from {CKPT_PATH}: {e}")
        print("Running in demo mode without model predictions")
        TORCH_OK = False
        device = 'disabled'
        model = None
        used_simple = False
        tfm = None


def infer_image(image: Image.Image, threshold: float):
    if not TORCH_OK:
        # UI验证模式：不加载模型，返回固定值，便于检查页面功能
        prob_pneu = 0.0
        pred_label = int(prob_pneu >= threshold)
        return prob_pneu, pred_label
    x = tfm(image).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = F.softmax(logits, dim=1).cpu().numpy()[0]
    prob_pneu = float(probs[1])
    pred_label = int(prob_pneu >= threshold)
    return prob_pneu, pred_label


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=APP_TITLE, primary=PRIMARY_THRESHOLD, alt=ALT_THRESHOLD)


@app.route('/predict', methods=['POST'])
def predict():
    # threshold selection
    mode = request.form.get('threshold_mode', 'primary')
    custom_val = request.form.get('custom_threshold', '')
    threshold = PRIMARY_THRESHOLD if mode == 'primary' else ALT_THRESHOLD
    if mode == 'custom':
        try:
            threshold = float(custom_val)
        except Exception:
            threshold = PRIMARY_THRESHOLD

    file = request.files.get('image')
    if not file or file.filename == '':
        return redirect(url_for('index'))

    # save upload
    filename = str(int(time.time() * 1000)) + '_' + file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # open with PIL and infer
    image = Image.open(save_path).convert('RGB')
    prob_pneu, pred_label = infer_image(image, threshold)

    result = {
        'path': filename,
        'threshold_used': threshold,
        'prob_pneumonia': round(prob_pneu, 6),
        'pred_label': int(pred_label),
        'label_text': 'PNEUMONIA' if pred_label == 1 else 'NORMAL',
    }
    return render_template('result.html', title=APP_TITLE, result=result, primary=PRIMARY_THRESHOLD, alt=ALT_THRESHOLD)


@app.route('/uploads/<path:fname>')
def serve_upload(fname):
    return send_from_directory(UPLOAD_DIR, fname)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    # JSON or form with optional threshold
    threshold = request.form.get('threshold') or (request.json.get('threshold') if request.is_json else None)
    try:
        thr = float(threshold) if threshold is not None else PRIMARY_THRESHOLD
    except Exception:
        thr = PRIMARY_THRESHOLD

    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'missing image'}), 400
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    prob_pneu, pred_label = infer_image(image, thr)
    return jsonify({
        'threshold_used': thr,
        'prob_pneumonia': prob_pneu,
        'pred_label': int(pred_label),
        'label_text': 'PNEUMONIA' if pred_label == 1 else 'NORMAL'
    })


if __name__ == '__main__':
    print(f'Using device: {device}\nCheckpoint: {CKPT_PATH}\nPrimary threshold: {PRIMARY_THRESHOLD} | Alt: {ALT_THRESHOLD}\nSkip model: {SKIP_MODEL} | Torch ok: {TORCH_OK}')
    # Use a non-default port to avoid conflicts with other local services that may respond with plain text like "ok".
    app.run(host='0.0.0.0', port=5175, debug=False)