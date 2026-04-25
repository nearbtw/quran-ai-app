import os, json, urllib.request
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="Quran AI Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SURAHS = [
  {"id":1,"name":"Al-Fatiha","ar":"الفاتحة","count":7,"type":"Makkah"},
  {"id":2,"name":"Al-Baqarah","ar":"البقرة","count":286,"type":"Madinah"},
  {"id":3,"name":"Ali 'Imran","ar":"آل عمران","count":200,"type":"Madinah"},
  {"id":4,"name":"An-Nisa","ar":"النساء","count":176,"type":"Madinah"},
  {"id":5,"name":"Al-Ma'idah","ar":"المائدة","count":120,"type":"Madinah"},
  {"id":6,"name":"Al-An'am","ar":"الأنعام","count":165,"type":"Makkah"},
  {"id":7,"name":"Al-A'raf","ar":"الأعراف","count":206,"type":"Makkah"},
  {"id":8,"name":"Al-Anfal","ar":"الأنفال","count":75,"type":"Madinah"},
  {"id":9,"name":"At-Tawbah","ar":"التوبة","count":129,"type":"Madinah"},
  {"id":10,"name":"Yunus","ar":"يونس","count":109,"type":"Makkah"},
  {"id":11,"name":"Hud","ar":"هود","count":123,"type":"Makkah"},
  {"id":12,"name":"Yusuf","ar":"يوسف","count":111,"type":"Makkah"},
  {"id":13,"name":"Ar-Ra'd","ar":"الرعد","count":43,"type":"Madinah"},
  {"id":14,"name":"Ibrahim","ar":"إبراهيم","count":52,"type":"Makkah"},
  {"id":15,"name":"Al-Hijr","ar":"الحجر","count":99,"type":"Makkah"},
  {"id":16,"name":"An-Nahl","ar":"النحل","count":128,"type":"Makkah"},
  {"id":17,"name":"Al-Isra","ar":"الإسراء","count":111,"type":"Makkah"},
  {"id":18,"name":"Al-Kahf","ar":"الكهف","count":110,"type":"Makkah"},
  {"id":19,"name":"Maryam","ar":"مريم","count":98,"type":"Makkah"},
  {"id":20,"name":"Taha","ar":"طه","count":135,"type":"Makkah"},
  {"id":21,"name":"Al-Anbya","ar":"الأنبياء","count":112,"type":"Makkah"},
  {"id":22,"name":"Al-Hajj","ar":"الحج","count":78,"type":"Madinah"},
  {"id":23,"name":"Al-Mu'minun","ar":"المؤمنون","count":118,"type":"Makkah"},
  {"id":24,"name":"An-Nur","ar":"النور","count":64,"type":"Madinah"},
  {"id":25,"name":"Al-Furqan","ar":"الفرقان","count":77,"type":"Makkah"},
  {"id":26,"name":"Ash-Shu'ara","ar":"الشعراء","count":227,"type":"Makkah"},
  {"id":27,"name":"An-Naml","ar":"النمل","count":93,"type":"Makkah"},
  {"id":28,"name":"Al-Qasas","ar":"القصص","count":88,"type":"Makkah"},
  {"id":29,"name":"Al-'Ankabut","ar":"العنكبوت","count":69,"type":"Makkah"},
  {"id":30,"name":"Ar-Rum","ar":"الروم","count":60,"type":"Makkah"},
  {"id":31,"name":"Luqman","ar":"لقمان","count":34,"type":"Makkah"},
  {"id":32,"name":"As-Sajdah","ar":"السجدة","count":30,"type":"Makkah"},
  {"id":33,"name":"Al-Ahzab","ar":"الأحزاب","count":73,"type":"Madinah"},
  {"id":34,"name":"Saba","ar":"سبأ","count":54,"type":"Makkah"},
  {"id":35,"name":"Fatir","ar":"فاطر","count":45,"type":"Makkah"},
  {"id":36,"name":"Ya-Sin","ar":"يس","count":83,"type":"Makkah"},
  {"id":37,"name":"As-Saffat","ar":"الصافات","count":182,"type":"Makkah"},
  {"id":38,"name":"Sad","ar":"ص","count":88,"type":"Makkah"},
  {"id":39,"name":"Az-Zumar","ar":"الزمر","count":75,"type":"Makkah"},
  {"id":40,"name":"Ghafir","ar":"غافر","count":85,"type":"Makkah"},
  {"id":41,"name":"Fussilat","ar":"فصلت","count":54,"type":"Makkah"},
  {"id":42,"name":"Ash-Shuraa","ar":"الشورى","count":53,"type":"Makkah"},
  {"id":43,"name":"Az-Zukhruf","ar":"الزخرف","count":89,"type":"Makkah"},
  {"id":44,"name":"Ad-Dukhan","ar":"الدخان","count":59,"type":"Makkah"},
  {"id":45,"name":"Al-Jathiyah","ar":"الجاثية","count":37,"type":"Makkah"},
  {"id":46,"name":"Al-Ahqaf","ar":"الأحقاف","count":35,"type":"Makkah"},
  {"id":47,"name":"Muhammad","ar":"محمد","count":38,"type":"Madinah"},
  {"id":48,"name":"Al-Fath","ar":"الفتح","count":29,"type":"Madinah"},
  {"id":49,"name":"Al-Hujurat","ar":"الحجرات","count":18,"type":"Madinah"},
  {"id":50,"name":"Qaf","ar":"ق","count":45,"type":"Makkah"},
  {"id":51,"name":"Adh-Dhariyat","ar":"الذاريات","count":60,"type":"Makkah"},
  {"id":52,"name":"At-Tur","ar":"الطور","count":49,"type":"Makkah"},
  {"id":53,"name":"An-Najm","ar":"النجم","count":62,"type":"Makkah"},
  {"id":54,"name":"Al-Qamar","ar":"القمر","count":55,"type":"Makkah"},
  {"id":55,"name":"Ar-Rahman","ar":"الرحمن","count":78,"type":"Madinah"},
  {"id":56,"name":"Al-Waqi'ah","ar":"الواقعة","count":96,"type":"Makkah"},
  {"id":57,"name":"Al-Hadid","ar":"الحديد","count":29,"type":"Madinah"},
  {"id":58,"name":"Al-Mujadila","ar":"المجادلة","count":22,"type":"Madinah"},
  {"id":59,"name":"Al-Hashr","ar":"الحشر","count":24,"type":"Madinah"},
  {"id":60,"name":"Al-Mumtahanah","ar":"الممتحنة","count":13,"type":"Madinah"},
  {"id":61,"name":"As-Saff","ar":"الصف","count":14,"type":"Madinah"},
  {"id":62,"name":"Al-Jumu'ah","ar":"الجمعة","count":11,"type":"Madinah"},
  {"id":63,"name":"Al-Munafiqun","ar":"المنافقون","count":11,"type":"Madinah"},
  {"id":64,"name":"At-Taghabun","ar":"التغابن","count":18,"type":"Madinah"},
  {"id":65,"name":"At-Talaq","ar":"الطلاق","count":12,"type":"Madinah"},
  {"id":66,"name":"At-Tahrim","ar":"التحريم","count":12,"type":"Madinah"},
  {"id":67,"name":"Al-Mulk","ar":"الملك","count":30,"type":"Makkah"},
  {"id":68,"name":"Al-Qalam","ar":"القلم","count":52,"type":"Makkah"},
  {"id":69,"name":"Al-Haqqah","ar":"الحاقة","count":52,"type":"Makkah"},
  {"id":70,"name":"Al-Ma'arij","ar":"المعارج","count":44,"type":"Makkah"},
  {"id":71,"name":"Nuh","ar":"نوح","count":28,"type":"Makkah"},
  {"id":72,"name":"Al-Jinn","ar":"الجن","count":28,"type":"Makkah"},
  {"id":73,"name":"Al-Muzzammil","ar":"المزمل","count":20,"type":"Makkah"},
  {"id":74,"name":"Al-Muddaththir","ar":"المدثر","count":56,"type":"Makkah"},
  {"id":75,"name":"Al-Qiyamah","ar":"القيامة","count":40,"type":"Makkah"},
  {"id":76,"name":"Al-Insan","ar":"الإنسان","count":31,"type":"Madinah"},
  {"id":77,"name":"Al-Mursalat","ar":"المرسلات","count":50,"type":"Makkah"},
  {"id":78,"name":"An-Naba","ar":"النبأ","count":40,"type":"Makkah"},
  {"id":79,"name":"An-Nazi'at","ar":"النازعات","count":46,"type":"Makkah"},
  {"id":80,"name":"'Abasa","ar":"عبس","count":42,"type":"Makkah"},
  {"id":81,"name":"At-Takwir","ar":"التكوير","count":29,"type":"Makkah"},
  {"id":82,"name":"Al-Infitar","ar":"الانفطار","count":19,"type":"Makkah"},
  {"id":83,"name":"Al-Mutaffifin","ar":"المطففين","count":36,"type":"Makkah"},
  {"id":84,"name":"Al-Inshiqaq","ar":"الانشقاق","count":25,"type":"Makkah"},
  {"id":85,"name":"Al-Buruj","ar":"البروج","count":22,"type":"Makkah"},
  {"id":86,"name":"At-Tariq","ar":"الطارق","count":17,"type":"Makkah"},
  {"id":87,"name":"Al-A'la","ar":"الأعلى","count":19,"type":"Makkah"},
  {"id":88,"name":"Al-Ghashiyah","ar":"الغاشية","count":26,"type":"Makkah"},
  {"id":89,"name":"Al-Fajr","ar":"الفجر","count":30,"type":"Makkah"},
  {"id":90,"name":"Al-Balad","ar":"البلد","count":20,"type":"Makkah"},
  {"id":91,"name":"Ash-Shams","ar":"الشمس","count":15,"type":"Makkah"},
  {"id":92,"name":"Al-Layl","ar":"الليل","count":21,"type":"Makkah"},
  {"id":93,"name":"Ad-Duhaa","ar":"الضحى","count":11,"type":"Makkah"},
  {"id":94,"name":"Ash-Sharh","ar":"الشرح","count":8,"type":"Makkah"},
  {"id":95,"name":"At-Tin","ar":"التين","count":8,"type":"Makkah"},
  {"id":96,"name":"Al-'Alaq","ar":"العلق","count":19,"type":"Makkah"},
  {"id":97,"name":"Al-Qadr","ar":"القدر","count":5,"type":"Makkah"},
  {"id":98,"name":"Al-Bayyinah","ar":"البينة","count":8,"type":"Madinah"},
  {"id":99,"name":"Az-Zalzalah","ar":"الزلزلة","count":8,"type":"Madinah"},
  {"id":100,"name":"Al-'Adiyat","ar":"العاديات","count":11,"type":"Makkah"},
  {"id":101,"name":"Al-Qari'ah","ar":"القارعة","count":11,"type":"Makkah"},
  {"id":102,"name":"At-Takathur","ar":"التكاثر","count":8,"type":"Makkah"},
  {"id":103,"name":"Al-'Asr","ar":"العصر","count":3,"type":"Makkah"},
  {"id":104,"name":"Al-Humazah","ar":"الهمزة","count":9,"type":"Makkah"},
  {"id":105,"name":"Al-Fil","ar":"الفيل","count":5,"type":"Makkah"},
  {"id":106,"name":"Quraysh","ar":"قريش","count":4,"type":"Makkah"},
  {"id":107,"name":"Al-Ma'un","ar":"الماعون","count":7,"type":"Makkah"},
  {"id":108,"name":"Al-Kawthar","ar":"الكوثر","count":3,"type":"Makkah"},
  {"id":109,"name":"Al-Kafirun","ar":"الكافرون","count":6,"type":"Makkah"},
  {"id":110,"name":"An-Nasr","ar":"النصر","count":3,"type":"Madinah"},
  {"id":111,"name":"Al-Masad","ar":"المسد","count":5,"type":"Makkah"},
  {"id":112,"name":"Al-Ikhlas","ar":"الإخلاص","count":4,"type":"Makkah"},
  {"id":113,"name":"Al-Falaq","ar":"الفلق","count":5,"type":"Makkah"},
  {"id":114,"name":"An-Nas","ar":"الناس","count":6,"type":"Makkah"}
]

