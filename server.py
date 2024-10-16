import uvicorn, time, os, subprocess, jsonlines
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
def home_post(request: Request, pwd: str = Form(""), email: str = Form(""), input_text: str = Form("")):
    timestr  = time.strftime("%Y%m%d_%H%M%S")
    clientIP = request.client.host

    ### Health checks
    if(input_text == ""): # fail case
        output = "enter a non-empty string in the text box"
    else:
        with jsonlines.open('usercreds.jsonl', 'r') as jsonl_f:
            users = [obj for obj in jsonl_f]
        match_user = False
        for userdict in users:
            if((email == userdict["email"]) and (pwd == userdict["password"])):
                match_user = True
                break
        if(not match_user): # fail case
            output =  "email and pwd combination not found in database<br>"
            output += "make sure you entered them correctly<br><br>"
            output += "note that the server does not check validity of inputs<br>"
            output += "so you need to check your inputs yourself (e.g., whitespaces)"
        else:
            # inputs are OK if we made it this far
            username = email.split("@")[0]
            submissionfolder_name = './submissions/'+username+'/'
            submissionfolder_exists = os.path.isdir(submissionfolder_name)
            if(not submissionfolder_exists):
                os.makedirs(submissionfolder_name)
            submissionfile_name = timestr + "_" + clientIP.replace(".","p") + "_" + username+ ".vhdl"
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
                responsefile_name = timestr + "_" + clientIP.replace(".","p") + "_" + username+ ".dbg"
                with open(submissionfolder_name + responsefile_name, "w") as dbg:
                    dbg.write(output)
            
    return templates.TemplateResponse('home.html', context={'request': request, 'result': output, 'input_text': input_text})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, forwarded_allow_ips='*')
