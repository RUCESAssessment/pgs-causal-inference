# Re-import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# File paths
survey_path = "/Users/gloryekbote/Desktop/work/research project/data/CleanPGS_2025.xlsx"
gpa_path = "/Users/gloryekbote/Desktop/work/research project/data/May25 Undergrad GPAs.xlsx"
reference_path = "/Users/gloryekbote/Desktop/work/research project/data/Class of 2025_May PGS_June 9, 2025_10.38 (1).xlsx"

# Step 1: Load data
df_survey = pd.read_excel(survey_path, sheet_name='Raw Data')
df_gpa = pd.read_excel(gpa_path, sheet_name='Undergrad May25 GPAs')
df_reference = pd.read_excel(reference_path, sheet_name='Sheet0')

# Step 2: Clean survey and GPA data
df_survey_cleaned = df_survey.drop(index=0).reset_index(drop=True)
df_survey_cleaned['RUID'] = df_survey_cleaned['RUID'].astype(str).str.strip().str.lstrip('0')
df_gpa.rename(columns={'S Rutgers Id': 'RUID', 'S Cum Gpa Ug To Date': 'GPA'}, inplace=True)
df_gpa['RUID'] = df_gpa['RUID'].astype(str).str.strip().str.lstrip('0')

# Step 3: Merge
merged_df = pd.merge(df_survey_cleaned, df_gpa, on='RUID', how='left')

# Step 4: Rename columns
column_reference_labels = df_reference.iloc[0]
column_mapping = dict(zip(merged_df.columns[:len(column_reference_labels)], column_reference_labels))
merged_df_renamed = merged_df.rename(columns=column_mapping)

# Display the final merged and renamed DataFrame
print(merged_df_renamed)
# Save the updated DataFrame
output_file_path = "/Users/gloryekbote/Desktop/work/research project/data/Final24PGS.xlsx"
merged_df_renamed.to_excel(output_file_path, sheet_name='Raw Data', index=False)
print(f"Updated Excel file saved at: {output_file_path}")