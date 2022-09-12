import os
import filecmp
import shutil
import sys
import time


def synch(source , replica):
    comparison = filecmp.dircmp(source,replica)
    if comparison.common_dirs:
        for i in comparison.common_dirs:
           synch(os.path.join(source,i), os.path.join(replica,i))
    if comparison.left_only:
        copyFun(comparison.left_only,source,replica,'creation')
    if comparison.right_only:
        for i in comparison.right_only:
            path = os.path.join(source,os.path.basename(i))
            if os.path.isdir(path):
                shutil.rmtree(os.path.join(replica,i))
                f.write('Folder Removed from Replica: '+ os.path.basename(i) + "\n")
                print('Folder Removed from Replica: ',os.path.basename(i))
            else:
                os.remove(os.path.join(replica,i))
                f.write('File Removed from Replica: ' + os.path.basename(i) + "\n")
                print('File Removed from Replica: ' ,os.path.basename(i))
    if comparison.diff_files:
        copyFun(comparison.diff_files,source,replica,'update')



def copyFun(list,source,replica,type):
    for i in list:
        path = os.path.join(source, os.path.basename(i))
        if os.path.isdir(path):
            shutil.copytree(path,os.path.join(replica,os.path.basename(i)))
            if type == 'creation':
                f.write('Folder Created in Replica: ' + os.path.basename(path) + "\n")
                print('Folder Created in Replica: ',os.path.basename(path))
            else:
                f.write('Folder Updated in Replica: ' + os.path.basename(path) + "\n")
                print ('Folder Updated in Replica: ',os.path.basename(path))
        else:
            shutil.copy2(path,replica)
            if type == 'creation':
                f.write('File Created in Replica:' + os.path.basename(path) + "\n")
                print('File Created in Replica:',os.path.basename(path))
            else:
                f.write('File Updated in Replica:' + os.path.basename(path) + "\n")
                print ('File Updated in Replica:',os.path.basename(path))



if __name__ == '__main__':

    sourceFolder = sys.argv[1]
    replicaFolder = sys.argv[2]
    interval = int(sys.argv[3])
    logFile = sys.argv[4]

    f = open(logFile, 'x')
    f.write('This is the LOG FILE:\n')


    while True:
        f.write('Synch Began\n')
        synch(sourceFolder, replicaFolder)
        f.write('Synch Ended\n')
        time.sleep(interval)




