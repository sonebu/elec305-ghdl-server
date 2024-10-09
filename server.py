import uvicorn, json, enum, time, os, requests, glob
from typing import Union
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from functions import bl3_wakeup_ytaudioreq_timestrjid, redirect_getlink
from sources import source_interface_jp2ensrt
from sources import source_redirect_aid

bl1_url = "https://ghdl.buraksoner.com"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

@app.get("/")
def home_get(request: Request):
    result = 'submit your vhdl code'
    return templates.TemplateResponse('home.html', context={'request': request})

@app.get("/health_check", status_code=200)
def health_check(request:Request):
    return "Healthy"

@app.post('/')
def home_post(request: Request, input_text: str = Form("")):
    timestr  = time.strftime("%Y%m%d%H%M%S")
    clientIP = request.client.host

    ### Health checks
    if(input_text == ""):
        output = "enter a non-empty string in the text box"
        return templates.TemplateResponse('home.html', context={'request': request, 'result': output, 'input_text': input_text})

    ### inputs are OK if we made it this far
    return templates.TemplateResponse('home.html', context={'request': request, 'result': "OK", 'input_text': input_text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, forwarded_allow_ips='*')
