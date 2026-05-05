import pandas as pd
import matplotlib.pyplot as plt


# Sample data
data = {'Year': [2020, 2021, 2022, 2023],
        'Sales': [100, 150, 130, 180],
        'Expenses': [80, 90, 95, 110]}
df = pd.DataFrame(data)

plt.hist(df['Expenses'],  color='skyblue')

plt.xlabel("Year")
plt.ylabel("xpenses")

plt.show()
