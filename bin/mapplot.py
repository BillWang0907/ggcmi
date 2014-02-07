#!/usr/bin/env python

# import modules
import re, matplotlib
from os.path import split
import matplotlib.pyplot as plt
from netCDF4 import Dataset as nc
from optparse import OptionParser
from mpl_toolkits.basemap import Basemap
from numpy import logical_and, arange, meshgrid, double

parser = OptionParser()
parser.add_option("-i", "--input", dest = "input", default = "", type = "string",
                  help = "Input rescaled netCDF4 file", metavar = "FILE")
parser.add_option("-t", "--time", dest = "time", default = "", type = "string",
                  help = "Time to plot ('all' = all years)")
parser.add_option("-s", "--scen", dest = "scen", default = "", type = "string",
                  help = "Scenario to plot")
parser.add_option("-r", "--irr", dest = "irr", default = "", type = "string",
                  help = "Irrigation to plot")
parser.add_option("-v", "--var", dest = "var", default = "", type = "string",
                  help = "Variable to plot")
parser.add_option("-l", "--limits", dest = "limits", default = "", type = "string",
                  help = "Plot limits")
parser.add_option("-o", "--output", dest = "output", default = "", type = "string",
                  help = "Output filename", metavar = "FILE")
options, args = parser.parse_args()

crop = split(options.input)[1].split('_')[3]

with nc(options.input) as f:
    lat = f.variables['lat'][:]
    lon = f.variables['lon'][:]
    scen = f.variables['scen'].long_name.split(', ')
    irr = f.variables['irr'].long_name.split(', ')
    time = f.variables['time'][:]
    tunits = f.variables['time'].units
    var = f.variables[options.var + '_' + crop][:]
    varunits = f.variables[options.var + '_' + crop].units

scen_idx = scen.index(options.scen)
irr_idx = irr.index(options.irr)
var = var[:, :, :, scen_idx, irr_idx]

time += int(re.findall(r'\d+', tunits)[0])

if options.time == 'all':
    var = var.mean(axis = 0)
    years_str = years = str(time[0]) + '-' + str(time[-1])
else:
    y = options.time.split('-')
    if len(y) == 1:
        var = var[time == int(y[0])].mean(axis = 0)
        years_str = y[0]
    elif len(y) == 2:
        tidx = logical_and(time >= int(y[0]), time <= int(y[1]))
        var = var[tidx].mean(axis = 0)
        years_str = str(time[tidx][0]) + '-' + str(time[tidx][-1])
    else:
        raise Exception('Unrecognized -t option')

# get plot limits
if options.limits != '':
    pmin, pmax = [double(l) for l in options.limits.split(',')]
else:
    pmin = var.min()
    pmax = var.max()

# plot
m = Basemap(llcrnrlon = -180, llcrnrlat = -90, urcrnrlon = 180, urcrnrlat = 90, \
            resolution = 'c', projection = 'cyl')
lons, lats = meshgrid(lon, lat)
x, y = m(lons, lats)
cs = m.pcolor(x, y, var, vmin = pmin, vmax = pmax, cmap = matplotlib.cm.RdBu)
cbar = m.colorbar(cs, location = 'right')
m.drawcoastlines(zorder = 10)
m.drawstates()
m.drawmapboundary()
m.drawcountries(zorder = 10)
m.drawparallels(arange(90, -110, -30), labels = [1, 0, 0, 0])
m.drawmeridians(arange(-180, 180, 60), labels = [0, 0, 0, 1])
plt.title(options.var + ' (' + varunits + '), ' + years_str)

# save
plt.savefig(options.output)
plt.close()