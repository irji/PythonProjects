import pandas as pd

def main():
    input_data = pd.read_csv("input.txt", sep=",")

    #print(input_data)
    dates = input_data["Date"].unique()
    wells = input_data["Well"].unique()
    vectors = ["PMAX", "QWMAX", "QOSMAX", "QGSMAX", "PMIN", "QHCMAX"]

    #result

    print(dates)














if __name__ == '__main__':
    main()
    pass