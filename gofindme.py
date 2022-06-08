from ast import arg
import requests
import json
import sys
import getopt
import csv
opts, args = getopt.getopt(sys.argv[1:], "c:dfh", ['campaign'])

cflag = False
dflag = False
fglag = False

for opt, arg in opts:
    if opt == '-c':
        campaign = arg
        cflag = True
    
    if opt == '-d':
        dflag = True
    
    if opt == '-f':
        fflag = True

    elif opt == '-h':
        print("\n")
        print("usage example: gofindme.py -c https://www.gofundme.com/f/digitalandrews-fundraising-campaign -d -f")
        print("\n")
        print("-c           Set Campaing URL")
        print("-d           Show donation amounts in output")
        print("-f           Write output to CSV file")
        quit()

if cflag == False:
    print("usage: gofindme.py -c campaignstring")
    quit()

try:
        campaign = campaign[campaign.index('f/') + 2 : ]
        campaign = campaign[0 : campaign.index('?')]

except ValueError:
        pass

url = "https://gateway.gofundme.com/web-gateway/v1/feed/{}/".format(campaign)
donationsAPI = "donations"
countAPI = "counts"

#API request to get counts data which contains total donations
request = requests.request(
        "GET", url+countAPI, data="", headers="")

counts = request.text

# clean up response to remove additional unnneded objects
try:
        
        counts = counts[counts.index(':') + 1 : ]
        counts = counts[counts.index(':') + 1 : ]
        counts = counts[0 : counts.index('},"meta"')]

except ValueError:
        pass
try:
    countsdict = json.loads(counts)
    totaldonations =  countsdict["total_donations"]
except:
    print("Cannot find campaign, check campaign url, see -h for help")
    quit()

donatorq = ""

#API Request to get donations info (limit of 100 donations per request, must split into multiple requests)
for i in range(int(totaldonations/100) + 1):

    querystring = {"limit": 100, "offset": (i)*100}

    response = requests.request(
        "GET", url+donationsAPI, data="", headers="", params=querystring)
    donator = response.text

    # Remove all characters before the character '[' from string and after ']' to split out json objects
    try:
        donator = donator[donator.index('[') + 1 : ]
        donator = donator[0 : donator.index(']')]
    except ValueError:
        pass

    #if not the last request of donations add comma delimiter
    if i < int(totaldonations/100):
        donator += ","

    donatorq += donator   

#split into single json objects on delimiter
donatorq=donatorq.split("},")

#Add back in { to complet json object
for i in range(len(donatorq)-1):
    donatorq[i]+="}"


       
            
#for each json object change it to dictionary
for i in range(len(donatorq)):
    donatordict = json.loads(donatorq[i])
    if dflag == True:
        print (donatordict["name"] + "(" + str(donatordict["amount"]) + donatordict["currencycode"] + ")")
    else:
        print (donatordict["name"])
    
if fflag == True:
     with open('{}.csv'.format(campaign), 'w', newline='') as file:
            fieldnames = ['Name', 'Amount Donated', 'Currency', 'Donation Date/Time']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
            
            csv_writer.writeheader()
            for i in range(len(donatorq)):
                donatordict = json.loads(donatorq[i])
                csv_donatordict = {"Name": donatordict["name"], "Amount Donated": donatordict["amount"], "Currency": donatordict["currencycode"], "Donation Date/Time": donatordict["created_at"]}
                csv_writer.writerow(csv_donatordict)





