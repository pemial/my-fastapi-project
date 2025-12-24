from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random
from fastapi.responses import RedirectResponse

app = FastAPI(title='URL shortener')

class URLItem(BaseModel):
    url: str

db = {}

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        if short_id in db:
            continue
        return short_id

# POST /shorten: принимает полный URL (JSON: {“url”:"…"}) и возвращает короткую ссылку
@app.post('/shorten')
def shorten_url(item: URLItem):
    short_id = generate_short_id()
    db[short_id] = {'url': item.url, "clicks": 0}
    return {'short_id': f'http://127.0.0.1:8000/{short_id}'}

# GET /{short_id}: перенаправляет на полный URL, если он существует
@app.get('/{short_id}')
def redirect_to_url(short_id: str):
    if short_id not in db:
        raise HTTPException(status_code=404, detail='URL not found')
    db[short_id]['clicks'] += 1
    return RedirectResponse(db[short_id]['url'])

# GET /stats/{short_id}: возвращает файл JSON с информацией о полном URL
@app.get('/stats/{short_id}')
def get_stats(short_id: str):
    if short_id not in db:
        raise HTTPException(status_code=404, detail='URL not found')
    return {'url': db[short_id]['url'], 'clicks': db[short_id]['clicks']}
