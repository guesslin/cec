#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Check elctks.csv and elcand.csv data in each folder
# elctks sample
# 01,001,01,001,0000,0,01,469 ,5.57 ,
# 省市(2),縣市(3),選區(2),鄉鎮市區(3),村里別(4),投開票所(4),候選人號次(3),得票數(8),得票率(7,4),當選註記(1)
# 拿 0, 1, 2, 3, 4, 6
# elcand sample
# 01,001,01,001,0000,01,陳鴻源,1 ,1,042,99,  ,  ,Y, ,
# 省市(2),縣市(3),選區(2),鄉鎮市區(3),村里別(4),候選人號次(3),名字(80),政黨代號(3),性別(1),出生日期(7),年齡(3),出生地(10),學歷(10),現任(1),當選註記(1),副手(1)
# 拿 0, 1, 2, 3, 4, 5
#
# TODO:
# 給定資料夾 > 找到該資料夾底下 elcand\w+\.csv(後稱cand) 以及 elctks\w+\.csv(後稱ctks)
# > 從 cand 中建立 省市,縣市,選區,鄉鎮市區,村里別,候選人號次 之唯一編碼 cuid
# > 從 ctks 開票記錄比對是否在 cuid 有出現
# > 若 ctks 中有投票記錄之候選人，但未在 cand中出現，則輸出顯示整筆記錄，並記錄到主要記錄檔
# > 若 cand 中有參選記錄之候選人，但未在 ctks 中出現，則輸出至另一記錄檔
#
# 比對方法:
# 用 ctks 產生的 quid 作為查詢 cuid 的 prefix
#
# usage: ctks_check.py -h
#       -h, --help      print this help
#       -f, --folder    檢查的資料夾
#       -q, --quiet     僅顯示錯誤訊息


import argparse
import os


def get_files(path):
    l = os.listdir(path)
    r = {}
    for f in l:
        if 'elctks' in f:
            r['elctks'] = os.path.join(path, f)
        elif 'elcand' in f:
            r['elcand'] = os.path.join(path, f)
    return r


def elcand(filename):
    cuids = []
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            l = line.split(',')
            t = []
            t.append(int(l[0].strip()))  # 省市
            t.append(int(l[1].strip()))  # 縣市
            t.append(int(l[2].strip()))  # 選區
            t.append(int(l[3].strip()))  # 鄉鎮市區
            t.append(int(l[4].strip()))  # 村里別
            t.append(int(l[5].strip()))  # 選舉人號次
            if int(t[0])+int(t[1])+int(t[3])+int(t[4]) == 0:
                t[2] = 0
            cuids.append(t)
    return cuids


def elctks(filename):
    quids = []
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            l = line.split(',')
            t = []
            t.append(l[0].strip())  # 省市
            t.append(l[1].strip())  # 縣市
            t.append(l[2].strip())  # 選區
            t.append(l[3].strip())  # 鄉鎮市區
            t.append(l[4].strip())  # 村里別
            t.append(l[6].strip())  # 選舉人號次
            t.append(line.strip())
            quids.append(t)
    return quids


def exist_cand(cuids, quid):
    for cuid in cuids:
        flag = 0
        for i in xrange(len(cuid)):
            if cuid[i] == 0:
                flag += 1
                continue
            elif cuid[i] == int(quid[i]):
                flag += 1
            else:
                break
        if flag == 6:
            return True
    return False


def main(args):
    output = "ctks_logs.txt"
    if args.output:
        output = args.output
    if args.folder:
        print 'start checking', args.folder
        r = get_files(args.folder)
        cands = elcand(r['elcand'])
        tickets = elctks(r['elctks'])
        with open(output, 'a+') as fout:
            for quid in tickets:
                if not exist_cand(cands, quid):
                    print >>fout, args.folder, '-'.join(quid[:-1]), quid[-1].strip()
        print 'end of checking', args.folder
    else:
        print "no folder given"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="檢查的資料夾")
    parser.add_argument("-q", "--quiet", help="僅顯示錯誤訊息", action="store_true")
    parser.add_argument("-o", "--output", help="儲存異常結果")
    args = parser.parse_args()
    main(args)
