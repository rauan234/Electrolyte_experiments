import matplotlib.pyplot as plt

import os
from os import listdir
from os.path import isfile, join



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

def display_processed(plist, name):
    a0 = []
    a1 = []
    a2 = []
    for session in plist:
        a0.append(session[0])
        a1.append(session[1])
        a2.append(session[2])
    n = list(range(len(plist)))

    print('A0 max: ' + str(max(a0)))
    print('A1 max: ' + str(max(a1)))
    print('A2 max: ' + str(max(a2)))

    plt.xlabel('number of measurement')
    plt.ylabel('potential, 5000/1024 millivolts')

    plt.plot(n, a0, 'o', color='b')
    plt.title(name + ' A0')
    plt.savefig(name + ' A0.png')
    plt.show()

    plt.plot(n, a1, 'o', color='b')
    plt.title(name + ' A1')
    plt.savefig(name + ' A1.png')
    plt.show()

    plt.plot(n, a2, 'o', color='b')
    plt.title(name + ' A2')
    plt.savefig(name + ' A2.png')
    plt.show()

def display_raw(plist, name):
    a0 = []
    a1 = []
    a2 = []
    for session in plist:
        a0 += session[0]
        a1 += session[1]
        a2 += session[2]

    n = list(range(len(plist) * len(plist[0][0])))
    n = list(map(lambda a: a / len(plist[0][0]), n))

    plt.xlabel('number of measurement')
    plt.ylabel('potential, 5000/1024 millivolts')

    plt.plot(n, a0, 'o', color='b')
    plt.title(name + ' A0')
    plt.savefig(name + ' A0.png')
    plt.show()

    plt.plot(n, a1, 'o', color='b')
    plt.title(name + ' A1')
    plt.savefig(name + ' A1.png')
    plt.show()

    plt.plot(n, a2, 'o', color='b')
    plt.title(name + ' A2')
    plt.savefig(name + ' A2.png')
    plt.show()

def transform(inp):
    name = inp.split('.')[0]

    name = name.replace(';', '\n')

    return name



files = [f for f in listdir(os.curdir) if isfile(join(os.curdir, f))]
for input_file in files:
    if(input_file.split('.')[1] != 'txt'):
        continue
    
    input_data = open(input_file, 'r').read()
    input_list = input_data.split('\n')

    rawplist = getrplist(input_list)

    display_raw(rawplist, transform(input_file) + ' raw ')

    plist = average(rawplist)

    display_processed(plist, transform(input_file) + ' procesed ')
