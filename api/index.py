from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# BrawlAPI'nin base endpoint'i
BASE_URL = "https://api.brawlapi.com/v1"

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
    <body class="bg-gray-900 text-white flex justify-center p-4">
        <div class="w-full max-w-md bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-700">
            <h1 class="text-2xl font-bold text-yellow-500 mb-4 text-center">🏆 BS ANALYZER</h1>
            <input type="text" id="tag" placeholder="Örn: 2Y0JUYPLR" class="w-full p-3 bg-gray-900 rounded-lg mb-2 border border-gray-600">
            <button onclick="getData()" class="w-full p-3 bg-teal-500 font-bold rounded-lg hover:bg-teal-600 transition">SORGULA</button>
            <div id="res" class="mt-4"></div>
        </div>
        <script>
            async function getData() {
                const rawTag = document.getElementById('tag').value;
                const tag = rawTag.replace('#', '').trim();
                document.getElementById('res').innerHTML = "Veri işleniyor...";
                
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
    # API'ye giden tam URL'yi görmek için burayı takip et
    url = f"https://api.brawlapi.com/v1/player/{tag}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Hata detayını bize döndürsün
        if response.status_code != 200:
            return {"html": f"❌ API Hatası ({response.status_code}): {response.text}"}
        
        data = response.json()
        # ... geri kalanı aynı
        
        # Verileri güvenli çek
        name = data.get("name", "Bilinmiyor")
        trophies = data.get("trophies", 0)
        club = data.get("club", {}).get("name", "Kulübü Yok")
        
        return {"html": f"""
        <div class="bg-gray-900 p-4 rounded-lg border border-teal-500">
            <p class="text-teal-400 font-bold">{name}</p>
            <p>🏆 Kupa: {trophies}</p>
            <p>🏠 Kulüp: {club}</p>
        </div>
        """}
    except Exception as e:
        return {"html": "<p class='text-red-500'>🚨 Bağlantı sorunu yaşandı.</p>"}from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# BrawlAPI'nin ücretsiz, IP kısıtlaması olmayan public proxy servisini kullanıyoruz.
# Bu servis, Supercell'in kısıtlamalarını bizim için aşar.
BRAWL_API_URL = "https://api.brawlapi.com/v1/player"

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
    <body class="bg-gray-900 text-white flex justify-center p-4">
        <div class="w-full max-w-md bg-gray-800 p-6 rounded-xl shadow-lg">
            <h1 class="text-2xl font-bold text-yellow-500 mb-4 text-center">🏆 BRAWL PRO ANALYZER</h1>
            <input type="text" id="tag" placeholder="Etiket: 2Y0JUYPLR" class="w-full p-3 bg-gray-700 rounded-lg mb-2">
            <button onclick="getData()" class="w-full p-3 bg-teal-500 font-bold rounded-lg">ANALİZ ET</button>
            <div id="res" class="mt-4"></div>
        </div>
        <script>
            async function getData() {
                const tag = document.getElementById('tag').value.replace('#', '');
                document.getElementById('res').innerHTML = "Veri çekiliyor...";
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
    try:
        # BrawlAPI üzerinden gerçek veriyi çek
        response = requests.get(f"{BRAWL_API_URL}/{tag}")
        if response.status_code != 200:
            return {"html": "⚠️ Oyuncu bulunamadı!"}
        
        data = response.json()
        
        # Senin istediğin detaylı veri seti
        name = data.get("name")
        trophies = data.get("trophies")
        club = data.get("club", {}).get("name", "Yok")
        exp = data.get("expLevel")
        wins3v3 = data.get("3vs3Victories")
        solo = data.get("soloVictories")
        
        html = f"""
        <div class="space-y-2 text-sm">
            <p><b>İsim:</b> {name}</p>
            <p><b>Kupa:</b> {trophies}</p>
            <p><b>Kulüp:</b> {club}</p>
            <p><b>Seviye:</b> {exp}</p>
            <p><b>3v3 Galibiyet:</b> {wins3v3}</p>
            <p><b>Solo Galibiyet:</b> {solo}</p>
        </div>
        """
        return {"html": html}
    except Exception as e:
        return {"html": "🚨 Hata oluştu."}
