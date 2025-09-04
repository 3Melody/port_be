from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# โหลดค่า .env
load_dotenv()

app = Flask(__name__)

# ดึงค่าจาก .env
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        name = data.get("name")
        sender_email = data.get("email")
        message_text = data.get("message")

        # สร้าง email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"New contact from {name}"

        body = f"""
        📩 คุณได้รับข้อความใหม่จากฟอร์มติดต่อ:

        👤 ชื่อ: {name}
        📧 อีเมลผู้ส่ง: {sender_email}
        📝 ข้อความ:
        {message_text}
        """
        msg.attach(MIMEText(body, "plain"))

        # ส่ง email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()

        return jsonify({"status": "success", "message": "Email sent!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
