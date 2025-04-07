import os
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--txt", type=str, help="outputfile path,like mn15.txt")
args = parser.parse_args()

G=open(args.txt).readlines()
CHNO=open("CHNO.raw").readlines()
G0=[]
for h in G:
    num=h.strip().split()
    for i in CHNO:
        if num[0]==i.strip():
            G0.append(num)
#print(len(G0))

reaction_list=[]

Data_Val = open("DatasetEval_kcal.csv").readlines()
for i in Data_Val:
    j=i.strip().split(",")
    ref=j[-1]
    stio_reaction=j[1:-1]
    stio=[int(stio_reaction[h]) for h in range(0,len(stio_reaction),2)]
    reaction=[stio_reaction[h] for h in range(1,len(stio_reaction),2)]
    energy_m=[]
    for i in reaction:
        for h in G0:
            if i==h[0]:
                energy_m.append([i,float(h[1])])
    if len(energy_m)==len(stio):
        energy_run=[]
        for h in range(len(stio)):
            energy_run.append(stio[h]*energy_m[h][1])
        reaction_list.append([j[0],j,sum(energy_run)*627.51,float(ref)])
        #print(j[0],sum(energy_run)*627.51,ref)
#print(reaction_list)
datasets=open("gmtk55_63.raw").readlines()

def mae(y_true,y_pred):
    S=[]
    for i in range(len(y_true)):
        S.append(abs(y_true[i]-y_pred[i]))
    return sum(S)/len(S)


TR=[]
TP=[]
TOt=[]
for h in datasets:
    name_list=[]
    RE=[]
    for i in reaction_list:
        if h.strip() in i[0]:
            name_list.append(i[2:])
            RE.append(i)
    if len(name_list)>0:
        HR=[]
        HP=[]
        for i in range(len(name_list)):
            #print(RE[i][2],RE[i][3],abs(RE[i][2]-RE[i][3]),RE[i][1][1:-1])
            TR.append(RE[i][3])
            TP.append(RE[i][2])
            TOt.append([RE[i][3],RE[i][2]])
            HR.append(RE[i][3])
            HP.append(RE[i][2])
        print(h.strip(),len(HP),mae(HR,HP),)

Tot=np.array(TOt)
print("without PX13 and INV24 ",len(TR))
print("  ")
print("number, mae,rmse")
print(len(TR),mae(TR,TP),np.sqrt(np.mean(np.square(Tot[:,0]-Tot[:,1]))))
