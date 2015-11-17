import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.robust
matplotlib.style.use('ggplot')

class MovingWindow(object):
    def __init__(self, data, window = 100, step = 10, threshold = 5.0, norm = "l2"):
        self.data = data
        self.window = window
        self.step = step
        self.threshold = threshold
        # Determine the distance metric
        if norm == "l2": # L2 norm (Euclidean distance)
            self.distf = lambda x, y : np.sqrt(((x - y)**2.0).sum())
        elif norm == "l1": # L1 norm
            self.distf = lambda x, y : np.abs(x - y).sum()
            
    def _closest_norm(self, sample):
        min_dist = np.finfo(float).max
        # Search for minimum distance in past windows
        for i in range(0, len(self.data) - len(sample) - 1, self.step):
            dist = self.distf(self.data[i:i+self.window], sample)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def outliers(self):
        norms = []
        self.score = []
        self.outliers = []
        for i in range(self.window, len(self.data)):
            # Get value of closest norm of past windows
            minNorm = self._closest_norm(self.data[i-self.window:i])
            norms.append(minNorm)
            # MAD distance to the median, which can be interpreted as 
            # "robust standard deviation to the mean"
            distMADMedian = (minNorm - np.median(norms))/statsmodels.robust.scale.mad(norms)
            self.score.append(distMADMedian)
            self.outliers.append(distMADMedian > self.threshold)
        self.score = np.array(self.score)
        self.outliers = np.array(self.outliers)
        return self.outliers, self.score

    def plot(self, figsize= (10, 8)):
        plt.figure(figsize = figsize)
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        x = np.arange(self.window, len(self.data))
        ax1.plot(x, self.score, color = "blue", label = "Score")
        ax2.scatter(x[self.outliers], self.outliers[self.outliers], color = "red", label = "Outliers")
        ax2.set_ylim(0, 2)
        ax1.set_xlim(0, len(self.data))
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc=0)
        plt.show()                