VERSES_DATA = {}

def load_verses_data():
    global VERSES_DATA
    if os.path.exists("verses.json"):
        with open("verses.json", "r", encoding="utf-8") as f:
            VERSES_DATA = json.load(f)

load_verses_data()

PROGRESS_FILE = "progress.json"
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f: 
            return json.load(f)
    return {"streak":0, "goal":5, "today":0, "last_date": "", "ayahs":{}}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f: 
        json.dump(data, f, ensure_ascii=False)

@app.get("/api/surahs")
def get_surahs(): 
    return SURAHS

@app.get("/api/verses/{surah}")
def get_verses(surah: int):
    if str(surah) in VERSES_DATA:
        return VERSES_DATA[str(surah)]
    return [{"id": f"{surah}:1", "text": "وَاتَّقُواْ اللّهَ", "audio": "", "number": 1}]

@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    await file.read()
    return {"text": "مرحبا", "words": [{"word": "مرحبا", "start": 0, "end": 1}]}

@app.get("/api/progress")
def get_prog(): 
    return load_progress()

@app.post("/api/progress")
def set_prog(data: dict):
    prog = load_progress()
    prog.update(data)
    save_progress(prog)
    return {"status":"ok"}

@app.get("/")
def index(): 
    return HTMLResponse(open("index.html", "r", encoding="utf-8").read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
