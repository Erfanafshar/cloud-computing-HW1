from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import subprocess

host_name = 'localhost'
server_port = 8080
auth_headers = {'Content-type', 'text/plain'}
res_headers = {'Content-type', 'application/json'}
auth_table = [('admin', '123', 'admin--123'), ('user1', '22', 'user1--22')]


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

class Server(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        received_data = self.rfile.read(content_length)
        input_dic = json.loads(received_data)

        if self.headers['type'] == "log":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            username = input_dic['username']
            password = input_dic['password']

            for i in range(len(auth_table)):
                if username == auth_table[i][0]:
                    if password == auth_table[i][1]:
                        self.wfile.write(bytes(auth_table[i][2], 'utf-8'))
                    else:
                        self.wfile.write(bytes("wp", 'utf-8'))
                    break
            else:
                auth_token = username + "--" + password
                auth_table.append((username, password, auth_token))

                self.wfile.write(bytes(auth_token, 'utf-8'))

        # print(auth_table)

        if self.headers['type'] == "req":
            auth_token = self.headers['auth']
            if auth_token == 'admin--123':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                output_command_all = subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out_all, err_all = output_command_all.communicate()
                   
                command = input_dic['command']
                if command is 'clone':
                    self.wfile.write(bytes("permission denied", 'utf-8'))
                    return
                if 'vmName' in input_dic:
                    vmName = str(input_dic['vmName'])
                    if vmName != "VM1":
                        self.wfile.write(bytes("permission denied", 'utf-8'))
                        return
 
            if 'command' in input_dic:
                command = input_dic['command']

                if command == 'status':
                    if 'vmName' not in input_dic:
                        output_command_all = subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        output_command_run = subprocess.Popen(['vboxmanage', 'list', 'runningvms'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        out_all, err_all = output_command_all.communicate()
                        out_run, err_run = output_command_run.communicate()
                        
                        lst = find(out_all.decode('utf-8'), '"')
                        i = 0
                        all_vm = []
                        while i != len(lst):
                            vmName = out_all.decode('utf-8')[lst[i] + 1:lst[i+1]]
                            all_vm.append(vmName)
                            i += 2
                          
                        lst = find(out_run.decode('utf-8'), '"')
                        i = 0
                        run_vm = []
                        while i != len(lst):
                            vmName = out_run.decode('utf-8')[lst[i] + 1:lst[i+1]]
                            run_vm.append(vmName)
                            i += 2
                        
                        out = '{ "command": "status", "details": ['
                        for vm in all_vm:
                            if vm in run_vm:
                               out += '{"vmName": "'
                               out += vm 
                               out += '","status": "on"}'
                            else:
                               out += '{"vmName": "'
                               out += vm 
                               out += '","status": "off"'
                            out += ', '
                        out += '] }'
                        
                        self.wfile.write(bytes(out, 'utf-8'))
                        
                    else:                           
                        output_command_all = subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        output_command_run = subprocess.Popen(['vboxmanage', 'list', 'runningvms'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        out_all, err_all = output_command_all.communicate()
                        out_run, err_run = output_command_run.communicate()
                        vmName = str(input_dic['vmName'])
                        
                        if vmName in out_all.decode('utf-8'):
                            if vmName in out_run.decode('utf-8'):
                                output = '{"command": "status","vmName": "' + vmName +'","status": "on"}'
                            else:
                                output = '{"command": "status","vmName": "' + vmName +'","status": "off"}'
                            self.wfile.write(bytes(output, 'utf-8'))
                        else:
                            self.wfile.write(bytes("Wrong virtual machine name", 'utf-8'))

                elif command == 'on':
                    output_command = os.system('cmd /c "vboxmanage startvm VM1"')
                    print(output_command)
                    vmName = input_dic['vmName']
                    output = '{"command": "on","vmName": "' + vmName +'","status": "powering on"}'
                    self.wfile.write(bytes(output, 'utf-8'))

                elif command == 'off':
                    output_command = os.system('cmd /c "vboxmanage controlvm "VM1" poweroff"')
                    print(output_command)
                    vmName = input_dic['vmName']
                    output = '{"command": "off","vmName": "' + vmName +'","status": "powering off"}'
                    self.wfile.write(bytes(output, 'utf-8'))

                elif command == 'setting':                      
                    
                    vmName = input_dic['vmName']
                    cpu = input_dic['cpu']
                    ram = input_dic['ram']
                        
                    cmd1 = 'cmd /c "vboxmanage modifyvm ' + vmName + ' --memory ' + str(ram) + '"'
                    cmd2 = 'cmd /c "vboxmanage modifyvm ' + vmName + ' --cpus ' + str(cpu) + '"'
                 
                    output_command_1 = os.system(cmd1)
                    output_command_2 = os.system(cmd2)
                    output = '{"command": "setting","vmName": "' + vmName + '","cpu": ' + str(cpu) + ',"ram": ' + str(ram) + ',"status": "ok"}'
                    self.wfile.write(bytes(output, 'utf-8'))

                elif command == 'clone':
                   
                    
                    sourceVmName = input_dic['sourceVmName']
                    destVmName = input_dic['destVmName']
                        
                    cmd1 = 'cmd /c "vboxmanage export ' + sourceVmName + ' --output D:\A_newapp\VMs\\tmp\\new.ova"'
                    cmd2 = 'cmd /c "vboxmanage import D:\A_newapp\VMs\\tmp\\new.ova --vsys 0 --vmname ' + destVmName + '"'
                 
                    output_command_1 = os.system(cmd1)
                    output_command_2 = os.system(cmd2)
                    output = '{"command": "clone","sourceVmName": "' + sourceVmName + '","destVmName": "' + destVmName + '","status": "ok"}'
                    self.wfile.write(bytes(output, 'utf-8'))

                elif command == 'delete':
                
                    vmName = input_dic['vmName']
                                                    
                    cmd = 'cmd /c "vboxmanage unregistervm ' + vmName + '"'
                 
                    output_command_1 = os.system(cmd)
                    output = '{"command": "delete","vmName": "' + vmName + '","status": "ok"}'
                    self.wfile.write(bytes(output, 'utf-8'))

                else:
                    print("specified command doesn't recognized")
            else:
                print("command didn't specified")


if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), Server)
    print("Server started http://%s:%s" % (host_name, server_port))
    webServer.serve_forever()
