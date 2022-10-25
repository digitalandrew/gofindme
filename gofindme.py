import requests
import json
import sys
import getopt
import csv


class flags:
    def __init__(self):
        self.cflag = False
        self.dflag = False
        self.fflag = False
        self.hflag = False
        self.campaign = ""

    def set_flags(self):
        opts, args = getopt.getopt(sys.argv[1:], "c:dfh", ["campaign"])
        for opt, arg in opts:
            if opt == "-c":
                self.campaign = arg
                self.cflag = True
            if opt == "-d":
                self.dflag = True
            if opt == "-f":
                self.fflag = True
            if opt == "-h":
                self.hflag = True


def print_boilerplate():
    print("")
    print("**************************************************")
    print("               __ _           _         ")
    print("              / _(_)         | |               ")
    print("   __ _  ___ | |_ _ _ __   __| |_ __ ___   ___ ")
    print("  / _` |/ _ \|  _| | '_ \ / _` | '_ ` _ \ / _ \\")
    print(" | (_| | (_) | | | | | | | (_| | | | | | |  __/")
    print("  \__, |\___/|_| |_|_| |_|\__,_|_| |_| |_|\___|")
    print("   __/ |                                       ")
    print("  |___/     ")
    print("")
    print("**************************************************")
    print("")
    print("Created by: DigitalAndrew - https://github.com/digitalandrew/gofindme")
    print("")


def print_help():
    print("usage example: ")
    print(
        " gofindme.py -c https://www.gofundme.com/f/digitalandrews-fundraising-campaign -d -f"
    )
    print("")
    print("Options: ")
    print(" -c           Set Campaign URL")
    print(" -d           Show donation amounts in output")
    print(" -f           Write output to CSV file")


def create_api_url(campaign_url):
    #Creates the API url from the campagin url, returns string with api url
    try:
        campaign_url = campaign_url[campaign_url.index("f/") + 2 :]
        campaign_url = campaign_url[0 : campaign_url.index("?")]
    except ValueError:
        pass
    api_url = "https://gateway.gofundme.com/web-gateway/v1/feed/{}/".format(
        campaign_url
    )
    return api_url


def get_number_donations(api_url):
    # API request to get counts data which contains total donations, returns int of total number of donations
    count_api = "counts"

    try:
        request = requests.get(api_url + count_api, data="", headers="")
    except:
        print("Cannot find campaign, check campaign url, see -h for help")
        quit()
    counts = request.text

    counts_dict = json.loads(counts)
    counts_dict = counts_dict["references"]
    counts_dict = counts_dict["counts"]
    return counts_dict["total_donations"]


def get_donations(api_url, number_of_donations):
    #Gets all donation info and returns it in a list of dictionaries
    donations = []
    donations_api = "donations"

    # API Request to get donations info (limit of 100 donations per request, must split into multiple requests)
    for i in range(int(number_of_donations / 100) + 1):

        query_string = {"limit": 100, "offset": (i) * 100}

        response = requests.get(
            api_url + donations_api, data="", headers="", params=query_string
        )
        partial_donations = json.loads(response.text)
        partial_donations = partial_donations["references"]
        partial_donations = partial_donations["donations"]

        donations.append(partial_donations)
    flat_donations = [item for sublist in donations for item in sublist]

    return flat_donations


def print_donations(dflag, donations):
    if dflag == True:
        print("{0:35} {1}".format("Donations", "Amount"))
        print("{0:35} {1}".format("---------", "------"))
        for i in range(len(donations)):
            print(
                "{0:35} {1}".format(
                    donations[i]["name"],
                    "("
                    + str(donations[i]["amount"])
                    + donations[i]["currencycode"]
                    + ")",
                )
            )
    else:
        print("Donations")
        print("----------")
        for i in range(len(donations)):
            print(donations[i]["name"])


def write_csv(campaign, donations):
    try:
        campaign = campaign[campaign.index("f/") + 2 :]
        campaign = campaign[0 : campaign.index("?")]
    except ValueError:
        pass
    with open("{}.csv".format(campaign), "w+", newline="") as file:
        fieldnames = ["Name", "Amount Donated", "Currency", "Donation Date/Time"]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=",")

        csv_writer.writeheader()
        for i in range(len(donations)):
            csv_donations_dict = {
                "Name": donations[i]["name"],
                "Amount Donated": donations[i]["amount"],
                "Currency": donations[i]["currencycode"],
                "Donation Date/Time": donations[i]["created_at"],
            }
            csv_writer.writerow(csv_donations_dict)


def main():

    print_boilerplate()

    my_flags = flags()
    my_flags.set_flags()

    if my_flags.hflag == True:
        print_help()
        quit()

    if my_flags.cflag == False:
        print("usage: gofindme.py -c campaignstring")
        quit()

    print("Querying Donations for - {}".format(my_flags.campaign))
    print("")

    api_url = create_api_url(str(my_flags.campaign))

    number_of_donations = get_number_donations(api_url)

    donations = get_donations(api_url, number_of_donations)

    print_donations(my_flags.dflag, donations)

    if my_flags.fflag == True:
        write_csv(my_flags.campaign, donations)


if __name__ == "__main__":
    main()
