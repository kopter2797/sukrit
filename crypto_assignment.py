import hmac
import hashlib

class VigenereCipher:
    # คลาสสำหรับ Vigenere Cipher: เป็นเหมือนเครื่องมือเข้ารหัสลับ
    
    def __init__(self, key):
        # จุดเริ่มต้น (Constructor): รับ 'กุญแจ' มาเตรียมไว้ใช้
        self.key = preprocess_text(key)
        # เอากุญแจไปล้างให้สะอาด (ตัดช่องว่าง, ทำเป็นตัวพิมพ์ใหญ่) ก่อนเก็บไว้ใช้งาน

    def encrypt(self, plaintext):
        # ฟังก์ชันเข้ารหัส: แปลงข้อความให้อ่านไม่รู้เรื่อง
        
        plaintext = preprocess_text(plaintext)
        # ล้างข้อความที่จะทำให้สะอาดก่อน
        
        ciphertext = []
        # เตรียมกล่องว่างๆ ไว้ใส่ตัวอักษรที่เข้ารหัสเสร็จแล้ว
        
        key_length = len(self.key)
        # วัดความยาวกุญแจว่ายาวเท่าไหร่ (เพื่อไว้ใช้วนซ้ำ)
        
        for i, char in enumerate(plaintext):
            # หยิบตัวอักษรมาทีละตัว พร้อมลำดับที่ (i)
            
            p_val = ord(char) - ord('A')
            # แปลงตัวอักษรเป็นตัวเลข (A=0, B=1, ... Z=25)
            
            k_char = self.key[i % key_length]
            # หยิบตัวอักษรจากกุญแจมาคู่กัน (ถ้ายาวไม่พอ ให้วนกลับไปใช้ตัวแรกใหม่)
            
            k_val = ord(k_char) - ord('A')
            # แปลงกุญแจเป็นตัวเลขเหมือนกัน
            
            c_val = (p_val + k_val) % 26
            # เข้าสูตรลับ: เอาตัวเลขข้อความ + ตัวเลขกุญแจ (ถ้าเกิน 26 ให้วนกลับมาเริ่ม 0 ใหม่)
            
            c_char = chr(c_val + ord('A'))
            # แปลงตัวเลขผลลัพธ์กลับเป็นตัวอักษรภาษาอังกฤษ
            
            ciphertext.append(c_char)
            # เอาตัวอักษรที่ได้ไปใส่ในกล่องผลลัพธ์
            
        return "".join(ciphertext)
        # เอาตัวอักษรทั้งหมดมาต่อกันเป็นข้อความเดียว แล้วส่งกลับ

    def decrypt(self, ciphertext):
        # ฟังก์ชันถอดรหัส: แปลงรหัสลับกลับเป็นข้อความเดิมที่อ่านรู้เรื่อง
        
        ciphertext = preprocess_text(ciphertext)
        # ล้างข้อความรหัสลับให้สะอาด
        
        plaintext = []
        # เตรียมกล่องว่างๆ ไว้ใส่ผลลัพธ์ที่ถอดรหัสแล้ว
        
        key_length = len(self.key)
        # ดูความยาวกุญแจ
        
        for i, char in enumerate(ciphertext):
            # หยิบตัวอักษรรหัสลับมาทีละตัว
            
            c_val = ord(char) - ord('A')
            # แปลงเป็นตัวเลข (0-25)
            
            k_char = self.key[i % key_length]
            # หยิบกุญแจที่ต้องใช้คู่กันมา
            
            k_val = ord(k_char) - ord('A')
            # แปลงกุญแจเป็นตัวเลข
            
            p_val = (c_val - k_val) % 26
            # สูตรถอดรหัส: เอาตัวเลขรหัส - ตัวเลขกุญแจ (ย้อนกลับการบวก)
            
            p_char = chr(p_val + ord('A'))
            # แปลงตัวเลขกลับเป็นตัวอักษร
            
            plaintext.append(p_char)
            # เก็บใส่กล่อง
            
        return "".join(plaintext)
        # รวมร่างเป็นข้อความต้นฉบับแล้วส่งกลับ


