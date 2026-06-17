from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# Kendi gerçek geliştirici token'ını buraya girmen şart
# https://developer.brawlstars.com/ adresinden aldığın token
API_TOKEN = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImE1YjE3ZTViLWIyZDktNGFjZC05NDQwLTViNDIzZjI2ZjgzOCIsImlhdCI6MTc4MTcxODQzMywic3ViIjoiZGV2ZWxvcGVyLzA3NTEwNTI2LWUyM2MtNDJiMy1mODNjLWQyZWRjYWM0ODBlNiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDYuMTk2LjIwNC4wIl0sInR5cGUiOiJjbGllbnQifV19.WOJTwjFlELPBjD6JlyKOV7gLoEtmeYI3CI_s48lPurB2_OWShHf1wU4UWTwzqomi8G1usR5WNNAa4GmcXXxJqw

@app.get("/api/fetch")
def fetch_data(tag: str):
    # Tag'i temizle
    tag = tag.replace("#", "").upper()
    
    # Resmi API adresi
    url = f"https://api.brawlstars.com/v1/players/%23{tag}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {"html": f"❌ API Hata ({response.status_code}): Token veya etiket geçersiz."}
        
        data = response.json()
        
        return {"html": f"""
        <div class="p-4 bg-gray-900 border border-green-500 rounded text-white">
            <p><b>İsim:</b> {data.get('name')}</p>
            <p><b>Kupa:</b> {data.get('trophies')}</p>
            <p><b>En Yüksek:</b> {data.get('highestTrophies')}</p>
        </div>
        """}
    except Exception as e:
        return {"html": f"🚨 Sistem Hatası: {str(e)}"}
