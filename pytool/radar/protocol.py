#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date	  : 2017-12-21 20:22:27
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link	  : http://blog.csdn.net/enjoyyl
# @Version   : $1.0$

import struct
import pytool

SOF = 0x00
FRAMETYPE = 0x02
DEVID = 0x03
WORKMODE = 0x04
DATATYPE = 0x06
SOS = 0x08
EOS = 0x0A
DATALEN = 0x0E
DATALOAD = 0x10

UPDT_RADARARGS = 0x01
UPDT_ORIGECHO = 0x02
UPDT_BGECHO = 0x03
UPDT_TGECHO = 0x04
UPDT_DECISION = 0x05
UPDT_DETESLTS = 0x06
UPDT_TGINFO = 0x07
UPDT_ANALYSIS = 0x08
UPDT_LFT = 0x18
UPDT_SYSCFG = 0x20
UPDT_ALGPRM = 0x21
UPDT_DEBUG = 0x22
UPDT_REGR = 0x23
UPDT_MSG = 0xAA

Frame = {
    'SOF': 0x00,
    'FRAMETYPE': 0x02,
    'DEVID': 0x03,
    'WORKMODE': 0x04,
    'DATATYPE': 0x06,
    'SOS': 0x08,
    'EOS': 0x0A,
    'DATALEN': 0x0E,
    'DATALOAD': 0x10,
    'EOF': 0,
}


def findfrm(RxData=None, dtype=None, SOF=None, EOF=None):

    if dtype is None:
        dtype = 'bytes'

    if dtype is 'bytes':
        if SOF is None:
            SOF = b'$$'
        if EOF is None:
            EOF = b'####'

    if dtype is 'str':
        # data = data.decode("utf-8") ## byte like --> string
        if SOF is None:
            SOF = '$$'
        if EOF is None:
            EOF = '####'

    # print("data type: ", dtype, "SOF: ", SOF, "EOF: ", EOF)
    print("unpacking ...")
    lenRXs = len(RxData)
    # print('lenRXs: ', lenRXs)

    s = 2

    try:
        idxHead = RxData.index(SOF)
        s = 3
    except:
        s = -1
        idxHead = -1
    try:
        idxTail = RxData.index(EOF)
        s = 3
    except:
        s = -1
        idxTail = -1

    return s, idxHead, idxTail


def unpack(data=None, dtype=None, endian='Little', SOF=None, EOF=None):

    if endian is 'Little':
        endian = '<'
    if endian is 'Big':
        endian = '>'

    Frame['SOF'] = data[0:2]
    Frame['FRAMETYPE'] = struct.unpack(endian + 'B', data[2:3])[0]
    Frame['DEVID'] = struct.unpack(endian + 'B', data[3:4])[0]
    Frame['WORKMODE'] = struct.unpack(endian + 'B', data[4:5])[0]
    Frame['DATATYPE'] = struct.unpack(endian + 'H', data[6:8])[0]
    Frame['SOS'] = struct.unpack(endian + 'H', data[8:10])[0]
    Frame['EOS'] = struct.unpack(endian + 'H', data[10:12])[0]
    Frame['DATALEN'] = struct.unpack(endian + 'H', data[14:16])[0]
    Frame['DATALOAD'] = data[16:-4]
    Frame['EOF'] = data[-4:]

    return Frame


def parsing(Frame=None, endian='Little', SOF=None, EOF=None):

    if endian is 'Little':
        endian = '<'
    if endian is 'Big':
        endian = '>'
    # print(type(Frame['DATALOAD'][16:-5]), "=====================")
    # print(Frame['DATATYPE'], type(Frame['DATALOAD'][0:1]))
    # print('========= %s.' % Frame['DATALOAD'][0:1])
    data = []

    if Frame['DATATYPE'] is UPDT_ORIGECHO:
        adcmod = struct.unpack(endian + 'B', Frame['DATALOAD'][0:1])[0]
        for i in range(0, Frame['DATALEN']-1, 2):
        	# print(i, Frame['DATALEN'])
            # data.append(struct.unpack(endian + 'H', Frame['DATALOAD'][i+1:i+3])[0])
        	data.append(struct.unpack(endian + 'h', Frame['DATALOAD'][i+1:i+3])[0])
        if adcmod is 0x13:
            data = pytool.adcdata(
                data=data, mod='IQVIQV', verbose=False)
        if adcmod is 0x03:
            # print(adcmod)
            data = pytool.adcdata(
                data=data, mod='IQIQ', verbose=False)
    return data, adcmod