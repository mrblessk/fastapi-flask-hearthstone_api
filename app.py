# Core packages
from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template
import uvicorn

# FastAPI Templating
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# utils
import json

with open('data/hs_cards.json', encoding="utf8") as f:
    cardlist = json.load(f)


# Init Api & App
api = FastAPI()
app = Flask(__name__)

# Mount Flask on FastAPI
api.mount('/main', WSGIMiddleware(app))


# API Routes/Endpoints

# ::: Root
@api.get('/api', include_in_schema=False)
async def root_app():
    return {'text': 'Hello Hearthstone FastAPI'}

# ::: Data

# .../api/v1/cards/?limit=10
# ::: QueryParam
@api.get('/api/v1/cards')
async def read_all_cards(limit:int=10):
    """Return a list of all cards in limit"""
    return {'data': cardlist[:limit]}

# .../api/v1/cards/{card}
# ::: Path param
@api.get('/api/v1/cards/{card}')
async def read_card(card:str):
    """Return card by card name"""
    current_card = [item for item in cardlist if item['name'] == card.title()]
    return {'data': current_card}

# .../api/v1/cards/{card}/{key}
# ::: Path param
@api.get('/api/v1/cards/{card}/{key}')
async def read_card_attribute(card:str, key:str):
    """Return card detail by card name"""
    current_card = [item for item in cardlist if item['name'] == card.title()]
    current_card_att = current_card[0].get(key)
    return {'data': current_card_att}

# .../api/v1/cards/{card_id}
# ::: Path param
@api.get('/api/v1/cards/{card_id}')
async def read_card_by_card_id(card_id:str):
    """Return card by ID"""
    current_card = [item for item in cardlist if item['id'] == card_id.title()]
    return {'data': current_card}

# .../api/v1/cards/{card_id}/{key}
# ::: Path param
@api.get('/api/v1/cards/{card_id}/{key}')
async def read_card_attribute_by_id(card_id:str, key:str):
    """Return card detail by id"""
    current_card = [item for item in cardlist if item['id'] == card_id.title()]
    current_card_att = current_card[0].get(key)
    return {'data': current_card_att}


# FastAPI Templating moves
# Location for html
templates = Jinja2Templates(directory='templates/docs')


@api.get('/', response_class=HTMLResponse, include_in_schema=False)
async def docs_render(request: Request):
    """Render base navigation"""
    return templates.TemplateResponse('docs_fastapi.html', {'request': request})


@api.get('/show_card/', response_class=HTMLResponse, include_in_schema=False)
async def show_cards(request: Request, card_name):
    """Show card by name"""
    result = [item for item in cardlist if item['name'] == card_name]
    return templates.TemplateResponse('docs_fastapi.html', {'request': request, 'card': result[0]})


# Flask Section
@app.route('/')
def main_page():
    return render_template('main.html')


if __name__ == '__main__':
    uvicorn.run(api, host='127.0.0.1', port=8000)
