import uvicorn, time, os, subprocess
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
    else:
        ### inputs are OK if we made it this far
        with open("circ.vhdl", "w") as src:
            src.write(input_text)
        ghdl_run_result = subprocess.run(['ghdl', '-a', 'circ.vhdl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ghdl_run_result_err = ghdl_run_result.stderr.decode('utf-8')
        ghdl_run_result_out = ghdl_run_result.stdout.decode('utf-8')
        print(ghdl_run_result)
        if(ghdl_run_result_err == ""):
            output = "No errors."
        else:
            output = "GHDL Output:<br>"
            output += ghdl_run_result_err
            output += ghdl_run_result_out
            
    return templates.TemplateResponse('home.html', context={'request': request, 'result': output, 'input_text': input_text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, forwarded_allow_ips='*')
