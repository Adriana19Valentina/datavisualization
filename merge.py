import pandas as pd

# Load the data
df_1_name = "atm_final_romania.csv"
df_2_name = "data_within_romania_3.csv"
df1 = pd.read_csv(df_1_name)
df2 = pd.read_csv(df_2_name)

# Concatenate the dataframes
combined_df = pd.concat([df1, df2])

# Find duplicates based on the 'vicinity' and 'name_left' columns
duplicates = combined_df[
    combined_df.duplicated(subset=["vicinity", "name_left"], keep=False)
]

# Print the duplicates
print(duplicates)

# Get the count of each duplicate occurrence
duplicate_counts = (
    duplicates.groupby(["vicinity", "name_left"]).size().reset_index(name="Count")
)

# Print the counts of each duplicate group
print(duplicate_counts)

# Drop duplicates based on the 'vicinity' and 'name_left' columns
final_df = combined_df.drop_duplicates(subset=["vicinity", "name_left"])

# Optionally, save the final dataframe to a CSV file if needed
final_df.to_csv("atm_final_romania_2.csv", index=False)
