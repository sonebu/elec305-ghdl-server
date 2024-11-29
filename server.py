import uvicorn, time, os, subprocess, jsonlines, enum, shutil
from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from vcd2wavedrom import run_vcd2wavedrom

base_url = "https://ghdl.buraksoner.com"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/content", StaticFiles(directory="content", html = True), name="content")
templates = Jinja2Templates(directory='templates')
    
###################################################################################################################################################################
### Generic Routes
###

### Home: select HW
@app.get("/")
def home_get(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})

### Check submissions
@app.get("/checksubmissions")
def checksubmissions_get(request: Request, password: str = Form(""), username: str = Form("")):
    return templates.TemplateResponse('checksubmissions.html', context={'request': request, 'qout': 'Submission state table will appear here'})

@app.post("/checksubmissions")
def checksubmissions_post(request: Request, password: str = Form(""), username: str = Form("")):
    inputs_healthy, msg = inputchecks(username, password, "dummy text")
    if(inputs_healthy):
        hw1_q1_note, hw1_q2_note, hw1_q3_note, hw1_q4_note, hw1_q5_note = check_hw1_for_user(username);
        hw2_q1_note, hw2_q2_note, hw2_q3_note = check_hw2_for_user(username);
        output = f"""
<table>
<tr> <th></th>          <th>HW1</th>            <th>HW2</th></tr>
<tr> <td><b>Q1</b></td> <td>{hw1_q1_note}</td>  <td>{hw2_q1_note}</td> </tr>
<tr> <td><b>Q2</b></td> <td>{hw1_q2_note}</td>  <td>{hw2_q2_note}</td> </tr>
<tr> <td><b>Q3</b></td> <td>{hw1_q3_note}</td>  <td>{hw2_q3_note}</td> </tr>
<tr> <td><b>Q4</b></td> <td>{hw1_q4_note}</td>  <td>{"no hw q"}</td> </tr>
<tr> <td><b>Q5</b></td> <td>{hw1_q5_note}</td>  <td>{"no hw q"}</td> </tr>
</table>
"""
    else:
        output = msg
    return templates.TemplateResponse('checksubmissions.html', context={'request': request, 'qout': output})

def check_hw1_for_user(username):
    hw1_q1_note = checksubmission_for_hw_q_username(hw_tag = "hw1", question_tag = "q1", username = username);
    hw1_q2_note = checksubmission_for_hw_q_username(hw_tag = "hw1", question_tag = "q2", username = username);
    hw1_q3_note = checksubmission_for_hw_q_username(hw_tag = "hw1", question_tag = "q3", username = username);
    hw1_q4_note = checksubmission_for_hw_q_username(hw_tag = "hw1", question_tag = "q4", username = username);
    hw1_q5_note = checksubmission_for_hw_q_username(hw_tag = "hw1", question_tag = "q5", username = username);    
    return hw1_q1_note, hw1_q2_note, hw1_q3_note, hw1_q4_note, hw1_q5_note

def check_hw2_for_user(username):
    hw2_q1_note = checksubmission_for_hw_q_username(hw_tag = "hw2", question_tag = "q1", username = username);
    hw2_q2_note = checksubmission_for_hw_q_username(hw_tag = "hw2", question_tag = "q2", username = username);
    hw2_q3_note = checksubmission_for_hw_q_username(hw_tag = "hw2", question_tag = "q3", username = username);
    return hw2_q1_note, hw2_q2_note, hw2_q3_note

@app.get("/checksubmissions_admin")
def checksubmissions_admin_get(request: Request, password: str = Form(""), username: str = Form("")):
    return templates.TemplateResponse('checksubmissions.html', context={'request': request, 'qout': 'Enter admin creds.'})

