from crypto_assignment import VigenereCipher, AutokeyCipher, SecureDataIntegrity, DataRecoverySystem
from flask import Flask, render_template, request, jsonify

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
    use_recovery = data.get('use_recovery', False) # New flag for recovery system
    
    # Secret Key is now derived from the keyword itself!
    secret_key = keyword if use_security else None

    if not text or not keyword:
        return jsonify({'error': 'กรุณากรอกข้อมูลให้ครบถ้วน (Please provide both text and keyword)'}), 400

    print(f"DEBUG: Received Text for processing: {text!r}") # Debug input
    print(f"DEBUG: Config - Security: {use_security}, Recovery: {use_recovery}")

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

        # Recovery Logic Layer
        recovery = None
        if use_recovery:
            recovery = DataRecoverySystem()

        if action == 'encrypt':
            raw_ciphertext = cipher.encrypt(text)
            final_result = raw_ciphertext
            
            response = {'display_result': raw_ciphertext}
            
            # Apply signature if security is on
            if security:
                signed_result = security.sign_data(raw_ciphertext)
                final_result = signed_result
                response['signed'] = True
                
                # Apply recovery packet if recovery is on (MUST be done after signing)
                if recovery:
                    recovery_packet = recovery.create_recovery_packet(signed_result)
                    final_result = recovery_packet
                    response['recovered'] = False
            
            response['result'] = final_result
            return jsonify(response)
                
        elif action == 'decrypt':
            # Handle Recovery First (if enabled)
            recovery_status = None
            is_verified = False
            
            if use_recovery and recovery and security:
                # If recovery is on, we expect the format to be a recovery packet
                # We need the security object's verify_data method to check each part
                is_recovered_valid, recovered_data, status_msg = recovery.extract_and_recover(text, security.verify_data)
                
                if not is_recovered_valid:
                     return jsonify({'error': f'Recovery Failed: {status_msg}'}), 400
                
                # If valid, use the recovered data (which is the signed original)
                # But wait, extract_and_recover calls verify_data internally, so recovered_data is the RAW data (unsigned)
                text = recovered_data
                is_verified = True
                recovery_status = status_msg
                
            elif security:
                # Normal Security Check
                is_valid, verified_data = security.verify_data(text)
                if not is_valid:
                    return jsonify({'error': 'ตรวจพบการปลอมแปลง! (Tampering Detected) ข้อมูลไม่ถูกต้องหรือถูกแก้ไข'}), 400
                # Use the verified data for decryption
                text = verified_data
                is_verified = True
                
            result = cipher.decrypt(text)
            
            response = {'result': result}
            if is_verified:
                response['verified'] = True
            if recovery_status:
                response['recovery_status'] = recovery_status
                
            return jsonify(response)

        else:
            return jsonify({'error': 'คำสั่งไม่ถูกต้อง (Invalid action)'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
