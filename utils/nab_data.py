import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import json
import statsmodels
from collections import OrderedDict

matplotlib.style.use('ggplot')

class NABData(object):
    data_dir = os.path.join(os.path.dirname(os.path.abspath('.')), 'data')

    def __init__(self):            
        # Get time series data and store it in a dictionary
        self.data = OrderedDict() # keep the order the same for integer-based access
        for root, _, files in os.walk(self.data_dir):
            for f in files:
                if f.endswith('.csv'):
                   self.data[os.path.splitext(f)[0]] = pd.read_csv(root + '/' + f, index_col = 0, sep = ',') 
        # Turn indices into datetime objects
        for k in self.data:
            self.data[k].index = pd.to_datetime(self.data[k].index)
            
        # Get anomaly labels
        self.labels = {}
        with open(os.path.join(self.data_dir, '../labels/combined_windows.json')) as data_file:    
            js = json.load(data_file)
            for k,v in js.iteritems():
                key = k.split('/')[1].split('.')[0]
                self.labels[key] = []
                for anomalies in v:
                    start = pd.to_datetime(anomalies[0])
                    end = pd.to_datetime(anomalies[1])
                    self.labels[key].append([start, end])

    def _get_key(self, key):
        if type(key) == int:
            return self.data.keys()[key]
        return key


    def __getitem__(self, key):
        return self.data[self._get_key(key)]
    
    def plot(self, key, plot_anomalies = True, figsize=(10, 8)):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        key = self._get_key(key) # to get the string key for labels, title
        self[key].plot(color = 'b', ax=ax)
        if plot_anomalies:
            for anomalies in self.labels[key]:
                ax.axvspan(anomalies[0], anomalies[1], alpha=0.5, facecolor='red')
        ax.set_title(key)
        plt.show()
