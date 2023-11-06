from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.get('data')
        
        if data:
            img_base64 = generate_qr_code(data)
            return jsonify({'img': img_base64, 'data': data})
    
    return render_template('index.html')

@app.route('/download/<data>')
def download(data):
    img_base64 = generate_qr_code(data)
    img_data = base64.b64decode(img_base64)
    
    filename = f'{data}.png'
    return send_file(BytesIO(img_data), as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
