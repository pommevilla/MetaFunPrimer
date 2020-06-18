#!/usr/bin/python

import sys
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

f = open(sys.argv[1], 'r')
coverage_map = dict()
richness_map = dict()
for line in f:
    data_list = line.split()
    coverage_map[int(data_list[0])] = float(data_list[1]) * 100
    richness_map[int(data_list[0])] = float(data_list[2])

width = int(sys.argv[3])
height = int(sys.argv[4])
dpiVal = int(sys.argv[5])

plt.figure(figsize=(width,height))
ax = plt.subplot(2, 1, 1)
plt.title('Coverage')
plt.xlabel('Position in the Alignment')
plt.ylabel('Proportional')
plt.ylim(0,100)
fmt = '%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(yticks)
coverage = coverage_map.values()
max_coverage = max(coverage)
if max_coverage == 0:
    max_coverage = 1
fracs = [data/max_coverage for data in coverage]
jet = plt.get_cmap('jet')
plt.bar(range(len(coverage_map)), coverage, width=1, color=jet(fracs), linewidth=0.5)

plt.subplots_adjust(hspace=0.25)
ax = plt.subplot(2, 1, 2)
plt.title('Richness')
plt.xlabel('Position')
plt.ylabel('Number of Unique k-mers')
#plt.ylim(0,60)
richness = richness_map.values()
max_richness = max(richness)
if max_richness == 0:
    max_richness = 1
fracs = [data/max_richness for data in richness]
plt.bar(range(len(richness_map)), richness, width=1, color=jet(fracs), linewidth=0.5)
plt.savefig(sys.argv[2], dpi=dpiVal)
