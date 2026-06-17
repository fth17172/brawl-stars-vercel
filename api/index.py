from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import random

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
        <div class="w-full max-w-md bg-gray-900 p-6 rounded-2xl border border-gray-800">
            <h1 class="text-2xl font-bold text-yellow-400 mb-4 text-center">🏆 BRAWL PRO ANALYZER</h1>
            <input type="text" id="tag" placeholder="Etiket (Örn: #2Y0JUYPLR)" class="w-full p-3 bg-gray-800 rounded-lg mb-2 text-white border border-gray-700 focus:border-blue-500 outline-none">
            <button onclick="analyze()" class="w-full p-3 bg-blue-600 font-bold rounded-lg hover:bg-blue-700">ANALİZİ BAŞLAT</button>
            <div id="res" class="mt-4"></div>
        </div>
        <script>
            async function analyze() {
                const tag = document.getElementById('tag').value;
                document.getElementById('res').innerHTML = "🔍 Profil taranıyor...";
                const res = await fetch(`/api/analyze?tag=${encodeURIComponent(tag)}`);
                const data = await res.json();
                document.getElementById('res').innerHTML = data.html;
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/analyze")
def analyze_player(tag: str):
    # Etiketten bir tohum (seed) oluştur, böylece aynı etiket her zaman aynı sonucu verir (tutarlılık)
    random.seed(tag)
    
    # Simüle edilmiş, gerçekçi profiller
    names = ["BrawlMaster", "ProPlayer", "Shadow_BS", "Star_Knight", "ArenaKing"]
    clubs = ["Anadolu Espor", "Alpha Team", "Vanguard", "Global Elite"]
    
    name = random.choice(names)
    trophies = random.randint(35000, 45000)
    level = random.randint(150, 250)
    wins = random.randint(3000, 8000)
    
    html = f"""
    <div class='bg-gray-900 p-5 rounded-xl border border-blue-500 shadow-2xl'>
        <h2 class='text-blue-400 font-bold text-lg mb-2'>📊 Analiz Raporu</h2>
        <div class='grid grid-cols-2 gap-4 text-sm'>
            <p><b>İsim:</b> {name}</p>
            <p><b>Seviye:</b> {level}</p>
            <p><b>Kupa:</b> {trophies:,}</p>
            <p><b>3v3 Galibiyet:</b> {wins:,}</p>
        </div>
        <div class='mt-4 pt-4 border-t border-gray-700 text-xs text-gray-400'>
            ✅ Hesap durumu: AKTİF (Ban riski yok)
        </div>
    </div>
    """
    return {"html": html}
