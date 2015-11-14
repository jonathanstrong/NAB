import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.style.use('ggplot')

class NABData(object):
    def __init__(self):
        self.data = {}
        prepath = ''
        if os.getcwd().split('/')[-1] == 'utils':
            prepath = '../'
        for root, _, files in os.walk(prepath + 'data'):
            for f in files:
                if f.endswith('.csv'):
                   self.data[os.path.splitext(f)[0]] = pd.read_csv(root + '/' + f, index_col = 0, sep = ',') 

    def keys(self):
        return self.data.keys()
    
    def plot(self, key):
        if type(key) != "str":
            key = self.keys()[key]
        self.data[key].plot()

