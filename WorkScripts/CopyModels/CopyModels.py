import os.path
import errno
import shutil


def CopyModels(folderIn, folderOut):
    try:
        pattern = shutil.ignore_patterns("*.MSG", "*.INIT", "*.INSPEC", "*.UNSMRY", "*.UNRST", "*.err", "*.err", "*.smr", "*.SMSPEC", "*.EGRID", "*.ECLEND", "*.RSSPEC", "*.DBG", "*.log", "*.CFE")
        shutil.copytree(folderIn, folderOut, ignore=pattern)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(folderIn, folderOut)
        else:
            print('Directory not copied. Error: %s' % e)

    #print("Done.")


def main():
    folderOut = "D:\AdnocModels"
    cnt=1

    with open("models.txt") as f:
        lines = f.read().splitlines()

        for ln in lines:
            s = ln.replace("\t", " ").split(' ', -1)
            s1 = s[1].split('/',-1)
            s1_upd = ""

            for l1 in s1[:-1]:
                s1_upd = s1_upd + "\\" +l1

            fIn = "Y:\models." + s[0] + s1_upd

            CopyModels(fIn, folderOut + "\\" + str(cnt) + "_" + s1[-2])

            print("Model " + s1[-1])
            cnt+=1

    print("Done. Copied " + str(cnt) + " models.")

if __name__ == '__main__':
    main()
    pass