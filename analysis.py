import argparse
from datetime import datetime
from getpass import getpass
from pathlib import Path
from scrape_scorecards import scrape_golfshot
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
Index(['Unnamed: 0', 'N°', 'Nom', 'T', 'Date', 'NbT', 'Fml', 'Golf', 'Terrain',
       'Rep.', 'Par', 'SSS', 'Slope', 'Course Handicap', 'Stat.', 'Score',
       'SBA', 'PCC', 'Diff', 'Ajst', 'Idx'],
      dtype='object')
"""

fiche_index = 'data/fiche_historique_index_gaetan.schaeffer.xlsx'
fiche_index_2 = 'data/fiche_historique_index_Jerome Roeser.xlsx'

df = pd.read_excel(fiche_index)
df_2 = pd.read_excel(fiche_index_2)

#%%
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
axs[0].violinplot(df.Diff)
axs[1].violinplot(df_2.Diff)

for ax in axs:
    ax.set(ylim=(0, 100))
    
#%%
fig, ax = plt.subplots()

# ax.scatter(df.loc[:,'N°'], df.Diff)
ax.scatter(df.index, df.Idx)
# ax.scatter(df_2.loc[:,'N°'], df_2.Diff)
ax.scatter(df_2.index, df_2.Idx)
ax.set(ylim=(0, 54))





#%%
"""
import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# Fixing random state for reproducibility
np.random.seed(19680801)


# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

# plot violin plot
axs[0].violinplot(all_data,
                  showmeans=False,
                  showmedians=True)
axs[0].set_title('Violin plot')

# plot box plot
axs[1].boxplot(all_data)
axs[1].set_title('Box plot')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                  labels=['x1', 'x2', 'x3', 'x4'])
    ax.set_xlabel('Four separate samples')
    ax.set_ylabel('Observed values')

plt.show()
"""