@app.post("/checksubmissions_admin")
def checksubmissions_admin_post(request: Request, password: str = Form(""), username: str = Form("")):
    inputs_healthy, msg = inputchecks(username, password, "dummy text")
    if(inputs_healthy):
        with jsonlines.open('usercreds.jsonl', 'r') as jsonl_f:
            users = [obj for obj in jsonl_f]
        for userdict in users:
            if(userdict["username"] == "buraksoner"):
                adminpwdcheck = userdict["password"]
                break
        if((username == "buraksoner") and (password == adminpwdcheck)):
            output = "" # just init
            for userdict in users:
                if (userdict["username"] != "buraksoner"):
                    hw1_q1_note, hw1_q2_note, hw1_q3_note, hw1_q4_note, hw1_q5_note = check_hw1_for_user(userdict["username"]);
                    hw2_q1_note, hw2_q2_note, hw2_q3_note = check_hw2_for_user(userdict["username"]);
                    output += f"""
<label style="color:white; font-family: monospace;">{userdict["username"] + " submissions:"}</label><br>
<table>
<tr> <th></th>          <th>HW1</th>            <th>HW2</th></tr>
<tr> <td><b>Q1</b></td> <td>{hw1_q1_note}</td>  <td>{hw2_q1_note}</td> </tr>
<tr> <td><b>Q2</b></td> <td>{hw1_q2_note}</td>  <td>{hw2_q2_note}</td> </tr>
<tr> <td><b>Q3</b></td> <td>{hw1_q3_note}</td>  <td>{hw2_q3_note}</td> </tr>
<tr> <td><b>Q4</b></td> <td>{hw1_q4_note}</td>  <td>{"no hw q"}</td> </tr>
<tr> <td><b>Q5</b></td> <td>{hw1_q5_note}</td>  <td>{"no hw q"}</td> </tr>
</table><br><br>
"""
        else:
            output = "incorrect admin username-pwd"
    else:
        output = msg
    return templates.TemplateResponse('checksubmissions.html', context={'request': request, 'qout': output})



###################################################################################################################################################################
### HW1 Routes
### 
@app.get("/hw1")
def hw1_get(request: Request):
    return templates.TemplateResponse('hw1.html', context={'request': request})

@app.get("/hw1_q1")
def hw1_q1_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    return templates.TemplateResponse('hw1_q1.html', context={'request': request, 'input_text': input_text, 'qout': "..."})
@app.post('/hw1_q1')
def hw1_q1_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw1', question_tag = 'q1', dut_tb_type = "dut", checker_src_tag = 'hw1_q1_tb.vhdl', # put it under ./content/
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw1_q1.html', context={'request': request, 'input_text': input_text, 'qout': output})

@app.get("/hw1_q2")
def hw1_q2_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    return templates.TemplateResponse('hw1_q2.html', context={'request': request, 'input_text': input_text, 'qout': "..."})
@app.post('/hw1_q2')
def hw1_q2_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw1', question_tag = 'q2', dut_tb_type = "dut", checker_src_tag = 'hw1_q2_tb.vhdl', # put it under ./content/
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw1_q2.html', context={'request': request, 'input_text': input_text, 'qout': output})

@app.get("/hw1_q3")
def hw1_q3_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    return templates.TemplateResponse('hw1_q3.html', context={'request': request, 'input_text': input_text, 'qout': "..."})
@app.post('/hw1_q3')
def hw1_q3_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw1', question_tag = 'q3', dut_tb_type = "dut", checker_src_tag = 'hw1_q3_tb.vhdl', # put it under ./content/
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw1_q3.html', context={'request': request, 'input_text': input_text, 'qout': output})

@app.get("/hw1_q4")
def hw1_q4_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    return templates.TemplateResponse('hw1_q4.html', context={'request': request, 'input_text': input_text, 'qout': "..."})
@app.post('/hw1_q4')
def hw1_q4_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw1', question_tag = 'q4', dut_tb_type = "dut", checker_src_tag = 'hw1_q4_tb.vhdl', # put it under ./content/
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw1_q4.html', context={'request': request, 'input_text': input_text, 'qout': output})

