import requests
import json
import time
import datetime

# url = "https://cex.io/api/currency_limits"
# url = "https://cex.io/api/tickers/BTC/ETH/USD/BCH/BTG/DASH/XRP/XLM/ZEC/GHS"
# response = requests.request("GET", url)
# obj1 = json.loads(response.text)
# print(obj1)

allTikers = []
btcTikers = []
usdTikers = []
eurTikers = []
pairs = []

invest = 100


def GetAllTickers():
    url = "https://cex.io/api/tickers/BTC/ETH/USD/EUR/BCH/BTG/DASH/XRP/XLM/ZEC/GHS"
    res = requests.request("GET", url)

    obj1 = json.loads(res.text)

    # print(len(obj1["data"]))

    for t in obj1["data"]:
        # print(t)
        allTikers.append(t)

        if str(t["pair"]).lower().__contains__(":btc"):
            btcTikers.append(t)
        if str(t["pair"]).lower().__contains__("usd"):
            usdTikers.append(t)
        if str(t["pair"]).lower().__contains__("eur"):
            eurTikers.append(t)

    # print(len(btcTikers))
    # print(len(usdTikers))
    # print(len(eurTikers))
    print("Считано инструментов: " + str(len(allTikers)))


def CreatePairs():
    for e in eurTikers:
        s1 = str(e["pair"]).split(":")

        for b in btcTikers:
            if str(b["pair"]).__contains__(s1[0]):
                s2 = str(b["pair"]).split(":")
                if s1[0] == "BTC":
                    pair = [str(e["pair"]), str(b["pair"]), s2[0] + ":" + s1[1]]
                else:
                    pair = [str(e["pair"]), str(b["pair"]), s2[1] + ":" + s1[1]]

                pairs.append(pair)

    #print("Создано пар c EUR: " + str(len(pairs)))

    for d in usdTikers:
        s1 = str(d["pair"]).split(":")

        for b in btcTikers:
            if str(b["pair"]).__contains__(s1[0]):
                s2 = str(b["pair"]).split(":")
                if s1[0] == "BTC":
                    pair = [str(d["pair"]), str(b["pair"]), s2[0] + ":" + s1[1]]
                else:
                    pair = [str(d["pair"]), str(b["pair"]), s2[1] + ":" + s1[1]]

                pairs.append(pair)

    print("Создано пар c USD/EUR: " + str(len(pairs)))


def CalculateRate():
    # print(len(allTikers))
    # print(len(eurTikers))
    try:

        for p in pairs:

            pr1ask = 0
            pr1bid = 0
            pr2ask = 0
            pr2bid = 0
            pr3ask = 0
            pr3bid = 0

            #p=str(pr).split(",")
            #print(str(p[0]))

            for t in allTikers:
                if str(t["pair"]).__contains__(p[0]):
                    pr1ask = float(t["ask"])
                    pr1bid = float(t["bid"])
                if str(t["pair"]).__contains__(p[1]):
                    pr2ask = float(t["ask"])
                    pr2bid = float(t["bid"])
                if str(t["pair"]).__contains__(p[2]):
                    pr3ask = float(t["ask"])
                    pr3bid = float(t["bid"])

                if pr1ask != 0.0 and pr2ask != 0.0 and pr3bid != 0.0:
                    percent = (((invest / pr1ask) * pr2ask * pr3bid - invest) / invest) * 100

                    #print(str.format("{0} Расчетная доходность [{1};{2};{3}] равна {4}",
                    #                 datetime.datetime.now(), p[0], p[1], p[2], format(percent, ".3f")))

                    if percent > 1.2:
                        print(str.format("{0} Расчетная доходность [{1};{2};{3}] равна {4}",
                                         datetime.datetime.now(), p[0], p[1], p[2], format(percent, ".3f")))

                        try:
                            txt = str.format("Date: {0}; Sec: {1}_{2}_{3}; ", datetime.datetime.now(), p[0], p[1], p[2])
                            txt1 = str.format("{0}_ask: {1}; {0}_bid:{2}; ", p[0], pr1ask, pr1bid)
                            txt2 = str.format("{0}_ask: {1}; {0}_bid:{2}; ", p[1], pr2ask, pr2bid)
                            txt3 = str.format("{0}_ask: {1}; {0}_bid:{2}", p[2], pr3ask, pr3bid)

                            with open("CexIoLog.txt", "a") as fl:
                                fl.write(txt+txt1+txt2+txt3 + "\n")
                        except:
                            print("error print to file")

                        pr1ask = 0
                        pr1bid = 0
                        pr2ask = 0
                        pr2bid = 0
                        pr3ask = 0
                        pr3bid = 0

    except:
        print(str.format("{0} error", datetime.datetime.now()))


        # res = filter(lambda x: p[0] in x, allTikers[])
        # print(str(res))
    # print()


def main():
    print(datetime.datetime.now())
    open("CexIoLog.txt", "w")

    GetAllTickers()
    CreatePairs()

    # print(datetime.datetime.now())
    # CalculateRate()

    while True:
        CalculateRate()
        time.sleep(1)


if __name__ == '__main__':
    main()
    pass
