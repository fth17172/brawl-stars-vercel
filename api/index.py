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
