from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-950 text-white flex justify-center p-4">
        <div class="w-full max-w-md bg-gray-900 p-6 rounded-xl shadow-2xl border border-gray-800">
            <h1 class="text-xl font-bold text-yellow-400 mb-4 text-center">🏆 ANALİZ SİSTEMİ</h1>
            <input type="text" id="tag" placeholder="Örn: 2Y0JUYPLR" class="w-full p-3 bg-gray-800 rounded-lg mb-2 text-white placeholder-gray-500">
            <button onclick="getData()" class="w-full p-3 bg-teal-600 font-bold rounded-lg hover:bg-teal-700">SORGULA</button>
            <div id="res" class="mt-4 text-sm text-gray-300"></div>
        </div>
        <script>
            async function getData() {
                const rawTag = document.getElementById('tag').value.trim();
                const tag = rawTag.replace('#', '').toUpperCase();
                document.getElementById('res').innerHTML = "Bağlanıyor...";
                
                const res = await fetch(`/api/fetch?tag=${tag}`);
                const data = await res.json();
                document.getElementById('res').innerHTML = data.html;
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/fetch")
def fetch_data(tag: str):
    # Etiketi temizle: O harfini 0'a çevir, boşlukları sil
    clean_tag = tag.upper().replace("O", "0").replace("#", "").strip()
    
    url = f"https://api.brawlapi.com/v1/player/{clean_tag}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return {"html": f"<div class='text-red-400'>❌ Oyuncu bulunamadı! (Aranan: {clean_tag})</div>"}
        
        # ... geri kalanı aynı
        
        # Başarılı veri çekimi
        name = data.get("name", "Bilinmiyor")
        trophies = data.get("trophies", 0)
        club = data.get("club", {}).get("name", "Yok") if data.get("club") else "Kulübü Yok"
        
        return {"html": f"""
        <div class="space-y-2 p-4 bg-gray-800 rounded border-l-4 border-teal-500">
            <p><b>👤 İsim:</b> {name}</p>
            <p><b>🏆 Kupa:</b> {trophies}</p>
            <p><b>🏠 Kulüp:</b> {club}</p>
        </div>
        """}
    except Exception as e:
        return {"html": f"<div class='p-3 bg-orange-900/30 border border-orange-500 rounded'>🚨 Sistem Hatası: {str(e)}</div>"}
