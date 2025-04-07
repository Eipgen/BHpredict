import numpy as np
T=np.loadtxt("result_83.txt")
FBH,RBH,RE=[],[],[]
for i in range(0,len(T),3):
    name=T[i:i+3]
    ForBH,RevBH,Re=[],[],[]
    for j in range(15):
        ForBH.append(name[:,j][2]-name[:,j][0])
        RevBH.append(name[:,j][2]-name[:,j][1])
        Re.append(name[:,j][1]-name[:,j][0])
    FBH.append(ForBH)
    RBH.append(RevBH)
    RE.append(Re)

FBH=np.array(FBH)*627.51
RBH=np.array(RBH)*627.51
RE=np.array(RE)*627.51

print("reaction number ",RE.shape[0])
namelist=["CCSD(T)-f12a","B3LYP-D3","M06-2X","MN15","MN15-L","wB97M-V","WB97X-D3","WB97X-V","XYG3","XYGJ-OS","DeePHF@HF(G&T)","DeeP@PBE(G@T)","DeePHF@B3LYP(G@T)","DeePHF@M062X(G@T)","DeePHF@wb97mv(G&T)"]

print("FBH_mae,FBH_rmse,RBH_mae,RBH_rmse,RE_mae,RE_rmse")
for i in range(1,15):
    FBH_mae=np.mean(np.abs(FBH[:,i]-FBH[:,0]))
    FBH_rmse=np.sqrt(np.mean(np.square(FBH[:,i]-FBH[:,0])))
    RBH_mae=np.mean(np.abs(RBH[:,i]-RBH[:,0]))
    RBH_rmse=np.sqrt(np.mean(np.square(RBH[:,i]-RBH[:,0])))
    RE_mae=np.mean(np.abs(RE[:,i]-RE[:,0]))
    RE_rmse=np.sqrt(np.mean(np.square(RE[:,i]-RE[:,0])))
    print(namelist[i],FBH_mae,FBH_rmse,RBH_mae,RBH_rmse,RE_mae,RE_rmse)
        

