from tqdm import tqdm
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib

birth = date(1991, 1, 17)
today = date(2021, 3, 17)
death = date(2071, 1, 17)


current = birth + timedelta(days=17)

delta = today - birth
omega = death - birth

print(delta.days)
print(omega.days)
print("remaining", omega - delta)

past = pd.DataFrame({'day': np.arange(0, delta.days),
                     'status': np.array(np.zeros(delta.days))})
future = pd.DataFrame({'day': np.arange(delta.days, omega.days),
                       'status': np.array(np.ones(omega.days - delta.days))})

lifetime = pd.concat([past, future])
lifetime = lifetime.reset_index()
lifetime = lifetime.iloc[:, 1:]

years = list()
for i in tqdm(range(0, omega.days)):
    tyears = relativedelta(birth + timedelta(days=i), birth).years
    years.append(tyears)

move = list()
for k in tqdm(range(0, 80)):
    move = np.concatenate([move, np.arange(0, years.count(k))])

lifetime['date'] = move
lifetime['years'] = years
lifetime_wide = lifetime.pivot_table(index='years',
                                     columns='date',
                                     values='status')

sns.heatmap(lifetime_wide)