@app.get("/hw1_q5")
def hw1_q5_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    return templates.TemplateResponse('hw1_q5.html', context={'request': request, 'input_text': input_text, 'qout': "..."})

@app.post('/hw1_q5')
def hw1_q5_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw1', question_tag = 'q5', dut_tb_type = "dut", checker_src_tag = 'hw1_q5_tb.vhdl', # put it under ./content/
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw1_q5.html', context={'request': request, 'input_text': input_text, 'qout': output})


###################################################################################################################################################################
### HW2 Routes
### 
@app.get("/hw2")
def hw2_get(request: Request):
    return templates.TemplateResponse('hw2.html', context={'request': request})

@app.get("/hw2_q1")
def hw2_q1_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    wavedrom_listing = run_vcd2wavedrom("./content/hw2_q1_dut_tb_reftb_out.vcd", filter_signal_list=["dut_tb.dut_module.signal_in", "dut_tb.dut_module.clk", "dut_tb.dut_module.signal_out",
                                                                                                     "dut_tb.signal_in_tb", "dut_tb.clk_tb", "dut_tb.signal_out_tb"])
    ref_waveform_diag_html=f'''
    <div style="background-color:white;display: inline-block;padding: 25px;">
    <script type="WaveDrom" defer>
    {wavedrom_listing}
    </script>
    </div>
    '''
    return templates.TemplateResponse('hw2_q1.html', context={'request': request, 'input_text': input_text, 'ref_waveform_diag':ref_waveform_diag_html, 'qout':'...'})

@app.post('/hw2_q1')
def hw2_q1_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    wavedrom_listing = run_vcd2wavedrom("./content/hw2_q1_dut_tb_reftb_out.vcd", filter_signal_list=["dut_tb.dut_module.signal_in", "dut_tb.dut_module.clk", "dut_tb.dut_module.signal_out",
                                                                                                     "dut_tb.signal_in_tb", "dut_tb.clk_tb", "dut_tb.signal_out_tb"])
    ref_waveform_diag_html=f'''
    <div style="background-color:white;display: inline-block;padding: 25px;">
    <script type="WaveDrom" defer>
    {wavedrom_listing}
    </script>
    </div>
    '''
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw2', question_tag = 'q1', dut_tb_type = "tb", checker_src_tag = 'hw2_q1_dut_tb_reftb.vhdl',
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction);
    return templates.TemplateResponse('hw2_q1.html', context={'request': request, 'input_text': input_text, 'ref_waveform_diag':ref_waveform_diag_html, 'qout': output})