class AutokeyCipher:
    # คลาสสำหรับ Autokey Cipher: รุ่นอัปเกรดที่ปลอดภัยกว่า
    
    def __init__(self, key):
        # รับกุญแจดอกแรกมาเก็บไว้เป็นตัวเริ่มสตาร์ท
        self.key = preprocess_text(key)

    def encrypt(self, plaintext):
        # ฟังก์ชันเข้ารหัสแบบ Autokey
        
        plaintext = preprocess_text(plaintext)
        # ล้างข้อความให้สะอาด
        
        full_key = self.key + plaintext
        # เคล็ดลับวิชา Autokey: กุญแจชุดเต็ม คือ กุญแจแรก + ข้อความของเราเองต่อท้ายไปเรื่อยๆ
        # นี่คือสิ่งที่ทำให้มันต่างจาก Vigenere ธรรมดา
        
        ciphertext = []
        # เตรียมกล่องใส่ผลลัพธ์
        
        for i, char in enumerate(plaintext):
            # หยิบข้อความมาทีละตัว
            
            p_val = ord(char) - ord('A')
            # แปลงข้อความเป็นตัวเลข
            
            k_char = full_key[i]
            # หยิบกุญแจจาก full_key ที่เราสร้างไว้ข้างบน
            
            k_val = ord(k_char) - ord('A')
            # แปลงกุญแจเป็นตัวเลข
            
            c_val = (p_val + k_val) % 26
            # สูตรเดิม: (ข้อความ + กุญแจ) % 26
            
            c_char = chr(c_val + ord('A'))
            # แปลงกลับเป็นตัวอักษร
            
            ciphertext.append(c_char)
            # เก็บใส่กล่อง
            
        return "".join(ciphertext)
        # ส่งคืนรหัสลับ

    def decrypt(self, ciphertext):
        # ฟังก์ชันถอดรหัส Autokey (ส่วนนี้จะซับซ้อนหน่อย)
        
        ciphertext = preprocess_text(ciphertext)
        # ล้างข้อความรหัสลับ
        
        plaintext = []
        # กล่องเก็บข้อความต้นฉบับ
        
        current_key = list(self.key)
        # สร้างกุญแจเริ่มต้นในรูปแบบ List (เพราะเราจะต้องเติมของใหม่ต่อท้ายไปเรื่อยๆ)
        
        for i, char in enumerate(ciphertext):
            # หยิบรหัสลับมาทีละตัว
            
            c_val = ord(char) - ord('A')
            # แปลงเป็นตัวเลข
            
            k_char = current_key[i]
            # หยิบกุญแจตัวปัจจุบันมาใช้
            
            k_val = ord(k_char) - ord('A')
            # แปลงกุญแจเป็นตัวเลข
            
            p_val = (c_val - k_val) % 26
            # ถอดรหัส: เอา รหัสลับ - กุญแจ
            
            p_char = chr(p_val + ord('A'))
            # ได้ตัวอักษรต้นฉบับคืนมาแล้ว!
            
            plaintext.append(p_char)
            # เก็บใส่กล่องผลลัพธ์
            
            current_key.append(p_char)
            # **สำคัญมาก**: ตัวอักษรที่เราเพิ่งกู้คืนมาได้ (p_char)
            # จะกลายเป็น "กุญแจ" สำหรับตัวถัดๆ ไปทันที (นี่คือหัวใจของ Autokey)
            
        return "".join(plaintext)
        # ส่งคืนข้อความต้นฉบับที่สมบูรณ์


class SecureDataIntegrity:
    # คลาสใหม่: ระบบรักษาความปลอดภัยข้อมูล (ป้องกันการแก้ไข)
    # ใช้หลักการ HMAC (Hash-based Message Authentication Code)
    
    def __init__(self, secret_key):
        # กุญแจลับสำหรับเซ็นชื่อ (ต้องเก็บไว้เป็นความลับห้ามบอกใคร)
        self.secret_key = secret_key.encode('utf-8')

    def sign_data(self, data):
        # สร้างลายเซ็นดิจิทัล (Signature)
        # เปรียบเหมือนการประทับตราครั่งลงบนจดหมาย ถ้าใครแกะอ่านหรือแก้เนื้อหา ตราจะแตก
        data_bytes = data.encode('utf-8')
        signature = hmac.new(self.secret_key, data_bytes, hashlib.sha256).hexdigest()
        
        # ส่งกลับข้อมูลพร้อมลายเซ็น (คั่นด้วย |)
        return f"{data}|{signature}"

    def verify_data(self, signed_data):
        # ตรวจสอบความถูกต้อง (Verify)
        try:
            # แยกเนื้อหา กับ ลายเซ็น ออกจากกัน
            data, received_signature = signed_data.split('|')
            
            # คำนวณลายเซ็นใหม่จากเนื้อหาที่ได้รับ
            expected_signature = hmac.new(self.secret_key, data.encode('utf-8'), hashlib.sha256).hexdigest()
            
            # เทียบกันว่าตรงไหม (ใช้ compare_digest เพื่อความปลอดภัยสูงสุด กันการจับเวลา)
            if hmac.compare_digest(received_signature, expected_signature):
                return True, data # ผ่าน! ของแท้แน่นอน
            else:
                return False, None # ไม่ผ่าน! มีคนแอบแก้ข้อมูล
        except ValueError:
            return False, None # รูปแบบข้อมูลผิดพลาด


