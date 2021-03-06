# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import xlwt
import time
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


def getFile(dir):
    """
    subfile and size of the dir
    :param dir:folder
    :return:list[file,size]
    """
    File_LIST = []
    print type(File_LIST)
    if os.path.isdir(dir):
        for i in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, i)):
                fileSize = os.path.getsize(os.path.join(dir, i))
                File_LIST.append([i, fileSize])
    return File_LIST


def switchQua(str):
    return {
        '50': "50",
        '75': "75",
        '95': "95",
        'll': "100",
    }.get(str, "default")


def switchComp(str):
    return {
        '50': "lossy",
        '75': "lossy",
        '95': "lossy",
        'll': "lossness",
    }.get(str, "default")


def getRatio(pngStr, webpStr):
    if float(pngStr) > 0:
        return round(float(webpStr) / float(pngStr),3)
    else:
        return -1

def writeStyle(count,num,ratio):
    global table
    global style0

    if 0 < ratio < 1:
        table.write(count, num, ratio, style0)
    else:
        table.write(count, num, ratio)

def writeAllToXls(data_list_all):
    global table
    global count
    global style0
    global sizeWeights

    listSum = [0,0,0,0,0]

    for datalist in data_list_all:
        sort(datalist, 1)

    for list in data_list_all:
        print "xls:", list

    for png_arr in data_list_all[0]:
        if (count < 60000):
            count += 1
            listSum[0] += png_arr[1]
            table.write(count, 0, png_arr[0][:-4])
            table.write(count, 1, png_arr[0][-3:])
            table.write(count, 5, getFileSize(png_arr[1]))
            table.write(count, 6, 1)
            for k in range(1, 5):
                for m in range(len(data_list_all[k])):
                    if png_arr[0][:-4] in data_list_all[k][m][0]:
                        if count < 60000:
                            count += 1
                            listSum[k] += data_list_all[k][m][1]
                            table.write(count, 0, data_list_all[k][m][0][:-5])
                            table.write(count, 1, "webp")
                            print data_list_all[k][m][0][-7:-5]
                            table.write(count, 2, switchComp(data_list_all[k][m][0][-7:-5]))
                            table.write(count, 3, switchQua(data_list_all[k][m][0][-7:-5]))
                            table.write(count, 4, "6")
                            table.write(count, 5, getFileSize(data_list_all[k][m][1]))
                            sizeRatio = getRatio(png_arr[1], data_list_all[k][m][1])
                            writeStyle(count,6,sizeRatio)
                            break

    table.write(1,7,getFileSize(listSum[0]))
    table.write(2,7,getFileSize(listSum[1]))
    table.write(3,7,getFileSize(listSum[2]))
    table.write(4,7,getFileSize(listSum[3]))
    table.write(5,7,getFileSize(listSum[4]))
    table.write(1,8,1)
    writeStyle(2,8,getRatio(listSum[0],listSum[1]))
    writeStyle(3,8,getRatio(listSum[0],listSum[2]))
    writeStyle(4,8,getRatio(listSum[0],listSum[3]))
    writeStyle(5,8,getRatio(listSum[0],listSum[4]))


def getDataList(output_dir, name, output_list):
    if os.path.isfile(os.path.join(output_dir, name)):
        fileSize = os.path.getsize(os.path.join(output_dir, name))
        output_list.append([name, float(fileSize)])



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

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    patterni = xlwt.Pattern()
    patterni.pattern = 1
    patterni.pattern_fore_colour = 27
    patterni.pattern_back_colour = 35
    style1.pattern = patterni

    file = xlwt.Workbook(encoding='utf-8')
    table = file.add_sheet('sheet1', cell_overwrite_ok=True)

    table.write(0, 0, 'name', style1)
    table.write(0, 1, 'type', style1)
    table.write(0, 2, 'compression', style1)
    table.write(0, 3, 'quality', style1)
    table.write(0, 4, 'method', style1)
    table.write(0, 5, 'size', style1)
    table.write(0, 6, 'size ratio', style1)
    table.write(0, 7, 'sizeSum', style1)
    table.write(0, 8, 'sizeSum ratio', style1)

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
        get_bitmap(soure_dir, output_dir)
    else:
        print "please input the soure dir and sizeWeights"
        sys.exit(1)

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

    for dir in list_all_dir:
        print dir, list_all_dir.index(dir), data_list_all[list_all_dir.index(dir)]
        for i in os.listdir(dir):
            getDataList(dir, i, data_list_all[list_all_dir.index(dir)])


    for list in data_list_all:
        print "main:", list
    try:
        writeAllToXls(data_list_all)
    except Exception, e:
        print "writeAllToXls hava a error"
        traceback.print_exc()
    name = soure_dir.split("/")
    try:
        file.save("webp_"+name[len(name)-1]+".xls")
    except Exception, e:
        print "save Xls hava a error"
        traceback.print_exc()
    print "save xls over"


    print "the number of bitmap needed to webp:",len(os.listdir(output_dir))

    for webpStr in list_all_dir:
        print webpStr
        try:
            commandzip = "zip " +name[len(name)-1]+"_"+webpStr.split("./")[1]+".zip" + " -r "+webpStr
            subprocess.call(commandzip, shell=True)
        except Exception, e:
            print "zip hava a error"
            traceback.print_exc()

    print "zip over"

    print "all over"
