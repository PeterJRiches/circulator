# import required library for accessing Sierra with authorization
import requests
import json
import secrets
import csv

# function that gets the authentication token
def get_token():
    url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v3/token"
    header = {"Authorization": "Basic " + str(secrets.sierra_api), "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    json_response = json.loads(response.text)
    token = json_response["access_token"]
    return token

# function that gets all of the items in the circulator
def update_circulator_info():

    token = get_token()
    request = requests.get("https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v5/items?status=y&fields=id,bibIds,callNumber", headers={
            "Authorization": "Bearer " + token
        })
    try:
        json_response = json.loads(request.text)['entries']
    except KeyError:
        json_response = []
        print(f'No Items Found {request.status_code}')
    return json_response

# creates the csv file
def main():
    circulator_file = open('//CHFS/Shared Documents/OpenData/datasets/staging/circulator.csv', 'w')
    csvwriter = csv.writer(circulator_file)
    csvwriter.writerow(['id','BibIds','Call Number'])
    circulator_info = update_circulator_info()
    for entry in circulator_info:
        row = []
        row.append(entry["id"])
        row.append(entry["bibIds"][0])
        try:
            row.append(entry["callNumber"])
        except: 
            row.append(" ")
        csvwriter.writerow(row)

# call the main function
main()
