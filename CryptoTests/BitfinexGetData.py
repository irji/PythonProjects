import requests
import json

#url = "https://api.bitfinex.com/v1/pubticker/btcusd"
#response = requests.request("GET", url)
#obj1 = json.loads(response.text)
#print(obj1["bid"])

allTikers = []
#usdTikers = []
eurTikers = []

def GetAllTickers():
    url = "https://api.bitfinex.com/v1/symbols"
    res=requests.request("GET", url)

    allTikers=res.text.replace("[","").replace("]","").split(",")

    for t in allTikers:
        #print(t)
        #if str(t).__contains__("usd"):
        #    usdTikers.append(t)
        if str(t).__contains__("eur"):
            eurTikers.append(t)

    #print(len(usdTikers))
    print(len(eurTikers))


def main():
    GetAllTickers()

if __name__ == '__main__':
    main()
    pass