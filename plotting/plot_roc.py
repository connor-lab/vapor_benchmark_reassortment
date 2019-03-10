import sys
import matplotlib
matplotlib.use('agg')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
sns.set_style("ticks")

from numpy import genfromtxt

# Import csv
fig, axes = plt.subplots(nrows=2, ncols=1, sharey=True, sharex=True, figsize=(10,10))
for i, ax in enumerate(axes):
    fname = sys.argv[1+i]
    arr = genfromtxt(fname, delimiter=',')

    y = arr[:,1]
    x = arr[:,2]

    #append 0,0 to the start (equivalently using parameter = 0 percent identity)
    x = np.insert(x, 0, 0., axis=0)
    y = np.insert(y, 0, 0., axis=0)

    #append 1,1 to the end (equivalently using parameter = 100 percent identity)
    y = np.append(y, 1.)
    x = np.append(x, 1.)
    ax.step(x, y)
    ax.plot([min(x),1],[min(y),1], color='black', linestyle='dashed')

ax = fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
ax.set_ylabel("True Positive Rate", labelpad=15)
ax.set_xlabel("False Positive Rate", labelpad=10)


plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.07)
plt.savefig("roc.pdf", format="pdf")
plt.show()
