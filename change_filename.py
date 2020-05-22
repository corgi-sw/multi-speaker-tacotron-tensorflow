import os
import argparse

def change1(path):
    for name in os.listdir(path):
        s = name.split(' ')[-1]
        ss = s.split('.')[0].zfill(4)

        os.rename(path +"/" + name, path + "/" + ss + '.wav')
        print(path + "/" + ss + '.wav')

def change2(path):
    l = sorted(os.listdir(path))
    for name in l:
        s = name.split('.')[1].zfill(4)
        n = int(s) - 1
        ss = str(n).zfill(4)

        os.rename(path + "/" + name, path + "/Raw." + ss + '.wav')
        print(path + "/" + name + "  " + path + "/Raw." + ss + '.wav')

def change3(path):
    l = sorted(os.listdir(path))
    for name in l:
        os.rename(path + "/" + name, path + "/Raw." + name)
        print(path + "/Raw." + name)

def change4(path):
    idx = 0
    l = sorted(os.listdir(path))
    for name in l:
        ss = str(idx).zfill(4)
        os.rename(path + "/" + name, path + "/Raw." + ss + '.wav')
        print(path + "/" + name + "  " + path + "/Raw." + ss + '.wav')
        idx += 1

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    config = parser.parse_args()
    
    change4(config.path)