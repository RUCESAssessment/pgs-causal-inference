# Re-import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the uploaded final merged dataset
final_path = "/Users/gloryekbote/Desktop/work/research project/data/Final24PGS.xlsx"
df_final = pd.read_excel(final_path)

# ----------------------------
# 1. General Data Quality Checks (Simplified)
# ----------------------------

# Total responses
total_responses_final = df_final.shape[0]

# Finished responses
finished_responses_final = df_final[df_final['Finished'] == True].shape[0]

# ----------------------------
# 2. GPA Analysis
# ----------------------------

# Filter for non-null GPA values
gpa_data_final = df_final[df_final['GPA'].notna()].copy()
gpa_data_final['GPA'] = gpa_data_final['GPA'].astype(float)

# GPA summary
gpa_summary_final = gpa_data_final['GPA'].describe()

# # GPA histogram
# plt.figure(figsize=(10, 6))
# sns.histplot(gpa_data_final['GPA'], bins=30, kde=True)
# plt.title('GPA Distribution')
# plt.xlabel('Cumulative GPA')
# plt.ylabel('Number of Students')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# Display key outputs
print(gpa_summary_final)
print(total_responses_final)
print(finished_responses_final)

# Check for column named exactly 'School'
if 'School' in df_final.columns:
    # Filter for valid GPA values
    gpa_by_named_school = df_final[df_final['GPA'].notna()].copy()
    gpa_by_named_school['GPA'] = gpa_by_named_school['GPA'].astype(float)

    # Group by 'School' and calculate summary
    gpa_school_summary = gpa_by_named_school.groupby('School').agg(
        Count=('GPA', 'count'),
        Mean_GPA=('GPA', 'mean'),
        Median_GPA=('GPA', 'median'),
        Std_GPA=('GPA', 'std')
    ).reset_index().sort_values(by='Mean_GPA', ascending=False)

    # Display the results
    print(gpa_school_summary)
else:
    gpa_school_summary = "No column named 'School' found in the dataset."


# === 1. Primary Activity After Graduation (Confirmed) vs First Choice Activity ===
activity_col = "Which of the following best describes what your PRIMARY activity will be AFTER graduation (confirmed, not what you hope to be doing)?"
first_choice_col = "What is/was your first choice activity for after graduation (what you hoped to be doing, not necessarily what you currently have confirmed)? - Selected Choice"

# Frequency distribution for confirmed vs. desired outcomes
confirmed_activity_dist = df_final[activity_col].value_counts(dropna=False).reset_index()
first_choice_dist = df_final[first_choice_col].value_counts(dropna=False).reset_index()

# === 2. Employment Info Summary ===
employment_type_col = "Which one of these categories BEST describes your employment type?"
industry_col = "Select the industry that best describes the work of your company/organization:\n\nFor example, if you are an IT professional for a non-profit that serves the field of education, you would select \"Educational Services\" as your organization's industry. - Broad Industry"
salary_col = "What is your annual gross salary in U.S. dollars (excluding bonuses, commission, or overtime)?\n\n\n\nEnter your salary WITHOUT dollar signs or commas.\n\n\n\nFor example, enter 20000.57 NOT $20,000.57 or 20,000.57"

# Clean and convert salary column
df_final[salary_col] = pd.to_numeric(df_final[salary_col], errors='coerce')

# Employment type distribution
employment_type_dist = df_final[employment_type_col].value_counts(dropna=False).reset_index()

# Top industries
industry_dist = df_final[industry_col].value_counts(dropna=False).head(10).reset_index()

# Salary summary
salary_summary = df_final[salary_col].describe()

print(salary_summary)

