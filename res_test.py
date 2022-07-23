

import pprint
import pandas as pd


res = pd.read_csv("res.csv", on_bad_lines='skip', \
                index_col=False, dtype='unicode')

#print(res['attribution'])

#res['count'] = res.groupby('attribution')['attribution'].transform(pd.Series.value_counts)
#res.sort_values('count', ascending=False)


#counter = 0

res.query("classification == 'Painting'",inplace=True)

#for index, row in res.iterrows():
    #if row['classification'] == "Painting":
    #counter += 1
        
#print(counter)

df = res.groupby(['attribution'])['attribution'].count().reset_index(
  name='Count').sort_values(['Count'], ascending=False)

#with open('attribution freq.txt', 'a') as my_data_file:
df.to_csv(r'Attribution-Author frequency (Paintings).csv', index=None, mode='w')

#print(df)