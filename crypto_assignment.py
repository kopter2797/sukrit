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


# พื้นที่ทดสอบการทำงาน (Main Playground)
if __name__ == "__main__":
    # ตรวจสอบว่ากำลังรันไฟล์นี้โดยตรงใช่ไหม
    
    print("--- แบบฝึกหัดถอดรหัสลับ (Cryptography Assignment) ---")
    
    # ข้อมูลสมมติสำหรับทดสอบ
    original_text = "ATTACK AT DAWN"
    # ข้อความลับ: "บุกตอนรุ่งสาง"
    
    keyword = "LEMON"
    # รหัสผ่าน: "LEMON"
    
    print(f"ข้อความเดิม: {original_text}")
    print(f"รหัสผ่าน:    {keyword}")
    print("-" * 30)

    # 1. ลองเล่น Vigenere
    v_cipher = VigenereCipher(keyword)
    v_encrypted = v_cipher.encrypt(original_text)
    v_decrypted = v_cipher.decrypt(v_encrypted)
    
    print("ผลลัพธ์ Vigenere Cipher:")
    print(f"เข้ารหัสแล้ว: {v_encrypted}")
    print(f"ถอดรหัสกลับ: {v_decrypted}")
    print("-" * 30)

    # 2. ลองเล่น Autokey
    a_cipher = AutokeyCipher(keyword)
    a_encrypted = a_cipher.encrypt(original_text)
    a_decrypted = a_cipher.decrypt(a_encrypted)
    
    print("ผลลัพธ์ Autokey Cipher (ปลอดภัยกว่า):")
    print(f"เข้ารหัสแล้ว: {a_encrypted}")
    print(f"ถอดรหัสกลับ: {a_decrypted}")
    print("-" * 30)

    # เรื่องน่ารู้: ทำไม Autokey ถึงเก่งกว่า?
    print("\nทำไม Autokey ถึงเจ๋งกว่า Vigenere?")
    
    explanation = """
    1. Vigenere ใช้กุญแจเดิมวนซ้ำไปเรื่อยๆ (เช่น LEMONLEMON...)
       ถ้าโจรจับทางได้ว่ากุญแจยาว 5 ตัวอักษร ก็เสร็จโจรเลย! (เข้าทาง Kasiski method)
    
    2. Autokey ฉลาดกว่า เพราะใช้กุญแจแค่รอบแรก
       รอบต่อไปมันเอา "ข้อความของเราเอง" มาทำเป็นกุญแจ
       ทำให้กุญแจเปลี่ยนรหัสไปเรื่อยๆ ไม่มีรูปแบบซ้ำๆ ให้โจรจับทางได้ง่ายๆ ครับ
    """
    
    print(explanation)