@app.get("/hw2_q2")
def hw2_q2_get(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    wavedrom_listing = run_vcd2wavedrom("./content/hw2_q2_dut_tb_out.vcd", filter_signal_list=["dut_tb.dut_module.signal_in", "dut_tb.dut_module.clk", 
                                                                                               "dut_tb.dut_module.enable", "dut_tb.dut_module.signal_out"])
    ref_waveform_diag_html=f'''
    <div style="background-color:white;display: inline-block;padding: 25px;">
    <script type="WaveDrom" defer>
    {wavedrom_listing}
    </script>
    </div>
    '''
    return templates.TemplateResponse('hw2_q2.html', context={'request': request, 'input_text': input_text, 'ref_waveform_diag':ref_waveform_diag_html, 'qout':'...'})

@app.post('/hw2_q2')
def hw2_q2_post(request: Request, password: str = Form(""), username: str = Form(""), input_text: str = Form(""), buttonaction: str = Form("")):
    wavedrom_listing = run_vcd2wavedrom("./content/hw2_q2_dut_tb_refout.vcd", filter_signal_list=["dut_tb.dut_module.signal_in", "dut_tb.dut_module.clk", 
                                                                                                  "dut_tb.dut_module.enable", "dut_tb.dut_module.signal_out"])
    ref_waveform_diag_html=f'''
    <div style="background-color:white;display: inline-block;padding: 25px;">
    <script type="WaveDrom" defer>
    {wavedrom_listing}
    </script>
    </div>
    '''
    output = handle_question(timestr  = time.strftime("%Y%m%d_%H%M%S"), clientIP = request.client.host, 
                             hw_tag   = 'hw2', question_tag = 'q2', dut_tb_type = "dut", checker_src_tag = 'hw2_q2_dut_tb.vhdl',
                             username = username, password = password, input_text = input_text, buttonaction = buttonaction, dut_withwavedrom=True);
    return templates.TemplateResponse('hw2_q2.html', context={'request': request, 'input_text': input_text, 'ref_waveform_diag':ref_waveform_diag_html, 'qout': output})

###################################################################################################################################################################
### Helper Functions
###

def inputchecks(username, password, input_text):
    message = '<pre style="background-color:black; color:white; font-family:monospace">'
    if(input_text == ""): # fail case
        message += "enter a non-empty string in the text box"
        inputs_healthy = False
    else:
        with jsonlines.open('usercreds.jsonl', 'r') as jsonl_f:
            users = [obj for obj in jsonl_f]
        match_user = False
        for userdict in users:
            if((username == userdict["username"]) and (password == userdict["password"])):
                match_user = True
                break
        if(not match_user): # fail case
            message +=  "username and password combination not found in database<br>"
            message += "make sure you entered them correctly<br><br>"
            message += "note that the server does not check validity of inputs<br>"
            message += "so you need to check your inputs yourself (e.g., whitespaces)"
            inputs_healthy = False
        else:
            inputs_healthy = True
            message += ""
    message += '</pre>'
    return inputs_healthy, message

def vhdl_syntax_check(submission_foldername, vhdl_filename, submission_id):
    ghdl_run_result = subprocess.run(['ghdl', '-a', vhdl_filename], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ghdl_run_result_err = ghdl_run_result.stderr.decode('utf-8')
    if(ghdl_run_result_err == ""):
        output = "No errors."
        syntax_state = "syntaxOK"
    else:
        output = 'Syntax errors:'
        output += '<pre style="background-color:black; color:white; font-family:monospace">'
        output += ghdl_run_result_err.replace("\n","<br>").replace(vhdl_filename + ":",'<font color="#C01C28"><b>line:column --> </b></font>').replace('^','<font color="#C01C28"><b>^</b></font>')
        output += "</pre>"
        syntax_state = "syntaxERROR"
    syntaxresponse_filename = submission_id + "_" + syntax_state + ".html"
    with open(submission_foldername + syntaxresponse_filename, "w") as syntax_file:
        syntax_file.write(output)
    return output

def dut_functionality_check(submission_foldername, testbench_name, submission_id, dut_withwavedrom=False):
    shutil.copyfile("./content/" + testbench_name, submission_foldername + testbench_name)
    ghdl_tb_analysis = subprocess.run(['ghdl', '-a', testbench_name], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # manually checked, make sure this is OK
    if(dut_withwavedrom):
        ghdl_tb_run  = subprocess.run(['ghdl', '-r', testbench_name.replace(".vhdl",""), '--vcd=out.vcd', '--stop-time=300ns'], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        ghdl_tb_run  = subprocess.run(['ghdl', '-r', testbench_name.replace(".vhdl","")], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ghdl_run_result_err = ghdl_tb_run.stderr.decode('utf-8')
    ghdl_run_result_out = ghdl_tb_run.stdout.decode('utf-8')
    output = '<pre style="background-color:black; color:white; font-family:monospace">'
    if (("error" in ghdl_run_result_out) or (len(ghdl_run_result_err) > 0)):
        submission_correct = False
        if(len(ghdl_run_result_out)>0):
            output += ghdl_run_result_out.replace("\n","<br>").replace('error','<font color="#C01C28"><b>error</b></font>').replace('note','<font color="#2473c7"><b>note</b></font>')
        if(len(ghdl_run_result_err)>0):
            output += ghdl_run_result_err
        output += '<br><font color="#C01C28"><b>Circuit has errors. Try again.</b></font><br>'
    else:
        print("std: ", ghdl_run_result_out)
        print("err: ", ghdl_run_result_err)
        #if ("failure" in ghdl_run_result_out):
        #    submission_correct = False
        #    if(len(ghdl_run_result_out)>0):
        #        output += ghdl_run_result_out.replace("\n","<br>").replace('failure','<font color="#C01C28"><b>failure</b></font>').replace('note','<font color="#2473c7"><b>note</b></font>')
        #    if(len(ghdl_run_result_err)>0):
        #        output += ghdl_run_result_err
        #    output += '<br><font color="#C01C28"><b>Circuit has errors. Try again.</b></font><br>'
        #else:
        #    submission_correct = True

        output += ghdl_run_result_out.replace("\n","<br>").replace('note','<font color="#2473c7"><b>note</b></font>')
        output += '<br><font color="#168233"><b>No errors, circuit works as intended.</b></font><br>'
    output += "</pre>"
    simulation_state = "simOK" if submission_correct else "simERROR"
    simulationresponse_filename = submission_id + "_" + simulation_state + ".html"
    with open(submission_foldername + simulationresponse_filename, "w") as simulation_file:
        simulation_file.write(output)
    return output, submission_correct

# todo: dut u buraya çekip submit edilen tbyi run edip çıktı wavedrom u almak lazım
def tb_functionality_check(submission_foldername, hw_tag, question_tag, ref_tb_name, submission_id):
    dut_name = hw_tag + "_" + question_tag + "_dut.vhdl"
    shutil.copyfile("./content/" + dut_name   , submission_foldername + dut_name)
    shutil.copyfile("./solutions/" + ref_tb_name, submission_foldername + ref_tb_name)
    
    # run the submitted testbench first and get the wavedrom output
    ghdl_tb_analysis = subprocess.run(['ghdl', '-a', dut_name], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # manually checked, make sure this is OK
    ghdl_tb_run      = subprocess.run(['ghdl', '-r', 'dut_tb', '--vcd=out.vcd', '--stop-time=300ns'], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ghdl_run_result_err = ghdl_tb_run.stderr.decode('utf-8')
    ghdl_run_result_out = ghdl_tb_run.stdout.decode('utf-8')
    output = '<pre style="background-color:black; color:white; font-family:monospace">'
    if (("error" in ghdl_run_result_out) or (len(ghdl_run_result_err) > 0)):
        submission_correct = False
        if(len(ghdl_run_result_out)>0):
            output += ghdl_run_result_out.replace("\n","<br>").replace('error','<font color="#C01C28"><b>error</b></font>').replace('note','<font color="#2473c7"><b>note</b></font>')
        if(len(ghdl_run_result_err)>0):
            output += ghdl_run_result_err
        output += '<br><font color="#C01C28"><b>Circuit has errors. Try again.</b></font><br>'
        output += "</pre>"
    else:
        output += ghdl_run_result_out.replace("\n","<br>").replace('note','<font color="#2473c7"><b>note</b></font>')
        output += '<br><font color="#168233">Testbench and DUT run together as intended.</font> See the waveforms from your submission below (cropped to 300 ns):<br><br>'
        output += "</pre>"
        submitted_wavedrom_listing = run_vcd2wavedrom(submission_foldername + "out.vcd", filter_signal_list=["dut_tb.dut_module.signal_in", 
                                                                                                             "dut_tb.dut_module.clk", "dut_tb.dut_module.signal_out",
                                                                                                             "dut_tb.signal_in_tb", "dut_tb.clk_tb", "dut_tb.signal_out_tb"])
        waveform_diag_html=f'''
        <div style="background-color:white;display: inline-block;padding: 25px;">
        <script type="WaveDrom" defer>
        {submitted_wavedrom_listing}
        </script>
        </div>
        '''
        output += waveform_diag_html
        
        output += '\n<pre style="background-color:black; color:white; font-family:monospace">'
        output += '<br>Now running the testbench checker, see the GHDL output for that one below:<br><br></pre>'

        # run the testbench checker (ref_tb)
        ghdl_tb_analysis = subprocess.run(['ghdl', '-a', ref_tb_name], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # manually checked, make sure this is OK
        ghdl_tb_run      = subprocess.run(['ghdl', '-r', 'reference_tb', '--stop-time=300ns'], cwd=submission_foldername, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ghdl_run_result_err = ghdl_tb_run.stderr.decode('utf-8')
        ghdl_run_result_out = ghdl_tb_run.stdout.decode('utf-8')
        output += '<pre style="background-color:black; color:white; font-family:monospace">'
        if (("error" in ghdl_run_result_out) or (len(ghdl_run_result_err) > 0)):
            submission_correct = False
            if(len(ghdl_run_result_out)>0):
                output += ghdl_run_result_out.replace("\n","<br>").replace('error','<font color="#C01C28"><b>error</b></font>').replace('note','<font color="#2473c7"><b>note</b></font>')
            if(len(ghdl_run_result_err)>0):
                output += ghdl_run_result_err
            output += '<br><font color="#C01C28"><b>Testbench has errors. Try again.</b></font><br>'
        else:
            submission_correct = True
            output += ghdl_run_result_out.replace("\n","<br>").replace('note','<font color="#2473c7"><b>note</b></font>')
            output += '<br><font color="#168233"><b>No errors, testbench works as intended.</b></font><br>'
        output += "</pre>"

    simulation_state = "simOK" if submission_correct else "simERROR"
    simulationresponse_filename = submission_id + "_" + simulation_state + ".html"
    with open(submission_foldername + simulationresponse_filename, "w") as simulation_file:
        simulation_file.write(output)
    return output, submission_correct

def handle_question(timestr, clientIP, hw_tag, question_tag, dut_tb_type, checker_src_tag, username, password, input_text, buttonaction, dut_withwavedrom=False):
    inputs_healthy, msg = inputchecks(username, password, input_text)
    if(inputs_healthy):
        submission_id         = timestr + "_" + clientIP.replace(".","p") + "_" + hw_tag + "_" + question_tag + "_" + username
        hw_q_user_foldername  = './submissions/' + hw_tag + '/' + question_tag + '/' + username + '/' 
        submission_foldername = hw_q_user_foldername + submission_id + '/'
        if(not os.path.isdir(submission_foldername)):
            os.makedirs(submission_foldername)
        vhdl_filename = submission_id + ".vhdl"
        with open(submission_foldername + vhdl_filename, "w") as src:
            src.write(input_text)

        if(buttonaction == "Check Syntax"):
            output = vhdl_syntax_check(submission_foldername, vhdl_filename, submission_id)
            if(output == "No errors."):
                output = '<pre style="background-color:black; color:white; font-family:monospace"><br><font color="#168233">No syntax errors.</font><br></pre>'
        elif(buttonaction == "Check Functionality"):
            syntax_output = vhdl_syntax_check(submission_foldername, vhdl_filename, submission_id)
            if(syntax_output == "No errors."):
                if(dut_tb_type == "dut"):
                    output, _ = dut_functionality_check(submission_foldername, checker_src_tag, submission_id, dut_withwavedrom)
                elif(dut_tb_type == "tb"):
                    output, _ = tb_functionality_check(submission_foldername, hw_tag, question_tag, checker_src_tag, submission_id)
                else:
                    print("somethings wrong, handle_question")
            else:
                output = syntax_output
        elif(buttonaction == "Submit Answer"):
            submissionrecord_filename = 'submission.record'
            previous_submissionrecord_exists = os.path.isfile(hw_q_user_foldername + submissionrecord_filename);
            previous_correct_submissionrecord_exists = False
            if(previous_submissionrecord_exists):
                with open(hw_q_user_foldername + submissionrecord_filename, "r") as submissionrecord_file:
                    submission_record = submissionrecord_file.read()
                if("correct" in submission_record):
                    previous_correct_submissionrecord_exists = True
            if(previous_correct_submissionrecord_exists):
                output = '<pre style="background-color:black; color:white; font-family:monospace">'
                output += 'You already have an <font color="#168233"><b>accepted and saved</b></font> submission, so you cannot make a new submission.<br>'
                output += 'However, you can still test alternatives with "Check Syntax" and "Check Functionality" if you want to.<br>'
                output += 'Double-check your submission status from: <a class="ulink" href="https://ghdl.buraksoner.com/checksubmissions" target="_blank">https://ghdl.buraksoner.com/checksubmissions</a><br>'
                output += "</pre>"
            else:
                syntax_output = vhdl_syntax_check(submission_foldername, vhdl_filename, submission_id)
                output = '<pre style="background-color:black; color:white; font-family:monospace">'
                if(syntax_output == "No errors."):
                    if(dut_tb_type == "dut"):
                        _, submission_correct = dut_functionality_check(submission_foldername, checker_src_tag, submission_id, dut_withwavedrom)
                    elif(dut_tb_type == "tb"):
                        _, submission_correct = tb_functionality_check(submission_foldername, hw_tag, question_tag, checker_src_tag, submission_id)
                    if(submission_correct):
                        output += 'Submission <font color="#168233"><b>accepted and saved</b></font>, no errors, congratulations &#x1F973;.<br>'
                        output += 'You can still test alternatives with "Check Syntax" and "Check Functionality" if you want to.<br>'
                        output += 'Double-check your submission status from: <a class="ulink" href="https://ghdl.buraksoner.com/checksubmissions" target="_blank">https://ghdl.buraksoner.com/checksubmissions</a><br>'
                        submission_state = "correct"
                    else:
                        output += 'Submission <font color="#168233"><b>accepted</b></font>, but it has <font color="#C01C28"><b>functional errors</b></font>. You can still resubmit.'
                        submission_state = "functional error"
                else:
                    output = 'Submission <font color="#168233"><b>accepted</b></font>, but it has <font color="#C01C28"><b>syntax errors</b></font>. You can still resubmit.'
                    submission_state = "syntax error"
                output += "</pre>"
                with open(hw_q_user_foldername + submissionrecord_filename, "w") as submissionrecord_file:
                    submissionrecord_file.write(submission_state + "\n" + submission_id)
        else:
            output = "somethings wrong, handle_question"
            print("somethings wrong, handle_question")
    else:
        output = msg

    return output

def checksubmission_for_hw_q_username(hw_tag, question_tag, username):
    hw_q_user_foldername             = './submissions/' + hw_tag + '/' + question_tag + '/' + username + '/' 
    submissionrecord_filename        = 'submission.record'
    previous_submissionrecord_exists = os.path.isfile(hw_q_user_foldername + submissionrecord_filename);
    if(previous_submissionrecord_exists):
        with open(hw_q_user_foldername + submissionrecord_filename, "r") as submissionrecord_file:
            submission_record = submissionrecord_file.read()
        
        if("correct" in submission_record):
            submission_note = '<font color="#168233"><b>done</b></font>, date_time (UTC):' + "_".join(submission_record.replace("correct\n","").split("_")[0:2])
        elif("functional error" in submission_record):
            submission_note = '<font color="#C01C28"><b>functional error</b></font>, date_time (UTC):' + "_".join(submission_record.replace("functional error\n","").split("_")[0:2])
        elif("syntax error" in submission_record):
            submission_note = '<font color="#C01C28"><b>syntax error</b></font>, date_time (UTC):' + "_".join(submission_record.replace("syntax error\n","").split("_")[0:2])
        else:
            submission_note = "somethings wrong, checksubmission_for_hw_q_username"
            print("somethings wrong, checksubmission_for_hw_q_username")
    else:
        submission_note = '<font color="#2473c7"><b>no submission</b></font>'
    return submission_note


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, forwarded_allow_ips='*') # reload=True
