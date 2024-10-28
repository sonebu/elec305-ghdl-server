import uvicorn, time, os, subprocess, jsonlines, enum
from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

base_url = "https://ghdl.buraksoner.com"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

# not sure if this is necessary
@app.get("/health_check", status_code=200)
def health_check(request:Request):
    return "Healthy"

class hwChoices(str, enum.Enum):
    hw1 = "HW1"
    
@app.post('/')
def home_post(request: Request, hw_selection: hwChoices = Form(hwChoices)):
    hw_name = hw_selection.name
    redirect_url = base_url + "/" + hw_name
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/")
def home_get(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})

@app.get("/hw1")
def home_get(request: Request):
    return templates.TemplateResponse('hw1.html', context={'request': request})

def inputchecks(username, password, input_text):
    if(input_text == ""): # fail case
        message = "enter a non-empty string in the text box"
        return -1, message
    else:
        with jsonlines.open('usercreds.jsonl', 'r') as jsonl_f:
            users = [obj for obj in jsonl_f]
        match_user = False
        for userdict in users:
            if((username == userdict["username"]) and (password == userdict["password"])):
                match_user = True
                break
        if(not match_user): # fail case
            output =  "username and password combination not found in database<br>"
            output += "make sure you entered them correctly<br><br>"
            output += "note that the server does not check validity of inputs<br>"
            output += "so you need to check your inputs yourself (e.g., whitespaces)"
            return -1, output
        else:
            return 0

@app.post('/hw1_q1')
async def home_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form("")):
    timestr  = time.strftime("%Y%m%d_%H%M%S")
    clientIP = request.client.host

    ret, msg = inputchecks(username, password, input_text)
    if(ret == 0): # inputs are OK if we made it this far
        username = username.split("@")[0]
        submissionfolder_name = './submissions/hw1/'+username+'/'
        submissionfolder_exists = os.path.isdir(submissionfolder_name)
        if(not submissionfolder_exists):
            os.makedirs(submissionfolder_name)
        submissionfile_name = timestr + "_" + clientIP.replace(".","p") + "_" + username + ".vhdl"
        with open(submissionfolder_name + submissionfile_name, "w") as src:
            src.write(input_text)
        ghdl_run_result = subprocess.run(['ghdl', '-a', submissionfolder_name + submissionfile_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ghdl_run_result_err = ghdl_run_result.stderr.decode('utf-8')
        ghdl_run_result_out = ghdl_run_result.stdout.decode('utf-8')
        if(ghdl_run_result_err == ""):
            output = "No errors."
        else:
            output = "GHDL Output:<br>"
            output += ghdl_run_result_err
            output += ghdl_run_result_out
            responsefile_name = timestr + "_" + clientIP.replace(".","p") + "_" + username + ".dbg"
            with open(submissionfolder_name + responsefile_name, "w") as dbg:
                dbg.write(output)
    else:
        output = msg

    return templates.TemplateResponse('hw1.html', context={'request': request, 'input_text': input_text, 'qout': output})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, reload=True, forwarded_allow_ips='*')
