import fitz
import pandas as pd
import numpy as np
from progress.bar import Bar

file1_name = input("Political Party Data (include .pdf at the end):")
file2_name = input("Purchaser Data (include .pdf at the end):")
file = fitz.open(file1_name)
data = []

def toInt(a: pd.Series):
    a = a.to_numpy()
    b = np.zeros((len(a)), dtype=int)
    c = 0
    for x in a:
        t = x.split(",")
        z = ""
        for x in t:
            z += x
        b[c] = int(z)
        c += 1
    return pd.Series(b)

def toDate(a: pd.Series):
    nr = []
    for x in a:
        t = x.split("/")
        month = {
            "Jan": '01',
            "Dec": '12',
            "Nov": "11",
            "Oct": "10",
            "Sep": "09",
            "Aug": "08",
            "Jul": "07",
            "Jun": "06",
            "May": "05",
            "Apr": "04",
            "Mar": "03",
            "Feb": "02"
        }
        m = month[t[1]]
        d = t[0]
        y = t[2]
        z = "-".join((y, m, d))
        nr.append(z)
    b = np.array(nr)
    # print(b)
    return pd.Series(b)

t = 0
with Bar(f'Processing {file1_name}...') as bar:
    for x in file.pages():
        if t % 5 == 0 and (t not in (0, 100, 200, 300, 400, 500, 150, 50, 150, 250, 350, 450)):
            bar.next()
        t += 1
        table = x.find_tables()[0]
        df = table.to_pandas()
        l = df['Denominations']
        m = df['Date of\nEncashment']
        b = toInt(l)
        c = toDate(m)
        df['Denominations'] = b
        df['Date of\nEncashment'] = c
        data.append(df)

final_data = pd.concat(data)
final_data.to_csv('./a.csv')

file = fitz.open(file2_name)
data = []
t = 0
with Bar(f'Processing {file2_name}...') as bar:
    for x in file.pages():
        if t % 4 == 0 or (t  in (0, 9, 27, 87)):
            bar.next()
        t += 1
        table = x.find_tables()[0]
        df = table.to_pandas()
        l = df['Denominations']
        m = df['Journal Date']
        o = df['Date of\nPurchase']
        p = df['Date of Expiry']
        b = toInt(l)
        c = toDate(m)
        d = toDate(o)


        e = toDate(p)
        df['Denominations'] = b
        df['Journal Date'] = c
        df['Date of\nPurchase'] = d
        df['Date of Expiry'] = e
        data.append(df)

final_data = pd.concat(data)
final_data.to_csv('./b.csv')



