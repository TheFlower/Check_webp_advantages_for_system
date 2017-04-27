# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import math
import traceback



global count
global table

'''
功能:
1.扫描目录,把所有的jpg and png图片按路径名命到output
2.使用cwebp工具将png and jpg转换为质量分别为50,75,95,lossless(100)的webp图片
3.获取每张图片运行时刻的decodebitmap time
4.将结果写入xls里.
'''


def getFileSize(size):
    """
    return the unit of size
    :param size: B
    :return:B or KB or MB
    """
    #传统除法
    # 1/2=0;
    # 1.0/2.0=0.5
    size = float(size)
    if math.fabs(size/1024)>1:
        if math.fabs(size/(1024*1024))>1:
            return '%6.2fMB' %float(size/(1024*1024))
        else:
            return '%6.2fKB' %float(size/1024)
    else:
        return '%6.2fB' %float(size)


def getTimeUnit(time):
    """
    return the unit of time
    :param time: ns
    :return:ns or us or ms or s
    """
    time = float(time)
    if math.fabs(time/1000)>1:
        if math.fabs(time/(1000*1000))>1:
            if math.fabs(time/(1000*1000*1000))>1:
                return '%5.2fs' %float(time/(1000*1000*1000))
            else:
                return '%5.2fms' %float(time/(1000*1000))
        else:
            return '%5.2fus' %float(time/1000)
    else:
        return '%5.2fns' %float(time)


def checkStrLen(str):
    """
    :param str:
    :return:
    """
    if len(str) > 87:
        # 91-4( 4 webp )
        return str[-87:]
    else:
        return str


def get_bitmap(soure_dir, output_dir):
    global size
    print "get_bitmap"
    if os.path.isdir(soure_dir):
        for dirpath, dirnames, files in os.walk(soure_dir):
            if (dirpath.startswith(output_dir)): continue
            # remove output_dir
            for f in files:
                if f.endswith('.png') or f.endswith('.jpg'):
                    if 6 < len(f) and f.endswith(".9.png"):
                        print "NinePatch:",f
                        continue
                    if os.path.getsize(os.path.join(dirpath, f)) < size:
                        print "the file less than default:",f,os.path.getsize(os.path.join(dirpath, f)),"   defaultSize:",size
                        continue
                    commandCp = "cp " + os.path.abspath(dirpath + '/' + f) + " " + output_dir
                    if len(dirpath) > len(soure_dir):
                        # Unified format for the first file name
                        strname = dirpath[len(soure_dir) + 1:].replace("/", "_") + "_" + f[0:(len(f) - 4)] + f[-4:]
                    else:
                        strname = f
                    commandRename = "mv " + os.path.abspath(output_dir + '/' + f) + " " + \
                                    os.path.abspath(output_dir + '/' + checkStrLen(strname))
                    commandall = commandCp + ";" + commandRename
                    subprocess.call(commandall, shell=True)
                    print "name:",f
        print "CP over"
    else:
        print "please input the soure dir"


def startWepy(output_dir, list_webp_dir):
    cwebp = "./cwebp"
    if(not os.path.isfile(cwebp)):
        cwebp = "cwebp"
    print "startWepy"
    if os.path.isdir(output_dir):
        for i in os.listdir(output_dir):
            if i[-4:] == ".png" or i[-4:] == ".jpg":
                print i, len(i)
                qList = ["50", "75", "95"]
                for q in qList:
                    print q, ":", list_webp_dir[qList.index(q)]
                    command = cwebp+" -m 6 -q " + q + " " + os.path.abspath(output_dir + '/' + i) + " -o " + \
                              os.path.abspath(list_webp_dir[qList.index(q)] + '/' +
                                              i[0:-4] + "_" + q + ".webp")
                    subprocess.call(command, shell=True)
                commandlossless = cwebp+" -m 6 -q 100 " + "-lossless" + " " + os.path.abspath(output_dir + '/' + i) \
                                  + " -o " + os.path.abspath(list_webp_dir[3] + '/' +
                                                             i[0:-4] + "_ll" + ".webp")
                subprocess.call(commandlossless, shell=True)
    else:
        print "please input the soure dir"


