import pandas as pd
from scipy.stats import pointbiserialr
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('filtered_lichess/eval_db_processed.csv')

# Calculate ratio of white to black side having the advantage

w_adv = 0
b_adv = 0

for _, row in df.iterrows():
    if int(row['side']) == 1:
        w_adv += 1
    else:
        b_adv += 1

print(w_adv)
print(b_adv)

Find correlations between each factor and response variable
print(*pointbiserialr(df['side'], df['1']))
print(*pointbiserialr(df['side'], df['2']))
print(*pointbiserialr(df['side'], df['3']))
print(*pointbiserialr(df['side'], df['4']))
print(*pointbiserialr(df['side'], df['5']))
print(*pointbiserialr(df['side'], df['6']))
print(*pointbiserialr(df['side'], df['7']))

sns.catplot(df, y='1', kind='box')
plt.show()
sns.displot(df, x='1', kde=True)
plt.show()
sns.displot(df, x='2', kde=True)
plt.show()
sns.displot(df, x='3', kde=True)
plt.show()
sns.displot(df, x='4', kde=True)
plt.show()
sns.displot(df, x='5', kde=True)
plt.show()
sns.displot(df, x='6', kde=True)
plt.show()
sns.displot(df, x='7', kde=True)
plt.show()
