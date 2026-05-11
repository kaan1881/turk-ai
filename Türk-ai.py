import urllib.parse
import requests
import pyttsx3
import threading
import os
from flask import Flask, render_template_string, request, jsonify

# --- SİSTEM AYARLARI ---
app = Flask(__name__)

def konus(metin):
    def seslendir():
        try:
            # Flask ile çakışmaması için her seferinde yeni init
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.say(metin)
            engine.runAndWait()
        except:
            pass
    threading.Thread(target=seslendir, daemon=True).start()

# --- MODERN WEB TASARIMI (HTML & CSS) ---
WEB_ARAYUZU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TURK AI | MODERN EDITION</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { 
            background: radial-gradient(circle at top right, #1e293b, #0f172a); 
            height: 100vh; display: flex; align-items: center; justify-content: center; color: white;
        }
        .app-box {
            width: 90%; max-width: 900px; height: 80vh;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px; display: flex; flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }
        .header {
            padding: 25px; text-align: center; background: rgba(15, 23, 42, 0.5);
            font-size: 1.5rem; font-weight: bold; color: #38bdf8; letter-spacing: 3px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        #chat-area {
            flex: 1; padding: 30px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px;
        }
        .msg { padding: 15px 20px; border-radius: 20px; max-width: 80%; font-size: 16px; line-height: 1.6; }
        .user { align-self: flex-end; background: #38bdf8; color: #0f172a; font-weight: 500; border-bottom-right-radius: 5px; }
        .bot { align-self: flex-start; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.1); border-bottom-left-radius: 5px; }
        
        .input-box {
            padding: 25px; background: rgba(15, 23, 42, 0.5); display: flex; gap: 15px;
        }
        input {
            flex: 1; background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 15px 25px; border-radius: 15px; color: white; outline: none; font-size: 16px;
        }
        input:focus { border-color: #38bdf8; }
        button {
            background: #38bdf8; color: #0f172a; border: none; padding: 0 30px;
            border-radius: 15px; font-weight: bold; cursor: pointer; transition: 0.3s;
        }
        button:hover { background: #7dd3fc; transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="app-box">
        <div class="header">TURK AI CORE v6.0</div>
        <div id="chat-area"></div>
        <div class="input-box">
            <input type="text" id="user-input" placeholder="Kaan, bir mesaj yaz..." autocomplete="off">
            <button onclick="sendMessage()">GÖNDER</button>
        </div>
    </div>

    <script>
        const chat = document.getElementById('chat-area');
        const input = document.getElementById('user-input');

        async function sendMessage() {
            const text = input.value.trim();
            if(!text) return;

            chat.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg bot">${data.response}</div>`;
                chat.scrollTop = chat.scrollHeight;
            } catch (e) {
                chat.innerHTML += `<div class="msg bot" style="color: #f87171;">Bağlantı sorunu! Lütfen terminali kontrol et.</div>`;
            }
        }
        input.onkeypress = (e) => { if(e.key === 'Enter') sendMessage(); };
    </script>
</body>
</html>
"""

# --- ZEKA MOTORU (HATA ÖNLEYİCİ) ---
def get_ai_response(soru):
    sistem_mesaji = "Sen Turk AI'sın. Kaan tarafından geliştirildin. Samimi ve zeki cevaplar ver."
    temiz_soru = urllib.parse.quote(sistem_mesaji + soru)
    
    # Denenecek 3 farklı model linki
    modeller = [
        f"https://text.pollinations.ai/{temiz_soru}?model=openai",
        f"https://text.pollinations.ai/{temiz_soru}?model=mistral",
        f"https://text.pollinations.ai/{temiz_soru}"
    ]

    for url in modeller:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and r.text:
                return r.text
        except:
            continue
    return "Şu an tüm zeka motorlarım yoğun Kaan. İnternetini kontrol edip tekrar dener misin?"

# --- FLASK YOLLARI ---
@app.route('/')
def home():
    return render_template_string(WEB_ARAYUZU)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    # Yapay zekadan cevap al
    bot_reply = get_ai_response(user_msg)
    
    # Seslendir
    konus(bot_reply)
    
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TURK AI YÜKLENDİ!")
    print("Giriş adresi: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(port=5000, threaded=True)