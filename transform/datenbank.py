import os
import glob
import pandas as pd

def rt_concatenate():
    os.chdir('../data')
    file_list = glob.glob("RT_*.csv")
    df_from_each_file = (pd.read_csv(file, sep=',', header=0) for file in file_list)
    df_merged = pd.concat(df_from_each_file, ignore_index=True, sort=False)
    df_merged.to_csv("Merged_RT.csv")

def tw_concatenate():
    os.chdir('../data')
    file_list = glob.glob("TW_*.csv")
    df_from_each_file = (pd.read_csv(file, sep=',', header=0) for file in file_list)
    df_merged = pd.concat(df_from_each_file, ignore_index=True, sort=False)
    df_merged.to_csv("Merged_TW.csv")

if __name__ == '__main__':
    rt_concatenate()
    tw_concatenate()