import requests
import json
import time

def open_dict(loc):
    with open(loc) as json_file:
        data = json.load(json_file)
        return data

def write_json(data, filename): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent = 4)

#this function will handle the api call and return True, if the call was successful, false if the call returned and error
def create_assoc(apiKey, newJson):
    url = "https://api.hubapi.com/crm-associations/v1/associations/create-batch" + "?hapikey=" + apiKey
    put = requests.put(url, json = newJson, headers = {'accept': 'application/json'})
    if(put.status_code != 204):
        print("API-Call was not successfull - ERROR", put.status_code, ". Was not able to update ...")
        return False
    else:
        print("PUT-Request responded", put.status_code, ". Successfully updated!")
        return True

if __name__ == "__main__":
    assocs = open_dict("./new_assoc.json")
    num_assocs = len(assocs['data'])
    print("Length of Array: " + str(num_assocs))
    print("Starting the updating process...")

    apiKey = input("Pls input your API-KEY: ")

    assoc_package = []
    package_count = 0

    #will loop thru each individual association change,
    #transform them into packages of 50 packages each,
    #call the association api for each package
    for x in range(1, num_assocs):
        assoc_package.append(assocs['data'][x])
        
        if(x % 50 == 0 or x == num_assocs - 1):
            write_json(assoc_package, "dump/test_" + str(package_count) + ".json")
            time.sleep(1)
            if(create_assoc(apiKey, open_dict("dump/test_" + str(package_count) + ".json")) == False):
                print("Error at package " + str(package_count))
                break
            assoc_package = []
            package_count += 1