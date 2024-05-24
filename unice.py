import pandas as pd

file_path = 'atms_with_counties.csv'
df = pd.read_csv(file_path)

# df['name_left'] = df['name_left'].replace(to_replace=r'^CEC Bank.*', value='CEC Bank', regex=True)

# Replace values in 'name_left' that start with 'ATM CEC BANK' with 'ATM CEC BANK'
# df['name_left'] = df['name_left'].replace(to_replace=r'^ATM CEC BANK.*', value='ATM CEC BANK', regex=True)

# df['name_left'] = df['name_left'].replace(to_replace=r'^Cec Bank.*', value='CEC Bank', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace='CEC Bank ATM', value='CEC Bank', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace='CEC Bank BANK', value='CEC Bank', regex=True)

# df['name_left'] = df['name_left'].replace(to_replace='Bank BANK Bancomat', value='CEC Bank', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace='Atm BRD Negru Voda', value='BRD Groupe Societe Generale', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*Brd.*', value='BRD Groupe Societe Generale', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*BCR.*', value='BCR', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*ING.*', value='ING', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*Banca Transilvania*', value='Banca Transilvania', regex=True)

# df['name_left'] = df['name_left'].replace(to_replace=r'.*Raiffeisen*', value='Raiffeisen Bank', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace='Transilvania', value='Banca Transilvania', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*Banca Banca Transilvania.*', value='Banca Transilvania', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace='Bancomat Cek Bank', value='CEC Bank', regex=True)
# df['name_left'] = df['name_left'].replace(to_replace=r'.*FirstBank*', value='First Bank', regex=True)
df['name_left'] = df['name_left'].replace(to_replace='Raiffeisen Bank Bank', value='Raiffeisen Bank', regex=True)

df.to_csv('atms_with_counties.csv', index=False)


