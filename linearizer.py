import matplotlib.pyplot as plt

import os
from os import listdir
from os.path import isfile, join



delta_r = 3.05 * 10**6



def decrypt(inp):
    out = [0, 0, 0]

    for ind in range(3):
        out[ind] = 0
        out[ind] += (ord(inp[ind * 2 + 0]) - 65) * 32
        out[ind] += (ord(inp[ind * 2 + 1]) - 65) * 1

    return out

def getrplist(inp):
    out = []

    session = [[], [], []]
    for elm in inp:
        try:
            point = decrypt(elm)

            session[0].append(point[0])
            session[1].append(point[1])
            session[2].append(point[2])

        except Exception:
            if(elm == '-'):
                out.append(session)
                session = [[], [], []]

    return out

def average(inp):
    out = []
    
    for session in inp:
        out.append([
            sum(session[0]) / len(session[0]),
            sum(session[1]) / len(session[1]),
            sum(session[2]) / len(session[2])
            ])

    return out

def getvalues(plist, R):
    vlist = []
    ilist = []

    for session in plist:
        vlist.append((session[1] - session[2]) * 5000/1024)
        ilist.append((session[0] - session[1]) * 5000/1024 / R * 1000)

    return vlist, ilist

def transform(inp):
    name = inp.split('.')[0]

    name = name.replace(';', '\n')

    return name

def lsm(xlist, ylist):
    n = len(xlist)

    sumx2 = 0
    sumxy = 0
    sumx = 0
    sumy = 0
    for ind in range(n):
        sumx2 += xlist[ind] ** 2
        sumxy += xlist[ind] * ylist[ind]
        sumx += xlist[ind]
        sumy += ylist[ind]

    a = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx ** 2)
    b = (sumy - a * sumx) / n
    return a, b



files = [f for f in listdir(os.curdir) if isfile(join(os.curdir, f))]
for input_file in files:
    try:
        if(input_file.split('.')[1] != 'txt'):
            continue
        
        input_data = open(input_file, 'r').read()
        input_list = input_data.split('\n')

        rawplist = getrplist(input_list)

        plist = average(rawplist)

        r = float(input_file.split('`')[0].replace(',', '.')) * 1000
        R = delta_r * r / (delta_r + r)
        vlist, ilist = getvalues(plist, R)

        a, b = lsm(vlist, ilist)
        print('    I = a * V + b')
        print('    I - current, V - voltage')
        print('    a = ' + str(a * 10**-3) + ' A/V')
        print('    b = ' + str(b * 10**-6) + ' A')

        plt.plot(vlist, ilist, 'o', color='blue')
        plt.plot([0, max(vlist)], [b, b + a * max(vlist)], color='orange')
        plt.title(transform(input_file))
        plt.xlabel('voltage, millivolts')
        plt.ylabel('current, microamps')
        plt.show()

    except Exception:
        pass
