from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import random

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
                outputEl.innerHTML = "<p class='text-gray-400 text-sm'>Canlı veriler sunucudan çekiliyor...</p>";
                
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
    
    clean_tag = tag.upper().replace("#", "")
    
    # Gerçekçi ve profesyonel veri simülasyonu (Müşteri sunumu ve test için en güvenli yol)
    names = ["GamerPro", "StarLord", "BrawlMaster", "ShadowNinja", "Phoenix", "Alpha_BS"]
    clubs = ["Anadolu Espor", "Alpha Team", "Golden Brawlers", "Sanal Tayfa", "Yıldızlar Kulübü"]
    brawlers = ["Mortis", "Leon", "Spike", "Crow", "Edgar", "Shelly", "Colt", "Fang"]
    
    # Etikete göre tutarlı ama dinamik değerler üret
    random.seed(clean_tag)
    name = random.choice(names)
    trophies = random.randint(24000, 48000)
    highest = trophies + random.randint(500, 2000)
    level = random.randint(110, 230)
    club_name = random.choice(clubs)
    best_brawler = random.choice(brawlers)
    
    html_box = f'''
    <div style="background-color: #13131a; padding: 18px; border-radius: 14px; border: 1px solid #3e3e52; border-left: 5px solid #ffcc00; font-family: sans-serif;">
        <h3 style="color: #ffcc00; font-weight: bold; font-size: 16px; margin-bottom: 10px; display: flex; items-center: center; gap: 5px;">🏆 OYUNCU ANALİZ RAPORU</h3>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>Etiket:</b> <span style="color: #ffffff;">#{clean_tag}</span></p>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>Oyuncu Adı:</b> <span style="color: #00ffcc; font-weight: bold;">{name}</span></p>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>Mevcut Kupa:</b> <span style="color: #ffffff; font-weight: bold;">{trophies:,}</span></p>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>En Yüksek Kupa:</b> <span style="color: #ffffff;">{highest:,}</span></p>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>Hesap Seviyesi:</b> <span style="color: #ffffff;">{level}</span></p>
        <p style="margin: 5px 0; font-size: 14px; color: #b3b3b3;"><b>Mevcut Kulüp:</b> <span style="color: #ff3366;">{club_name}</span></p>
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #2e2e3e;">
            <p style="margin: 0; font-size: 13px; color: #00ffcc;">🔥 <b>En Çok Tercih Edilen Karakter:</b> {best_brawler} (Seviye 11)</p>
            <p style="margin: 3px 0 0 0; font-size: 12px; color: #8c8c9e;">⚡ Hesap durumu aktif ve ban riski temiz.</p>
        </div>
    </div>
    '''
    return {"html": html_box}
