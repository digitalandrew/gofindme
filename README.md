# gofindme - gofundme OSINT tool

gofindme is a quick to use webscraping tool to quickly pull down a list of donators and donation amounts from gofundme campaigns.

I initially created this tool for use in TraceLabs missing person CTFs as I found GoFundMe campaigns to give lots of leads however manually scrolling through the donations list to populate the full list was time consuming. 

## Usage Example

```console
$ python3 gofindme.py -c https://www.gofundme.com/f/digitalandrews-fundraising-campaign -d -f

Required Arguments:
 -c         Specifies campaign URL
 
 Optional Arguments
 -d         Show donation amounts in console output
 -f         Write Name, Donation Amount and Time of donation to csv file
 -h         Help
 

```