class DataRecoverySystem:
    # คลาสสำหรับระบบกู้คืนข้อมูล (Redundancy System)
    # หลักการ: ส่งข้อมูลไป 2 ชุด (ตัวจริง + ตัวสำรอง)
    # ถ้าตัวจริงพัง จะไปดึงตัวสำรองมาใช้แทน
    
    def __init__(self):
        self.separator = "||__BACKUP__||" 
        # ตัวคั่นระหว่างข้อมูลจริงกับข้อมูลสำรอง

    def create_recovery_packet(self, signed_data):
        # สร้างแพ็กเกจกู้คืน: เอาข้อมูลมาเบิ้ล 2 รอบ คั่นด้วยตัวคั่น
        return f"{signed_data}{self.separator}{signed_data}"

    def extract_and_recover(self, packet, integrity_verifier):
        # ฟังก์ชันกู้ชีพ: เช็คว่าตัวจริงรอดไหม ถ้าไม่รอดไปดูตัวสำรอง
        # integrity_verifier คือฟังก์ชัน verify_data ของ SecureDataIntegrity ที่ส่งเข้ามาช่วยตรวจ
        
        print(f"DEBUG: Attempting to split packet: {packet!r}")
        parts = packet.split(self.separator)
        print(f"DEBUG: Split parts count: {len(parts)}")
        
        if len(parts) != 2:
            return False, None, "Format Error: ไม่พบส่วนข้อมูลสำรอง (คุณอาจจะ Copy มาแค่ข้อความย่อ? กรุณาใช้ปุ่ม Copy เพื่อคัดลอกข้อมูลทั้งหมด)"

        primary_data = parts[0]
        backup_data = parts[1]

        # 1. ตรวจสอบตัวจริงก่อน
        is_valid_main, verified_text_main = integrity_verifier(primary_data)
        if is_valid_main:
            return True, verified_text_main, "Normal: ข้อมูลหลักสมบูรณ์ดี"

        # 2. ถ้าตัวจริงพัง! ให้มาตรวจสอบตัวสำรอง
        is_valid_backup, verified_text_backup = integrity_verifier(backup_data)
        if is_valid_backup:
            return True, verified_text_backup, "Recovered: ข้อมูลหลักเสียหาย แต่กู้ข้อมูลจากส่วนสำรองได้สำเร็จ!"

        # 3. ถ้าพังทั้งคู่
        return False, None, "Critical Failure: ข้อมูลเสียหายทั้งตัวจริงและตัวสำรอง"

def preprocess_text(text):
    # ฟังก์ชันผู้ช่วย: คัดกรองเฉพาะคนหน้าตาดี (A-Z) เข้างาน
    
    clean_text = ""
    # เตรียมพื้นที่ว่าง
    
    for char in text:
        # ตรวจทีละคน (ทีละตัวอักษร)
        
        if char.isalpha():
            # ถ้าเป็นตัวอักษรภาษาอังกฤษ (ABCD...) ให้ผ่าน
            
            clean_text += char.upper()
            # จัดระเบียบให้เป็นตัวพิมพ์ใหญ่ทั้งหมด
            
    return clean_text
    # ส่งคนที่ผ่านการคัดเลือกกลับไปใช้งาน


