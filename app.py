from flask import Flask, render_template, request, jsonify
from crypto_assignment import VigenereCipher, AutokeyCipher, SecureDataIntegrity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    keyword = data.get('keyword', '')
    cipher_type = data.get('cipher_type', 'vigenere')
    action = data.get('action', 'encrypt')
    
    # New security parameters
    use_security = data.get('use_security', False)
    # Secret Key is now derived from the keyword itself!
    secret_key = keyword if use_security else None

    if not text or not keyword:
        return jsonify({'error': 'กรุณากรอกข้อมูลให้ครบถ้วน (Please provide both text and keyword)'}), 400

    try:
        if cipher_type == 'vigenere':
            cipher = VigenereCipher(keyword)
        elif cipher_type == 'autokey':
            cipher = AutokeyCipher(keyword)
        else:
            return jsonify({'error': 'ประเภทการเข้ารหัสไม่ถูกต้อง (Invalid cipher type)'}), 400

        # Security Logic Layer
        security = None
        if use_security:
             # Use the keyword as the secret key
             security = SecureDataIntegrity(secret_key)

        if action == 'encrypt':
            result = cipher.encrypt(text)
            
            # Apply signature if security is on
            if security:
                result = security.sign_data(result)
                return jsonify({'result': result, 'signed': True})
                
        elif action == 'decrypt':
            # Verify signature first if security is on
            is_verified = False
            if security:
                is_valid, verified_data = security.verify_data(text)
                if not is_valid:
                    return jsonify({'error': 'ตรวจพบการปลอมแปลง! (Tampering Detected) ข้อมูลไม่ถูกต้องหรือถูกแก้ไข'}), 400
                # Use the verified data for decryption
                text = verified_data
                is_verified = True
                
            result = cipher.decrypt(text)
            
            if is_verified:
                 return jsonify({'result': result, 'verified': True})
        else:
            return jsonify({'error': 'คำสั่งไม่ถูกต้อง (Invalid action)'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
