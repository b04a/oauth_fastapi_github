from http.client import responses

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

GITHUB_CLIENT_ID = "your GITHUB_CLIENT_ID"
GITHUB_CLIENT_SECRET = "youre GITHUB_CLIENT_SECRET"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}")

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get('code')

    #MORE INFO:
    #https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
    token_user_auth = 'https://github.com/login/oauth/access_token'

    #get info about user by GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
    response = requests.post(token_user_auth, data={
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code
    }, headers={'Accept': 'application/json'})

    #convert response in json data
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        user_info_url = 'https://api.github.com/user'
        user_info_response = requests.get(user_info_url, headers={
            'Authorization': f'token {access_token}'
        })

        user_info = user_info_response.json()

        # Используем шаблон для отображения приветствия
        return templates.TemplateResponse("greeting.html", {"request": request, "username": user_info['login']})
    else:
        return 'Error returned during authentication'