#from scipy import interpolate
import numpy as np
from scipy.interpolate import griddata
from scipy import interpolate

#feed_gas = [3000, 1400, 1190, 1000, 980, 840, 756, 755, 754, 700, 595, 500, 490, 420, 378, 0]
#extra_fuel=[0, 0, 11, 21, 21, 24, 24, 4, 0, 5, 11, 15, 15, 15, 15, 15]

#new_extra_fuel = interpolate.interp1d(feed_gas, extra_fuel, kind='previous') #possibly you need to use kind='nearest' instead

#print(new_extra_fuel(1700))

points = np.array([
    [13.83, 16.21, 19.76, 27.84, 40.07, 50.80, 71.48, 95.18],
    [12.18, 14.31, 17.80, 25.92, 38.11, 48.84, 69.79, 93.84],
    [14.30, 15.84, 18.50, 25.28, 36.29, 46.85, 67.86, 92.14],
    [18.15, 19.30, 21.32, 26.90, 37.28, 46.95, 67.03, 91.12],
    [22.59, 23.51, 25.15, 29.83, 39.10, 48.36, 67.54, 90.89],
    [27.20, 27.98, 29.35, 33.37, 41.56, 49.76, 68.48, 91.50],
    [31.84, 32.54, 33.75, 37.31, 44.53, 52.41, 69.81, 92.22],
    [36.53, 37.15, 38.24, 41.44, 47.99, 55.20, 71.86, 93.18],
    [41.20, 41.76, 42.71, 45.59, 51.65, 58.40, 74.08, 94.76],
    [45.87, 46.35, 47.25, 49.88, 55.45, 61.79, 76.71, 96.60],
    [50.51, 50.96, 51.77, 54.19, 59.39, 65.28, 79.51, 98.78],
    [51.68, 52.11, 52.90, 55.27, 60.38, 66.17, 80.23, 99.34],
    [51.68, 52.11, 52.90, 55.27, 60.38, 66.17, 80.23, 99.34]])


grid_x = np.array([10.0, 12.0, 15.0, 22.0, 33.0, 43.0, 63.0, 86.5])
grid_y = np.array([50.0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1025, 1100])

func = interpolate.interp2d(grid_x, grid_y, points, kind='linear')

znew = func(33.0, 250)

print(znew[0])


