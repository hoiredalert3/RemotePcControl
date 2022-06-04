import subprocess
import psutil


def list_app():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    data=''
    for line in proc.stdout:
        if line.rstrip():
            data+=str(line.decode().rstrip())+'\n'
    return data
def list_process():
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
        # Get process detail as dictionary
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        # Append dict of process detail in list
        main_info=pInfoDict['name']
        listOfProcessNames.append(main_info)
    data=''
    for s in listOfProcessNames:
        data+=s
        data+='\n'
    return data
def kill_process(process):
    subprocess.call(["taskkill","/F","/IM",process])
