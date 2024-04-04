import os
import requests
import json
import csv
from dotenv import load_dotenv
load_dotenv()

def make_api_request(service_id, integration_id, rule_file, applied_rules):
    url = f"https://www.zenduty.com/api/account/teams/5183759f-0dc3-47d5-aa32-c38a49487809/services/{service_id}/integrations/{integration_id}/transformers/"
    headers = {
        "Authorization": f"token {bearer_token}",
        "Content-Type": "application/json"
    }
    
    with open(rule_file, 'r') as file:
        data = json.load(file)
        if data.get('description', '') in applied_rules.keys():
            rule_name = data.get('description','')
            unique_id = applied_rules.get(rule_name)
            urlPatch = f"https://www.zenduty.com/api/account/teams/5183759f-0dc3-47d5-aa32-c38a49487809/services/{service_id}/integrations/{integration_id}/transformers/{unique_id}/"
            response = requests.patch(urlPatch, headers=headers, json=data)
            if(response.status_code == 200):
                print(f"Successfully patched {rule_name}")
                print("METHOD : PATCH")
            else:
                print(f"ERROR in patching rule : {rule_name} {response}")
                print("METHOD : PATCH")
        else:
            response = requests.post(url, headers=headers, json=data)
            rule_name = data.get('description','')
            if(response.status_code == 201):
                print(rule_name + " is applied successfully")
                print("METHOD : POST")
            else:
                print(f"ERROR in applying rule : {rule_name} {response}")
                print("METHOD : POST")

def getRules(service_id, integration_id, applied_rules):
    url = f"https://www.zenduty.com/api/account/teams/5183759f-0dc3-47d5-aa32-c38a49487809/services/{service_id}/integrations/{integration_id}/transformers/"
    
    headers = {
        "Authorization": f"token {bearer_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        print("Applied Rules")
        print("--------------------------------------------------------------------------------")
        data = response.json()
        for item in data:
            print(item.get('description', ''))
            applied_rules[item.get('description', '')] = item.get('unique_id', '')
    else: 
        print(response)
        print("METHOD : GET")
def main():
    json_folder = "rulesJSONS"
    global bearer_token
    bearer_token = os.environ.get("zenduty_token")
    with open('zenduty.csv', mode ='r')as file:
        csvFile = csv.reader(file, delimiter=',')
        next(csvFile)
        for row in csvFile:
            service_name = row[0]
            service_id = row[1]
            integration_id = row[2]

            print(f"Scripting running for : {service_name}")
            print("--------------------------------------------------------------------------------")
            applied_rules = {}

            getRules(service_id, integration_id, applied_rules)
            print("Rule Applying Status")
            print("--------------------------------------------------------------------------------")
            for filename in os.listdir(json_folder):
                rule_file = os.path.join(json_folder, filename)
                make_api_request(service_id, integration_id, rule_file, applied_rules)
            print("--------------------------------------------------------------------------------")
            print("\n")

if __name__ == "__main__":
    main()
