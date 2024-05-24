# import pandas as pd
#
# # Încărcarea datelor din fișierul CSV
# df = pd.read_csv('atms_romania.csv')
#
# df_cleaned = df.drop_duplicates()
#
# # Salvarea datelor curățate înapoi într-un fișier CSV
# df_cleaned.to_csv('atms_romania_curatat.csv', index=False)


import pandas as pd

df = pd.read_csv('atms_romania_curatat2.csv')
df_filtered = df[df['name'] != 'Erste Bank ATM']
df_filtered.to_csv('atms_romania_curatat2.csv', index=False)
