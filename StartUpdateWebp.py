# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import xlwt
import time
import math
import traceback



'''
一级目录下所有子目录的轮询
e.g:参数是Client
即轮询 ApkUpdater等目录的资源

├── Client
│   ├── ApkUpdater
│   ├── DesktopBackup
│   ├── DLNAMediaRender
│   ├── Gslb
│   ├── Gslb_Volly
│   ├── Hybird
│   ├── InternetCommon
│   ├── Mall
│   ├── MultimediaPowerTest
│   ├── MzHealth
│   ├── MzPushSdk
│   ├── PushSdk-Open
│   ├── Pyxis
│   ├── RemoteCooperation
│   ├── SdkDynamicLoad
│   ├── SyncSdk
│   ├── VideoEditor
│   └── Weather_Intl
'''

def traversalDir(dir,size):
    if os.path.isdir(dir):
        lista =os.listdir(dir)
        lista.sort()
        print "dir:",lista
        for i in lista:
            print i
            if os.path.isdir(os.path.join(dir, i)):
                if len(os.listdir(os.path.join(dir, i))) == 1 and os.listdir(os.path.join(dir, i))[0].endswith(".git"):
                    print i+" is empty"
                    continue
                command = "python  "+ os.getcwd()+"/updateWebp.py "+ os.path.join(dir, i)+" "+size
                print "command:",command
                subprocess.call(command, shell=True)

'''
二级目录下所有子目录的轮询
e.g:参数是meizu
即轮询 ApkUpdater等目录的资源
├── meizu
│   ├── Client
│   │   ├── ApkUpdater
│   │   ├── DesktopBackup
│   │   ├── DLNAMediaRender
│   │   ├── Gslb
│   │   ├── Gslb_Volly
│   │   ├── Hybird
│   │   ├── InternetCommon
│   │   ├── Mall
│   │   ├── MultimediaPowerTest
│   │   ├── MzHealth
│   │   ├── MzPushSdk
│   │   ├── PushSdk-Open
│   │   ├── Pyxis
│   │   ├── RemoteCooperation
│   │   ├── SdkDynamicLoad
│   │   ├── SyncSdk
│   │   ├── VideoEditor
│   │   └── Weather_Intl
'''
def secTraversalDir(dir,size):
    if os.path.isdir(dir):
        lista =os.listdir(dir)
        lista.sort()
        print "dir:",lista
        for i in lista:
            if os.path.isdir(os.path.join(dir, i)):
                print "secDir:",os.path.join(dir, i)
                if i.endswith("Cloud"):
                    continue
                traversalDir(os.path.join(dir, i),size)
    else:
        print "have no the dir: "+dir



def unzip(path):
    """
    unzip apk
    :param path:
    :return:
    """
    apklist = os.listdir(path)
    for APK in apklist:
        zip_apk_path = os.path.join(path,APK)
        apkapklist = os.listdir(zip_apk_path)
        for zipapk in apkapklist:
            if zipapk[-4:] =='.apk' and not os.path.isdir(os.path.join(zip_apk_path,zipapk[:-4])):
                os.system('unzip ' +os.path.join(zip_apk_path,zipapk)+' -d'+' '+os.path.join(zip_apk_path,zipapk[:-4]))

if __name__ == '__main__':
    size = "50"
    if len(sys.argv) > 1:  # cp png/jpg/
        dir =sys.argv[1]
        if len(sys.argv) > 2:  # cp png/jpg/
            size =sys.argv[2]
    else:
        print "please input the dir of update or target "
        sys.exit(1)

    unzip(dir+r'/SYSTEM/app')
    unzip(dir+r'/SYSTEM/priv-app')
    reload(sys)
    sys.setdefaultencoding('utf8')

    secTraversalDir(dir+r'/system/app',size)
    secTraversalDir(dir+r'/system/priv-app',size)
    secTraversalDir(dir+r'/SYSTEM/app',size)
    secTraversalDir(dir+r'/SYSTEM/priv-app',size)
