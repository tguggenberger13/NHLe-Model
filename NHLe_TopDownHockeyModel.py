#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import TopDownHockey_Scraper.TopDownHockey_EliteProspects_Scraper as tdhepscrape


# In[ ]:


get_ipython().run_cell_magic('time', '', '\nleagues = ["ahl", "nhl"]\nseasons = ["2017-2018", "2018-2019"]\n\nahl_nhl_skaters_1719 = tdhepscrape.get_skaters(leagues, seasons)')


# In[ ]:


ahl_nhl_skaters_1719


# In[ ]:


ahl_nhl_skaters_1719 = ahl_nhl_skaters_1719.drop(columns = 'player')


# In[ ]:


ahl_nhl_skaters_1719


# In[ ]:


ahl_nhl_skaters_1719.playername = ahl_nhl_skaters_1719.playername.str.strip()


# In[ ]:


ahl_nhl_skaters_1719.loc[(ahl_nhl_skaters_1719.playername=="Chris Terry") | (ahl_nhl_skaters_1719.playername=="Sebastian Aho")]


# In[ ]:


#re-order columns 

ahl_nhl_skaters_1719 = ahl_nhl_skaters_1719.loc[:, ['playername', 'team', 'season', 'league', 'position', 'gp', 'g', 'a', 'tp', 'ppg', 'pim', '+/-', 'link']]

#rename player column
ahl_nhl_skaters_1719 = ahl_nhl_skaters_1719.rename(columns = {'playername':'player'})

#print 
ahl_nhl_skaters_1719


# In[ ]:


#filter out rows and columns that meet first and second criteria 

ahl_skaters_1718 = ahl_nhl_skaters_1719.loc[(ahl_nhl_skaters_1719.season=="2017-2018") & (ahl_nhl_skaters_1719.league=="ahl")]
nhl_skaters_1819 = ahl_nhl_skaters_1719.loc[(ahl_nhl_skaters_1719.season=="2018-2019") & (ahl_nhl_skaters_1719.league=="nhl")]


# In[ ]:


#merge

ahl_1718_nhl_1819 = ahl_skaters_1718.merge(nhl_skaters_1819, on ='link', how='inner')

ahl_1718_nhl_1819


# In[ ]:


# drop dupe columns from merge

ahl_1718_nhl_1819 = ahl_1718_nhl_1819.drop(columns = ['season_x', 'league_x', 'season_y', 'league_y', 'player_y', 'position_y'])

ahl_1718_nhl_1819


# In[ ]:


my_columns = list(ahl_1718_nhl_1819.columns)

my_columns.remove('link')

my_columns.append('link')

my_columns


# In[ ]:


ahl_1718_nhl_1819 = ahl_1718_nhl_1819.loc[:, my_columns]

ahl_1718_nhl_1819 = ahl_1718_nhl_1819.rename(columns = {'player_x':'player',
 'team_x':'ahl_team',
 'position_x':'position',
 'gp_x':'ahl_gp',
 'g_x':'ahl_g',
 'a_x':'ahl_a',
 'tp_x':'ahl_p',
 'ppg_x':'ahl_ppg',
 'pim_x':'ahl_pim',
 '+/-_x':'ahl_+/-',
 'team_y':'nhl_team',
 'gp_y':'nhl_gp',
 'g_y':'nhl_g',
 'a_y':'nhl_a',
 'tp_y':'nhl_p',
 'ppg_y':'nhl_ppg',
 'pim_y':'nhl_pim',
 '+/-_y':'nhl_+/-'})

ahl_1718_nhl_1819


# In[ ]:


ahl_1718_nhl_1819.dtypes


# In[ ]:


#replace hyphens as zeroes for numeric values

ahl_1718_nhl_1819.ahl_ppg = np.where(ahl_1718_nhl_1819.ahl_ppg=="-", 0, ahl_1718_nhl_1819.ahl_ppg)
ahl_1718_nhl_1819.nhl_ppg = np.where(ahl_1718_nhl_1819.nhl_ppg=="-", 0, ahl_1718_nhl_1819.nhl_ppg)
ahl_1718_nhl_1819.ahl_gp = np.where(ahl_1718_nhl_1819.ahl_gp=="-", 0, ahl_1718_nhl_1819.ahl_gp)
ahl_1718_nhl_1819.nhl_gp = np.where(ahl_1718_nhl_1819.nhl_gp=="-", 0, ahl_1718_nhl_1819.nhl_gp)

ahl_1718_nhl_1819[ahl_1718_nhl_1819.ahl_ppg=="-"]


# In[ ]:


#change to float dtypes

ahl_1718_nhl_1819.ahl_ppg = ahl_1718_nhl_1819.ahl_ppg.astype(float)
ahl_1718_nhl_1819.nhl_ppg = ahl_1718_nhl_1819.nhl_ppg.astype(float)
ahl_1718_nhl_1819.ahl_gp = ahl_1718_nhl_1819.ahl_gp.astype(float)
ahl_1718_nhl_1819.nhl_gp = ahl_1718_nhl_1819.nhl_gp.astype(float)

