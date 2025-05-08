import numpy as np
import torch
from deepks.model import CorrNet
from deepks.utils import load_yaml
import argparse


parser = argparse.ArgumentParser("get DeePHF output energy")
parser.add_argument("--model",type=str, default="model.out/model.pth", help="path of model")
parser.add_argument("--raw",type=str, default="test.raw", help="path of dm_eig npydata raw")

args = parser.parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

""" if report `layer_norm` error, use below code"""
#model_dict=torch.load(args.model, map_location=device)
#if 'layer_norm' in model_dict['init_args']:
#        del model_dict['init_args']['layer_norm']
#model= CorrNet.load_dict(model_dict)

model = CorrNet.load_dict(torch.load(args.model, map_location=device))
elem_dict=model.elem_dict
B = np.array([[key, value] for key, value in elem_dict.items()])

model.eval()

data=open(args.raw).readlines()
for i in data:
    i=i.strip()
    #sample_feature = np.load(args.dir+"/dm_eig.npy")
    sample_feature = np.load(i+"/dm_eig.npy")
    sample_tensor = torch.from_numpy(sample_feature).float()
    with torch.no_grad():
        energy_correction = model(sample_tensor).item()
    atom=np.load(i+"/atom.npy")[0][:,0]
    atom_E=[]
    for at in atom:
        if at==1:
            atom_E.append(B[:,1][0])
        elif at==6:
            atom_E.append(B[:,1][1])
        elif at==7:
            atom_E.append(B[:,1][2])
        elif at==8:
            atom_E.append(B[:,1][3])
    base_energy = np.load(i+"/e_base.npy")[0][0]
    E_atom=sum(atom_E) ## sum of atomization energy
    print(i,base_energy+energy_correction+E_atom)

