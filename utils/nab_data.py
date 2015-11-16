import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import json
import statsmodels
from collections import OrderedDict
import natural.date, natural.number

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

    def _files_iter(self):
        for key in self.data.keys():
            yield key, self.data[key]
    
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

    def summary(self):
        "returns a DataFrame with statistics about each file"
        data = []
        cols = ['file', 'length', 'features', 'period', 'periods_vary', 'min', 
                'max', 'mean', 'std', '25th_percentile', '50th_percentile', '75th_percentile']
        for filename, df in self._files_iter():
            row = dict([('file', filename)])
            row['length'] = len(df)
            row['features'] = len(df.columns)
            row['period'] = natural.date.compress(df.index[1]-df.index[0])
            row['periods_vary'] = int(np.unique(np.diff(df.index)).shape == (1,))
            row['min'] = df['value'].min()
            row['max'] = df['value'].max()
            row['mean'] = df['value'].mean()
            row['std'] = df['value'].std()
            for q in [25, 50, 75]:
                row['{}_percentile'.format(natural.number.ordinal(q))] = np.percentile(df['value'], q)
            data.append(row)
        return self._round_float_cols(pd.DataFrame(data)[cols])

    @staticmethod
    def _round_float_cols(df, digits=2):
        "convenience method; was hard to digest summary table"
        for col in df.columns: 
            if df[col].dtype in [np.float64, np.float32]:
                df[col] = np.round(df[col], digits)
        return df