ahl_1718_nhl_1819 = ahl_1718_nhl_1819.loc[(ahl_1718_nhl_1819.ahl_gp>=20) & (ahl_1718_nhl_1819.nhl_gp>=20)]

ahl_1718_nhl_1819


# In[ ]:


#build forward and dman dfs

forwards = ahl_1718_nhl_1819.loc[ahl_1718_nhl_1819.position!="D"]
defensemen = ahl_1718_nhl_1819.loc[ahl_1718_nhl_1819.position=="D"]

#count length of each df

forward_count = len(forwards)
defenseman_count = len(defensemen)


# In[ ]:


forward_count_string = str(forward_count)
defenseman_count_string = str(defenseman_count)

print("Total number of forwards: " + forward_count_string)
print("Total number of defensemen: " + defenseman_count_string)


# In[ ]:


forward_counts = forwards.groupby('nhl_team').player.count()
forward_counts


# In[ ]:


forward_counts = pd.DataFrame(forward_counts)


# In[ ]:


forward_counts.sort_values(by = 'player', ascending = False)

forward_counts = forward_counts.reset_index()

forward_counts


# In[ ]:


#begin work to find missing teams - create set

nhl_team_set = set(nhl_skaters_1819.team)


# In[ ]:


nhl_team_set = list(nhl_team_set)
print(pd.DataFrame(nhl_team_set))


# In[ ]:


nhl_team_df = pd.DataFrame(nhl_team_set)

nhl_team_df


# In[ ]:


nhl_team_df = nhl_team_df.rename(columns = {0:'nhl_team'})


# In[ ]:


teams_in_transitioning_forwards = list(forward_counts.nhl_team)

nhl_team_df.loc[nhl_team_df.nhl_team.isin(teams_in_transitioning_forwards)]


# In[ ]:


len(nhl_team_df.loc[nhl_team_df.nhl_team.isin(teams_in_transitioning_forwards)])


# In[ ]:


missing_teams = nhl_team_df.loc[~nhl_team_df.nhl_team.isin(teams_in_transitioning_forwards)]


#missing_teams = nhl_team_df.loc[~nhl_team.isin(teams_in_transitioning_forwards)]

missing_teams


# In[ ]:


forward_counts.head()


# In[ ]:


missing_teams = missing_teams.assign(player = 0)
missing_teams


# In[ ]:


#concat transitioning fwds with missing teams

full_transitioning_forwards = pd.concat([forward_counts, missing_teams])

#filter out "totals" since it's not a legit team

full_transitioning_forwards = full_transitioning_forwards.loc[full_transitioning_forwards['nhl_team']!='totals']

full_transitioning_forwards


# In[ ]:


full_transitioning_forwards.reset_index().head()


# In[ ]:


full_transitioning_forwards = full_transitioning_forwards.reset_index().drop(columns = 'index')

full_transitioning_forwards.head()


# In[ ]:


sns.countplot(full_transitioning_forwards.player)


# In[ ]:


np.corrcoef(ahl_1718_nhl_1819.ahl_ppg, ahl_1718_nhl_1819.nhl_ppg)[0, 1]


# In[ ]:


np.corrcoef(ahl_1718_nhl_1819.ahl_ppg, ahl_1718_nhl_1819.nhl_ppg)[0, 1]**2


# In[ ]:


correlation_coefficient = (np.corrcoef(ahl_1718_nhl_1819.ahl_ppg, ahl_1718_nhl_1819.nhl_ppg)[0, 1])
RSQ = correlation_coefficient**2
RSQ = round(RSQ, 2)
RSQ


# In[ ]:


sns.regplot(x = ahl_1718_nhl_1819.ahl_ppg, y = ahl_1718_nhl_1819.nhl_ppg, color = 'teal')


# In[ ]:


sns.regplot(x = ahl_1718_nhl_1819.ahl_ppg, y = ahl_1718_nhl_1819.nhl_ppg, color = 'teal')

plt.xlabel("AHL Points Per Game in 2017-2018")
plt.ylabel("NHL Points Per Game in 2018-2019")

RSQString = "R^2 = " + str(RSQ)

plt.text(0.2, 0.7, RSQString)

plt.show()


# In[ ]:


## projections for NHLe

nhl_ppg_average = np.mean(ahl_1718_nhl_1819.nhl_ppg)

ahl_ppg_average = np.mean(ahl_1718_nhl_1819.ahl_ppg)

ahl_nhl_equivalency = nhl_ppg_average/ahl_ppg_average

ahl_nhl_equivalency


# In[ ]:


def obtain_nhle_given_ahl_ppg(ahl_ppg):
    nhle = ahl_ppg * 82 * ahl_nhl_equivalency
    nhle = round(nhle, 2)
    print(nhle)


# In[ ]:


obtain_nhle_given_ahl_ppg(.84)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


## TDH Scraper


# In[ ]:


output = tdhepscrape.get_skaters("nhl", "2021-2022")


# In[ ]:


tdhepscrape.get_player_information(output)


# In[ ]:




