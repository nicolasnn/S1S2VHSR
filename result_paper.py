import glob
import pandas as pd
import numpy as np

# sensor = [,"S2"]

sensor = ["S1"]
sensor = ["Spot","S2","S1"]
sensor = ["S2","S1"]

sensor = ["S1","S2","Spot","S1-S2","S2-Spot","S1-S2-Spot"]

site = ["dordogne","reunion"]

JEacc = {"Spot" : { "dordogne": {"acc_mean" : 81.39, "acc_std" : 2.62}, "reunion" : {"acc_mean" : 88.35, "acc_std" : 1.33}}, 
         "S2" : { "dordogne": {"acc_mean" : 85.97, "acc_std" :  2.15}, "reunion" : {"acc_mean" : 88.09, "acc_std" : 1.06}}, 
         "S1" : { "dordogne": {"acc_mean" : 80.73, "acc_std" :  2.21}, "reunion" : {"acc_mean" : 73.39, "acc_std" : 2.66}},
         "S1-S2": { "dordogne": {"acc_mean" : 87.33, "acc_std" :  1.78}, "reunion" : {"acc_mean" : 92.05, "acc_std" : 0.30}},
         "S1-S2-Spot":{ "dordogne": {"acc_mean" : 87.48, "acc_std" :  1.68}, "reunion" : {"acc_mean" : 92.59, "acc_std" : 0.50}},
         "S2-Spot":{ "dordogne": {"acc_mean" : 88.56, "acc_std" :  1.62}, "reunion" : {"acc_mean" : 93.12, "acc_std" : 1.16}}}

dfi = pd.DataFrame(columns=["Sensor","Acc_Py","Acc_TF","std_Acc_Py","std_Acc_TF"])

for si in site:
    for s in sensor:
        print(s)
        acc_all = []
        list_csv = glob.glob(f"test_*_{s}_site-data_{si}*.csv")
           
        if len(list_csv) != 1:
            print("too many csv")
            breakpoint()
        else:
            print(list_csv[0])
            df = pd.read_csv(list_csv[0])
            acc_all = df["test_acc"].values.mean()
            std_all = df["test_acc"].values.std()

        if std_all>0.035:
            breakpoint()
            print(f"carefull high variation between repetition for site {si} sensor {s} split ")
        
        new_row = {"Dataset": si,"Sensor": s, "Acc_Py": acc_all*100, "Acc_TF": JEacc[s][si]["acc_mean"], "std_Acc_Py": std_all*100, "std_Acc_TF": JEacc[s][si]["acc_std"]}
        dfi = dfi.append(new_row, ignore_index=True)
print(dfi)
dfi.to_csv(path_or_buf="GlobalComparaison_Py_TF.csv",index=False)
dfi.to_csv(path_or_buf="GlobalComparaison_Py_TF.csv",index=False)
breakpoint()
print(dfi.to_latex(index=False,bold_rows=True,float_format="%.2f"))