def sort(A, num):
    """
    Sort by size
    :param A: list whose Element is list
    :param num: the size number of Element
    :return:Ordered list by size
    """
    for i in range(len(A)):
        (A[i][0], A[i][num]) = (A[i][num], A[i][0])
    A.sort()
    A.reverse()
    for i in range(len(A)):
        (A[i][0], A[i][num]) = (A[i][num], A[i][0])



def getRatio(pngStr, webpStr):
    if float(pngStr) > 0:
        return round(float(webpStr) / float(pngStr),3)
    else:
        return -1


def getdirsize(dir):
    """
    return the size of dir.
    For example:
    the size of /home/text is 100 byte
    >>getdirsize(r'/home/text')
    100.0
    """
    filesize = 0
    if os.path.isdir(dir):
        for filename in os.listdir(dir):
            filesize += os.path.getsize(os.path.join(dir, filename))
    return filesize



def unzip(path):
    """
    unzip apk
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        return
    apklist = os.listdir(path)
    for APK in apklist:
        zip_apk_path = os.path.join(path,APK)
        apkapklist = os.listdir(zip_apk_path)
        for zipapk in apkapklist:
            if zipapk[-4:] =='.apk' and not os.path.isdir(os.path.join(zip_apk_path,zipapk[:-4])):
                os.system('unzip ' +os.path.join(zip_apk_path,zipapk)+' -d'+' '+os.path.join(zip_apk_path,zipapk[:-4]))


if __name__ == "__main__":
    global count
    global DATA_LIST

    global style0
    global table

    global sizeWeights

    global devices
    global size

    reload(sys)
    sys.setdefaultencoding('utf8')

    size = 50*1024

    devices = " "
    sizeWeights = 6
    count = 0

    output_dir = "./output"
    webp_dir_50 = "./webp_50"
    webp_dir_75 = "./webp_75"
    webp_dir_95 = "./webp_95"
    webp_dir_lossless = "./webp_lossless"
    list_webp_dir = [webp_dir_50, webp_dir_75, webp_dir_95, webp_dir_lossless]
    list_all_dir = [output_dir, webp_dir_50, webp_dir_75, webp_dir_95, webp_dir_lossless]

    for str in list_all_dir:
        print "rm "
        os.system("rm -rf %s" % str)
        os.system("mkdir %s" % str)

    if len(sys.argv) > 1:  # cp png/jpg/
        soure_dir = sys.argv[1]
        if len(sys.argv) > 2:
            size =float(sys.argv[2])*1024
        if len(sys.argv) > 3:
            devices = sys.argv[3]
    else:
        print "please input the soure dir and sizeWeights"
        sys.exit(1)

    apklist =[soure_dir+r'/system/app', soure_dir+r'/system/priv-app',soure_dir+r'/SYSTEM/app',soure_dir+r'/SYSTEM/priv-app']

    for dir in apklist:
        unzip(dir)
        get_bitmap(dir, output_dir)


    if len(os.listdir(output_dir)) == 0:
        print "the dir of "+soure_dir+ " have not png or jpg bitmap!"
        sys.exit(0)

    startWepy(output_dir, list_webp_dir)  # webp

    data_output = []
    data_webp_50 = []
    data_webp_75 = []
    data_webp_95 = []
    data_webp_lossless = []
    data_list_all = [data_output, data_webp_50, data_webp_75, data_webp_95, data_webp_lossless]

    for list in data_list_all:
        print "main:", list


    name = soure_dir.split("/")


    for webpStr in list_all_dir:
        print webpStr
        try:
            commandzip = "zip " +name[len(name)-1]+"_"+webpStr.split("./")[1]+".zip" + " -r "+webpStr
            subprocess.call(commandzip, shell=True)
        except Exception, e:
            print "zip hava a error"
            traceback.print_exc()

    pngsize = getdirsize(output_dir)
    print "the dir :"+soure_dir
    for webpStr in list_all_dir:
        print "the number of "+webpStr+":",len(os.listdir(webpStr)),\
            "   the size of "+webpStr+":",getFileSize(getdirsize(webpStr)),\
            "   the radio to png :",getRatio(pngsize,getdirsize(webpStr))


    print "zip over"

    print "all over"
