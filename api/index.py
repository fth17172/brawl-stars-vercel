import gradio as gr
import requests

BS_KEYS = ["BS-FTH-17", "BS-XM4-99", "BS-W7R-12", "BS-K9A-34"]
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImE1YjE3ZTViLWIyZDktNGFjZC05NDQwLTViNDIzZjI2ZjgzOCIsImlhdCI6MTg4MTcxODQzMywic3ViIjoiZGV2ZWxvcGVyLzA3NTEwNTI2LWUyM2MtNDJiMy1mODNjLWQyZWRjYWM0ODBlNiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDYuMTk2LjIwNC4wIl0sInR5cGUiOiJjbGllbnQifV19.WOJTwjFlELPBjD6JlyKOV7gLoEtmeYI3CI_s48lPurB2_OWShHf1wU4UWTwzqomi8G1usR5WNNAa4GmcXXxJqw"

def check_bs_license(key):
    if key in BS_KEYS:
        return gr.update(visible=False), gr.update(visible=True), ""
    return gr.update(visible=True), gr.update(visible=False), "❌ Hatalı veya Geçersiz Lisans Kodu!"

def fetch_bs_stats(player_tag):
    if not player_tag:
        return "⚠️ Lütfen bir Oyuncu Etiketi (Tag) girin!"
    
    tag = player_tag.upper().replace("#", "%23")
    if not tag.startswith("%23"):
        tag = "%23" + tag

    url = f"https://api.brawlstars.com/v1/players/{tag}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            name = data.get("name", "Bilinmeyen Oyuncu")
            trophies = data.get("trophies", 0)
            highest_trophies = data.get("highestTrophies", 0)
            exp_level = data.get("expLevel", 0)
            club_name = data.get("club", {}).get("name", "Kulübü Yok")
            
            return f'''
            <div style="background-color: #1e1e2e; padding: 15px; border-radius: 10px; color: white; font-family: sans-serif; margin-top: 10px; border-left: 5px solid #ffcc00;">
                <h3 style="color: #ffcc00; margin: 0 0 10px 0;">🏆 Canlı Veriler</h3>
                <p style="margin: 5px 0; font-size: 16px;"><b>Oyuncu Adı:</b> <span style="color: #00ffcc;">{name}</span></p>
                <p style="margin: 5px 0;"><b>Kupa:</b> {trophies:,}</p>
                <p style="margin: 5px 0;"><b>En Yüksek Kupa:</b> {highest_trophies:,}</p>
                <p style="margin: 5px 0;"><b>Seviye:</b> {exp_level}</p>
                <p style="margin: 5px 0;"><b>Kulüp:</b> {club_name}</p>
            </div>
            '''
        return f"⚠️ Oyuncu bulunamadı veya API hatası. Kod: {response.status_code}"
    except Exception as e:
        return f"🚨 Bağlantı Hatası: {str(e)}"

# Gradio 6.0 log uyarısını engellemek için theme parametresini launch'a bırakıp sadeleştiriyoruz
with gr.Blocks() as demo:
    gr.Markdown("# 🏆 BRAWL STARS PRO ANALYZER")
    with gr.Column(visible=True) as login_box:
        key_input = gr.Textbox(label="Lisans Kodu", type="password")
        login_btn = gr.Button("Giriş Yap")
        error_output = gr.Markdown()
    with gr.Column(visible=False) as main_content:
        player_tag = gr.Textbox(label="Oyuncu Etiketi")
        search_btn = gr.Button("Sorgula")
        stats_output = gr.HTML()

    login_btn.click(check_bs_license, inputs=[key_input], outputs=[login_box, main_content, error_output])
    search_btn.click(fetch_bs_stats, inputs=[player_tag], outputs=[stats_output])

# Uygulama iskeletini oluştur
app = demo.queue().app

# 🔥 VERCEL STARTUP YAMASI (Zorla Config Enjeksiyonu)
# Vercel'in çalıştırmadığı konfigürasyon motorunu burada el ile tetikliyoruz.
try:
    app.blocks.config = demo.get_config_with_actions()
except Exception:
    try:
        app.blocks.config = demo.config
    except Exception:
        pass
