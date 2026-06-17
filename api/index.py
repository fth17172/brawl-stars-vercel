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
    <body class="bg-black text-white flex justify-center p-4">
        <div class="w-full max-w-md bg-gray-900 p-6 rounded-2xl border border-gray-800">
            <h1 class="text-2xl font-bold text-yellow-400 mb-4 text-center">🏆 BRAWL ANALYZER</h1>
            <input type="text" id="tag" placeholder="Etiket (Örn: 9UUUYQY8R)" class="w-full p-3 bg-gray-800 rounded-lg mb-2 text-white border border-gray-700">
            <button onclick="getData()" class="w-full p-3 bg-blue-600 font-bold rounded-lg hover:bg-blue-700">ANALİZİ BAŞLAT</button>
            <div id="res" class="mt-4"></div>
        </div>
        <script>
            async function getData() {
                const tag = document.getElementById('tag').value.replace('#', '').trim();
                document.getElementById('res').innerHTML = "Sunuculardan veri alınıyor...";
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
    # İki farklı API servisi deneyeceğiz (Yedekli mimari)
    endpoints = [
        f"https://api.brawlapi.com/v1/player/{tag}",
        f"https://brawlstars-api.vercel.app/api/player/{tag}" # Alternatif proxy
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                name = data.get("name", "Bilinmiyor")
                trophies = data.get("trophies", 0)
                club = data.get("club", {}).get("name", "Kulüp Yok")
                return {"html": f"<div class='bg-green-900/20 p-4 rounded border border-green-500'>👤 <b>{name}</b><br>🏆 Kupa: {trophies}<br>🏠 Kulüp: {club}</div>"}
        except:
            continue
            
    return {"html": "<div class='bg-red-900/20 p-4 rounded border border-red-500'>❌ Oyuncu verisine ulaşılamadı. Etiketi kontrol edin.</div>"}