if __name__ == "__main__":
    # ตรวจสอบว่ากำลังรันไฟล์นี้โดยตรงใช่ไหม
    
    print("--- แบบฝึกหัดถอดรหัสลับ + ระบบความปลอดภัย (Secure Crypto) ---")
    
    # ข้อมูลสมมติสำหรับทดสอบ
    original_text = "ATTACK AT DAWN"
    keyword = "LEMON"
    secret_key = "MY_TOP_SECRET_KEY" # กุญแจสำหรับตรวจสอบความถูกต้อง (HMAC Key)

    print(f"ข้อความเดิม: {original_text}")
    print(f"รหัสผ่านเข้ารหัส: {keyword}")
    print(f"กุญแจกันแก้ไข:   {secret_key}")
    print("-" * 30)

    # 1. เข้ารหัสด้วย Autokey (เหมือนเดิม)
    a_cipher = AutokeyCipher(keyword)
    encrypted_text = a_cipher.encrypt(original_text)
    print(f"[ขั้นตอน 1] เข้ารหัสลับเสร็จแล้ว: {encrypted_text}")

    # 2. เพิ่มความปลอดภัยด้วยการเซ็นชื่อ (HMAC)
    security = SecureDataIntegrity(secret_key)
    signed_encrypted_text = security.sign_data(encrypted_text)
    print(f"[ขั้นตอน 2] ประทับตรากันปลอมแปลง: {signed_encrypted_text}")
    print("-" * 30)

    # 3. จำลองสถานการณ์: ส่งข้อมูลไปปลายทาง (แบบปกติ)
    print(">>> กำลังส่งข้อมูลไปปลายทาง... (ไม่มีใครแอบแก้)")
    is_valid, verified_data = security.verify_data(signed_encrypted_text)
    
    if is_valid:
        decrypted_text = a_cipher.decrypt(verified_data)
        print(f"✅ ตรวจสอบผ่าน! ข้อมูลถูกต้อง")
        print(f"   ถอดรหัสได้ว่า: {decrypted_text}")
    else:
        print(f"❌ อันตราย! ข้อมูลถูกแก้ไข อย่าเชื่อถือ!")

    print("-" * 30)

    # 4. จำลองสถานการณ์: มีแฮกเกอร์แอบแก้ข้อมูล!
    print(">>> มีแฮกเกอร์แอบดักจับข้อมูลแล้วเปลี่ยนข้างใน! <<<")
    
    # แฮกเกอร์แก้รหัสลับตัวนึง (เช่น เปลี่ยนตัวแรก)
    hacked_data_parts = signed_encrypted_text.split('|')
    fake_cipher = "X" + hacked_data_parts[0][1:] # เปลี่ยนตัวแรกเป็น X
    hacked_signed_text = f"{fake_cipher}|{hacked_data_parts[1]}" # ประกอบร่างคืน
    
    print(f"ข้อมูลที่แฮกเกอร์แก้แล้ว: {hacked_signed_text}")
    
    is_valid, verified_data = security.verify_data(hacked_signed_text)
    
    if is_valid:
         # ถ้าเข้ามาในนี้ได้ แปลว่าระบบเราห่วย
        decrypted_text = a_cipher.decrypt(verified_data)
        print(f"✅ ตรวจสอบผ่าน (เป็นไปไม่ได้)")
    else:
        # ระบบต้องมาตกตรงนี้
        print(f"❌ ตรวจพบการปลอมแปลง! (Tampering Detected)")
        print(f"   ระบบปฏิเสธการถอดรหัส เพราะ Signature ไม่ตรงกับเนื้อหา")

    print("-" * 30)

    # 5. ระบบกู้คืนข้อมูล (Data Recovery System)
    print(">>> [NEW] ทดสอบระบบกู้คืนข้อมูล (Data Recovery) <<<")
    recovery = DataRecoverySystem()
    
    # สร้างแพ็กเกจกู้คืน (มี 2 ชุด)
    recovery_packet = recovery.create_recovery_packet(signed_encrypted_text)
    print(f"แพ็กเกจกู้คืน (2 ชุด): {recovery_packet}")
    
    # จำลอง: ข้อมูลชุดแรกโดนแก้ (เหมือนข้อ 4) แต่ชุดสองรอด
    tampered_packet_1 = f"{hacked_signed_text}{recovery.separator}{signed_encrypted_text}"
    print(f"สถานการณ์: ข้อมูลชุดแรกพัง, ชุดสองดี")
    
    # สั่งกู้คืน
    is_rec_valid, rec_data, rec_msg = recovery.extract_and_recover(tampered_packet_1, security.verify_data)
    print(f"ผลการกู้คืน: {rec_msg}")
    
    if is_rec_valid:
        decrypted_rec = a_cipher.decrypt(rec_data)
        print(f"   ถอดรหัสจากข้อมูลกู้คืน: {decrypted_rec}")

    print("-" * 30)
