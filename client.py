import requests
import json

server_url = 'http://localhost:8080'
log_headers = {"Content-type": "application/json", "type": "log"}
req_headers = {"Content-type": "application/json", "type": "req"}


def validate_json(inp):
    try:
        json.loads(inp)
    except ValueError:
        print("entered input is not in application/json format")
        return False
    return True


while True:
    print("username : ")
    username = input()
    print()
    print("password : ")
    password = input()
    log_input = '{ "username":"' + username + '", "password":"' + password + '"}'
    auth_resp = requests.post(server_url, data=log_input, headers=log_headers)
    if auth_resp.text == "wp":
        print()
        print("your password is wrong")
        continue

    req_headers["auth"] = auth_resp.text

    while True:
        print()
        print("Enter your input in json format : ")
        json_input = input()
        if json_input == "so":
            print("you just signed out")
            break

        if validate_json(json_input):
            response = requests.post(server_url, data=json_input, headers=req_headers)
            print("Server response : ")
            print(response.text)
            print()
