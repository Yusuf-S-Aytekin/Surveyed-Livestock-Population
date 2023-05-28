import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from mplcursors import cursor

#  link: https://ec.europa.eu/eurostat/web/agriculture/data/database?node_code=apro_mt_ls
#  Explanatory text of the database: https://ec.europa.eu/eurostat/cache/metadata/en/apro_anip_esms.htm#unit_measure1681892396594

df1 = pd.read_csv("apro_mt_lscatl.tsv")
df2 = pd.read_csv("apro_mt_lsgoat.tsv")
df3 = pd.read_csv("apro_mt_lspig.tsv")
df4 = pd.read_csv("apro_mt_lssheep.tsv")
#print(df1.columns) # Only 4 columns

lst=[]
c=-1
for df in [df1,df2,df3,df4]:
    for col in df.columns[3].split(): # The process of splitting the fourth column into a lot of columns
        c+=1
        for i in df.values:
            lst.append(list(i)[3].split("\t")[c]) # Split the values of the fourth column
        df[col]=lst # Match the splitted values with their columns
        lst=[]
    c=-1
    df.drop(columns=df.columns[3], inplace=True)
    df.replace(":",0,regex=True,inplace=True)
    df.replace("\s[a-z]","",regex=True,inplace=True)
    df.replace("\d[a-z]","",regex=True,inplace=True)
    df.iloc[:, 4:]=np.float64(df.iloc[:, 4:])/10**6
    df.drop(columns=df.columns[58:], inplace=True)
    for n in df.columns:
        df[n]=df[n].sum()
    df.drop(columns=df.columns[:4], inplace=True)
    df.drop(index=df.index[1:], inplace=True)

lstock=pd.merge(df1,df2,how="outer")
lstock=pd.merge(lstock, df3,how="outer")
lstock=pd.merge(lstock,df4,how="outer")
lstock.rename({0: "Bovine",1:"Goat",2:"Pig",3:"Sheep"}, axis=0,inplace=True)
lstock.columns=lstock.columns.astype(int)
lstock=lstock.T
lstock=lstock[::-1]

plt.style.use("fivethirtyeight")
 
def nplam1(sel):
    sel.annotation.set_text("Animal: {}\nYear: {}\nNumber of Livestock Animals: {:,}".format(
        lstock.columns[0],sel.target[0].astype(int),np.int64(sel.target[1]*1000000000)))
    sel.annotation.get_bbox_patch().set(fc="navy")
def nplam2(sel):
    sel.annotation.set_text("Animal: {}\nYear: {}\nNumber of Livestock Animals: {:,}".format(
        lstock.columns[1],sel.target[0].astype(int),np.int64(sel.target[1]*1000000000)))
    sel.annotation.get_bbox_patch().set(fc="greenyellow")
def nplam3(sel):
    sel.annotation.set_text("Animal: {}\nYear: {}\nNumber of Livestock Animals: {:,}".format(
        lstock.columns[2],sel.target[0].astype(int),np.int64(sel.target[1]*1000000000)))
    sel.annotation.get_bbox_patch().set(fc="violet")
def nplam4(sel):
    sel.annotation.set_text("Animal: {}\nYear: {}\nNumber of Livestock Animals: {:,}".format(
        lstock.columns[3],sel.target[0].astype(int),np.int64(sel.target[1]*1000000000)))
    sel.annotation.get_bbox_patch().set(fc="turquoise")

ax=lstock.plot(linestyle="--",color=["navy", "greenyellow", "violet","turquoise"], figsize=(14,7))

plt.gca().spines["right"].set_visible(False)
plt.gca().spines["top"].set_visible(False)
plt.xlabel("Year", color="dimgrey")
plt.ylabel("Number of Surveyed Livestoock Animals (x$10^9$ heads)", color="dimgrey")
plt.title("Surveyed Livestock Animals in Europe", color="dimgrey")

plt.ylim((0, lstock.values.max()+0.03))
plt.xlim((1969,2022))

plt.axvspan(2008,2010, hatch="/", color="rosybrown", alpha=0.5, label="H1N1 Pandemic") # o, x, ox, |, .
#plt.gca().spines["left"].set_position("center")

plt.legend()
np1=plt.scatter(lstock.index, lstock.iloc[:,0],alpha=0)
crs1=cursor(np1)
np2=plt.scatter(lstock.index, lstock.iloc[:,1],alpha=0)
crs2=cursor(np2)
np3=plt.scatter(lstock.index, lstock.iloc[:,2],alpha=0)
crs3=cursor(np3)
np4=plt.scatter(lstock.index, lstock.iloc[:,3],alpha=0)
crs4=cursor(np4)

crs1.connect("add", nplam1)
crs2.connect("add", nplam2)
crs3.connect("add", nplam3)
crs4.connect("add", nplam4)
plt.show()

