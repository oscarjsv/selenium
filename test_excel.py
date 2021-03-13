import pandas as pd

def route(route):
    df= pd.read_excel(route)
    dictionary = df.to_dict()
    for k in dictionary.values():
        for i in k.values():
            values_name = [i]
            print(values_name)
            

if __name__ == '__main__':
    rou = route("/home/oscar/Documents/selenium/selenium/excel.xlsx")