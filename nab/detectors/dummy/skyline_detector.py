from nab.detectors.base import AnomalyDetector

from nab.detectors.skyline.algorithms import (median_absolute_deviation,
                                              first_hour_average,
                                              stddev_from_average,
                                              stddev_from_moving_average,
                                              mean_subtraction_cumulation,
                                              least_squares,
                                              histogram_bins)



class DummyDetector(AnomalyDetector):

  def __init__(self, *args, **kwargs):

    # Initialize the parent
    super(SkylineDetector, self).__init__(*args, **kwargs)

    # Store our running history
    self.timeseries = []
    self.recordCount = 0
    self.algorithms =   [median_absolute_deviation,
                         first_hour_average,
                         stddev_from_average,
                         stddev_from_moving_average,
                         mean_subtraction_cumulation,
                         least_squares,
                         histogram_bins]


  def handleRecord(self, inputData):
    """
    Returns a list [anomalyScore].
    """
    import pdb; pdb.set_trace()

    score = 0.0
    inputRow = [inputData["timestamp"], inputData["value"]]
    self.timeseries.append(inputRow)
    for algo in self.algorithms:
      score += algo(self.timeseries)

    averageScore = score / len(self.algorithms)
    return [averageScore]
