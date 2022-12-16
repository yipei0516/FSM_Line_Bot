import pandas as pd

df = pd.read_csv('drama.csv')
# print(df[['類型', '演員名稱']])

genre = '愛情'
actor = '丁海寅'
years = 2021

fit_drama = df[ df['類型'].str.contains(genre) & df['演員名稱'].str.contains(actor) & (df['發行年份']==years) ]

#前面的state已經檢查過是否有包含這演員...->不需再檢查一次
text = ''
recommend_drama = fit_drama.head(3)
for index, row in recommend_drama.iterrows(): 
    print(index)
    print(row)
    text += row['韓劇名稱'] + '\n'
print(text)
