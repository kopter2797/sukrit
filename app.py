from flask import Flask, render_template, request, jsonify
from crypto_assignment import VigenereCipher, AutokeyCipher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    keyword = data.get('keyword', '')
    cipher_type = data.get('cipher_type', 'vigenere')
    action = data.get('action', 'encrypt')

    if not text or not keyword:
        return jsonify({'error': 'กรุณากรอกข้อมูลให้ครบถ้วน (Please provide both text and keyword)'}), 400

    try:
        if cipher_type == 'vigenere':
            cipher = VigenereCipher(keyword)
        elif cipher_type == 'autokey':
            cipher = AutokeyCipher(keyword)
        else:
            return jsonify({'error': 'ประเภทการเข้ารหัสไม่ถูกต้อง (Invalid cipher type)'}), 400

        if action == 'encrypt':
            result = cipher.encrypt(text)
        elif action == 'decrypt':
            result = cipher.decrypt(text)
        else:
            return jsonify({'error': 'คำสั่งไม่ถูกต้อง (Invalid action)'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
