import requests
import json

BASE_URL = "http://127.0.0.1:5000/process"

def test_recovery_flow():
    print("--- Testing Recovery System ---")
    
    # 1. Encrypt with Recovery
    payload = {
        "text": "LOVE",
        "keyword": "KEY",
        "cipher_type": "vigenere",
        "action": "encrypt",
        "use_security": True,
        "use_recovery": True
    }
    
    response = requests.post(BASE_URL, json=payload)
    if response.status_code != 200:
        print(f"FAILED: Encryption error {response.text}")
        return

    data = response.json()
    encrypted_packet = data['result']
    print(f"Encrypted Packet: {encrypted_packet}")
    
    if "||__BACKUP__||" not in encrypted_packet:
        print("FAILED: Recovery separator not found in packet.")
        return

    # 2. Decrypt Normal (Should work)
    payload_decrypt = {
        "text": encrypted_packet,
        "keyword": "KEY",
        "cipher_type": "vigenere",
        "action": "decrypt",
        "use_security": True,
        "use_recovery": True
    }
    
    response = requests.post(BASE_URL, json=payload_decrypt)
    res_data = response.json()
    
    if res_data.get('result') == "LOVE" and "Normal" in res_data.get('recovery_status', ''):
        print(" PASS: Normal Decryption")
    else:
        print(f"FAILED: Normal Decryption - {res_data}")

    # 3. Tamper Primary and Decrypt (Should Recover)
    parts = encrypted_packet.split("||__BACKUP__||")
    # Modify first char of first part
    tampered_primary = "X" + parts[0][1:] 
    tampered_packet = f"{tampered_primary}||__BACKUP__||{parts[1]}"
    
    payload_tamper = payload_decrypt.copy()
    payload_tamper['text'] = tampered_packet
    
    response = requests.post(BASE_URL, json=payload_tamper)
    res_data = response.json()
    
    if res_data.get('result') == "LOVE" and "Recovered" in res_data.get('recovery_status', ''):
         print(" PASS: Recovery from Primary Tampering")
    else:
        print(f"FAILED: Recovery - {res_data}")

    # 4. Tamper Both (Should Fail)
    tampered_backup = "X" + parts[1][1:]
    fully_tampered_packet = f"{tampered_primary}||__BACKUP__||{tampered_backup}"
    
    payload_fail = payload_decrypt.copy()
    payload_fail['text'] = fully_tampered_packet
    
    response = requests.post(BASE_URL, json=payload_fail)
    
    if response.status_code == 400 and "Recovery Failed" in response.json().get('error', ''):
        print(" PASS: Correctly Rejected Double Tampering")
    else:
        print(f"FAILED: Should have rejected but got {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        test_recovery_flow()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Flask server (app.py) is running on port 5000!")
