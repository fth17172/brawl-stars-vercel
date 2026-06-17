from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BS_KEYS = ["BS-FTH-17", "BS-XM4-99", "BS-W7R-12", "BS-K9A-34"]

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏆 BRAWL STARS PRO ANALYZER</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background-color: #13131a; color: #ffffff; }
        </style>
    </head>
    <body class="flex flex-col items-center justify-center min-h-screen p-4">
        <div class="w-full max-w-md bg-[#1e1e2e] p-6 rounded-2xl shadow-2xl border border-[#2e2e3e]">
            <h1 class="text-2xl font-bold text-center text-[#ffcc00] mb-6">🏆 BS PRO ANALYZER</h1>
            
            <div id="login-box" class="space-y-4">
                <p class="text-sm text-gray-400 text-center">Sisteme erişmek için 100 TL karşılığında aldığınız lisans kodunu girin.</p>
                <input type="password" id="license-key" placeholder="BS-XXXX-XX" class="w-full p-3 bg-[#13131a] border border-[#3e3e52] rounded-xl text-center text-white focus:outline-none focus:border-[#ffcc00]">
                <button onclick="verifyKey()" class="w-full p-3 bg-[#ffcc00] text-black font-bold rounded-xl hover:bg-[#e6b800] transition">Sisteme Giriş Yap</button>
                <p id="login-error" class="text-red-500 text-sm text-center hidden"></p>
            </div>

            <div id="main-content" class="space-y-4 hidden">
                <div class="flex flex-col space-y-2">
                    <label class="text-sm text-gray-400">Brawl Stars Oyuncu Etiketi</label>
                    <input type="text" id="player-tag" placeholder="Örn: 9UUUYQY8R" class="w-full p-3 bg-[#13131a] border border-[#3e3e52] rounded-xl text-white focus:outline-none focus:border-[#00ffcc]">
                </div>
                <button onclick="fetchStats()" class="w-full p-3 bg-[#00ffcc] text-black font-bold rounded-xl hover:bg-[#00e6b8] transition">Sorgula</button>
                <div id="stats-output" class="mt-4"></div>
            </div>
        </div>

        <script>
            let savedKey = "";
            const validKeys = ["BS-FTH-17", "BS-XM4-99", "BS-W7R-12", "BS-K9A-34"];

            function verifyKey() {
                const key = document.getElementById("license-key").value.trim();
                const errorEl = document.getElementById("login-error");
                
                if (validKeys.includes(key)) {
                    savedKey = key;
                    document.getElementById("login-box").classList.add("hidden");
                    document.getElementById("main-content").classList.remove("hidden");
                } else {
                    errorEl.innerText = "❌ Hatalı veya Geçersiz Lisans Kodu!";
                    errorEl.classList.remove("hidden");
                }
            }

            async function fetchStats() {
                const tag = document.getElementById("player-tag").value.trim();
                const outputEl = document.getElementById("stats-output");
                if (!tag) {
                    outputEl.innerHTML = "<p class='text-yellow-500 text-sm'>⚠️ Oyuncu etiketi girin!</p>";
                    return;
                }
                outputEl.innerHTML = "<p class='text-gray-400 text-sm'>Canlı veriler çekiliyor...</p>";
                
                try {
                    const res = await fetch(`/api/stats?tag=${encodeURIComponent(tag)}&key=${savedKey}`);
                    const data = await res.json();
                    if (res.status === 200) {
                        outputEl.innerHTML = data.html;
                    } else {
                        outputEl.innerHTML = `<p class='text-red-500 text-sm'>⚠️ ${data.detail || 'Hata oluştu'}</p>`;
                    }
                } catch (err) {
                    outputEl.innerHTML = "<p class='text-red-500 text-sm'>🚨 Sunucu bağlantı hatası!</p>";
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/stats")
def get_stats(tag: str, key: str):
    if key not in BS_KEYS:
        raise HTTPException(status_code=401, detail="Yetkisiz Erişim!")
    
    # Etiketteki # işaretini temizle, bu API saf etiket ister
    clean_tag = tag.upper().replace("#", "")

    # IP engeline takılmayan herkese açık proxy API mimarisi
    url = f"https://api.brawlapi.com/v1/player?tag={clean_tag}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            name = data.get("name", "Bilinmeyen Oyuncu")
            trophies = data.get("trophies", 0)
            highest_trophies = data.get("highestTrophies", 0)
            exp_level = data.get("expLevel", 0)
            
            # Kulüp bilgisi kontrolü
            club = data.get("club", {})
            club_name = club.get("name", "Kulübü Yok") if club else "Kulübü Yok"
            
            html_box = f'''
            <div style="background-color: #13131a; padding: 15px; border-radius: 12px; border-left: 5px solid #ffcc00;">
                <h3 style="color: #ffcc00; font-weight: bold; margin-bottom: 8px;">🏆 Canlı Veriler</h3>
                <p style="margin: 4px 0;"><b>Oyuncu Adı:</b> <span style="color: #00ffcc;">{name}</span></p>
                <p style="margin: 4px 0;"><b>Kupa:</b> {trophies:,}</p>
                <p style="margin: 4px 0;"><b>En Yüksek Kupa:</b> {highest_trophies:,}</p>
                <p style="margin: 4px 0;"><b>Seviye:</b> {exp_level}</p>
                <p style="margin: 4px 0;"><b>Kulüp:</b> {club_name}</p>
            </div>
            '''
            return {"html": html_box}
        
        return {"html": f"<p class='text-yellow-500 text-sm'>⚠️ Oyuncu bulunamadı. Etiketi doğru girdiğinizden emin olun.</p>"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
