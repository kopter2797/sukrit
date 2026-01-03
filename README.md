# Crypto Master (โปรเจกต์เข้ารหัสลับแบบสมมาตร)

เว็บแอปพลิเคชันสำหรับศึกษาและสาธิตการทำงานของ **Symmetric Encryption (การเข้ารหัสแบบสมมาตร)** โดยเน้นไปที่อัลกอริทึมคลาสสิก 2 ตัว คือ **Vigenere Cipher** และ **Autokey Cipher**


## ฟีเจอร์หลัก (Features)

- **Vigenere Cipher**: เข้ารหัส/ถอดรหัส แบบดั้งเดิม
- **Autokey Cipher**: เข้ารหัส/ถอดรหัส แบบ **ปลอดภัยกว่า** (ไม่มีการวนซ้ำของกุญแจ)
- **Modern UI**: ดีไซน์สวยล้ำสมัย สไตล์กระจก (Glassmorphism) พร้อม Animation
- **Educational Mode**: มีหน้า `/info` อธิบายหลักการทำงานเปรียบเทียบกันด้วยภาษาง่ายๆ
- **Code Comments**: โค้ดใน `crypto_assignment.py` มีคำอธิบายภาษาไทยประกอบทุกบรรทัด เพื่อความเข้าใจง่าย

## วิธีการติดตั้งและรันโปรแกรม (Installation)

1. **Clone repository นี้ลงเครื่อง**

   ```bash
   git clone https://github.com/kopter2797/sukrit.git
   cd sukrit
   ```

2. **ติดตั้งไลบรารีที่จำเป็น (Flask)**

   ```bash
   pip install flask
   ```

3. **รันโปรแกรม**

   ```bash
   python app.py
   ```

4. **เปิดใช้งาน**
   - เปิด Browser แล้วเข้าไปที่: `http://127.0.0.1:5000`

## โครงสร้างไฟล์ (File Structure)

- `app.py`: ตัวเซิร์ฟเวอร์หลัก (Flask Backend) ทำหน้าที่รับค่าจากหน้าเว็บมาประมวลผล
- `crypto_assignment.py`: หัวใจหลักของระบบ เก็บ Class `VigenereCipher` และ `AutokeyCipher` พร้อมคำอธิบายโค้ดอย่างละเอียด
- `templates/index.html`: หน้าจอหลักสำหรับใช้งานโปรแกรม
- `templates/info.html`: หน้าจออธิบายความรู้เปรียบเทียบ 2 วิธี
- `static/style.css`: ไฟล์ตกแต่งหน้าตาเว็บไซต์ (CSS)

## ตัวอย่างการใช้งาน (Example)

- **Input**: `ATTACK AT DAWN`
- **Keyword**: `LEMON`
- **Method**: Autokey
- **Action**: Encrypt
- **Result**: `LXFOPVEFRNHR`

---
