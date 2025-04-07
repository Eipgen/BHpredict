import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--txt", type=str, help="energy file")
args = parser.parse_args()

T=open(args.txt).readlines()
TSfile_raw=[]
for i in T:
    if "TS" in i:
        name=i.split()[0]
        energy=float(i.split()[-1])
        TSfile_raw.append([name,energy])

check_energy=[]
for i in TSfile_raw:
    Rname=i[0].split("TS")[0]+"R"
    Pname=i[0].split("TS")[0]+"P"
    R=[]
    P=[]
    for j in T:
        if Rname in j:
            R.append([j.split()[0],float(j.split()[-1])])
        if Pname in j:
            P.append([j.split()[0],float(j.split()[-1])])
    R1=[]
    P1=[]
    if len(R)>1 or len(R)==0:
        name="+".join([i[0] for i in R])
        value=sum([i[1] for i in R])
        R1.append([name,value])
    else:
        R1.append(R[0])
    if len(P)>1 or len(R)==0:
        name="+".join([i[0] for i in P])
        value=sum([i[1] for i in P])
        P1.append([name,value])
    else:
        P1.append(P[0])
    check_energy.append([i,R1[0],P1[0]])
    #print(i,R1[0],P1[0])

# filter

filter_reaction=[]
for j in check_energy:
    energy=[i[1] for i in j]
    if all(i != 0 for i in energy):
        if abs(energy[0]-energy[1])<0.5 and abs(energy[0]-energy[2])<0.5:
            #filter_reaction.append([j[1][0],j[2][0],j[0][0],energy[0],energy[1],energy[2]])
            filter_reaction.append([j[0][0],(energy[0]-energy[1])*627.51,(energy[0]-energy[2])*627.51,(energy[2]-energy[1])*627.51])
#print(filter_reaction)
            #print(j[1][0]+"->"+j[0][0]+"->"+j[2][0],energy[0]-energy[1],energy[0]-energy[2],energy[2]-energy[1])
energy_compare=[]
Ref=open("Reference.org").readlines()
H=[]
for h in Ref:
    h1=h.split("|")
    for h2 in filter_reaction:
        if h1[4].strip()+"TS"==h2[0]:
            if float(h1[5].strip()) >0 and float(h1[6].strip())>0:
                H.append([float(h1[5].strip()),float(h1[6].strip()),float(h1[7].strip()),h2[1],h2[2],h2[3]])
                energy_compare.append([h1[1]+h1[3],h1[4],h1[5].strip(),h1[6].strip(),h1[7].strip(),h2[0],h2[1],h2[2],h2[3]])


D_A=H[:35]
Cyd=H[35:47]+H[62:65]+H[66:72]
Elc=H[47:62]
intra=H[72:80]+[H[93]]
Rarrge=[H[65]]+H[80:93]
Ptransfer=H[94:]

def compare_mae_rmse(G):
    E=np.array(G)
    rmsd1=np.sqrt(np.mean(np.square(E[:,0]-E[:,3])))
    rmsd2=np.sqrt(np.mean(np.square(E[:,1]-E[:,4])))
    rmsd3=np.sqrt(np.mean(np.square(E[:,2]-E[:,5])))
    mae1=np.mean(np.abs(E[:,0]-E[:,3]))
    mae2=np.mean(np.abs(E[:,1]-E[:,4]))
    mae3=np.mean(np.abs(E[:,2]-E[:,5]))
    return (mae1+mae2)/2,mae3

H1=compare_mae_rmse(D_A)
H2=compare_mae_rmse(Cyd)
H3=compare_mae_rmse(Elc)
H4=compare_mae_rmse(intra)
H5=compare_mae_rmse(Rarrge)
H6=compare_mae_rmse(Ptransfer)
print("type:   Diels-Alder Cycloaddition Electrocyclic Intramolecular Rarrangement Proton-transfer")
print("number:",len(D_A),len(Cyd),len(Elc),len(intra),len(Rarrge),len(Ptransfer))
print("mae:   ",H1[0],H1[1],H2[0],H2[1],H3[0],H3[1],H4[0],H4[1],H5[0],H5[1],H6[0],H6[1])


