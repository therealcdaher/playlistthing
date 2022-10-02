from concurrent.futures import ThreadPoolExecutor
import os,shutil,json,hashlib,re

# Produce hex md5 string for given filename; if nothing is found, return empty hash
def getHash(filename):
    fhash = hashlib.md5()
    try:
        with open(filename,"rb") as mfile:
            for chunk in iter(lambda: mfile.read(4096), b""):
                fhash.update(chunk)
    except:
        pass
    return fhash.hexdigest()

# Convert playlist to new format
def convert(file):
    with open("data.json","r") as configfile:
        config = json.load(configfile)
        basePath = config["musicsource"]
        destDirectory = config["playlistdest"]
        newPath = config["musicdest"]

    with open(file, "r", encoding="utf-8-sig") as plfile, open(os.path.join(destDirectory, os.path.basename(file)), "w", encoding="utf-8-sig") as destfile:
        destfile.write("#EXTM3U\n")
        musicfiles = [i for i in plfile if i != "#EXTM3U\n"]
        for i in musicfiles:
            destfile.write(i.replace(basePath, newPath).replace("\\", "/"))
        plfile.close()
        destfile.close()
    
    print("Conversion complete")

# Copy music files to new destination
def copy(file):
    print(file)

    with open("data.json","r") as configfile:
        config = json.load(configfile)
        destDirectory = config["musicdest"]
        basePath = config["musicsource"]

    with open(file, "r", encoding="utf-8-sig") as plfile:
        musicfiles = [i.rstrip() for i in plfile if i[0] != "#"]
        filecount = 1
        for i in musicfiles:
            fhash = getHash(i)
            subdir = os.path.relpath(i, basePath)
            filepath = os.path.join(destDirectory, subdir)
            dir = os.path.dirname(filepath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            try:
                dhash = getHash(filepath)
                tries = 0
                if dhash == fhash:
                    print("File " + filepath + " already exists (" + str(filecount) + " of " + str(len(musicfiles)) + ")")
                while fhash != dhash and tries < 6:
                    tries += 1
                    print("Copying " + i + " to " + filepath + " (" + str(filecount) + " of " + str(len(musicfiles)) + ")")
                    shutil.copyfile(i, filepath)
                    dhash = getHash(filepath)
                    if fhash != dhash:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        if tries < 6:
                            print("Hash verification failed; recopying")
                        else:
                            print("File " + i + " failed to verify five times; aborting")
                    else:
                        print("Hash verify success")
            except Exception as e:
                print(e)
            filecount += 1
    print("Copy complete")