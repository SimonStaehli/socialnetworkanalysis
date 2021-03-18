import os
import glob
import pandas

def concatenate_rt(indir = "C:\\socialnetworkanalysis\\data", outfile = "C:\\socialnetworkanalysis\\transform\\rt_concatenated.csv"):
    os.chdir(indir)
    filelist = glob.glob("RT_*_2021-03-*.csv")
    dflist = []
    for filename in filelist:
        print(filename)
        df = pandas.read_csv(filename, header=True)
        dflist.append(df)
    concatdf = pandas.concat(dflist, axis=0)
    concatdf.to_csv(outfile, index=None)