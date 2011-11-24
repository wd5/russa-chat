          # -*- coding: utf-8 -*-
from os import path as op
import os

ROOT = op.normpath(op.dirname(__file__))
dir = '/Users/vladimir/PycharmProjects/my-chat2/static/smiles'
for root, dirs, files in os.walk(dir):
    my_string = str()
    for name in files:
        print '\'' + ':' + name[:-4] + ':' + '\'' + " : " + '\'<img src=' + "\\" + '\'/static/smiles/standart/' + name + '\\' + '\'' + '/>' + '\'' + ','

        my_string +=':' + name[:-4] +':' + "|"
