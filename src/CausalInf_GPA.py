import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_excel("Users/gloryekbote/Desktop/work/research project/data/Final24PGS.xlsx")
df.columns = df.columns.str.strip()

# Define column names
gpa_col = "GPA"
major_col = "Major1"
salary_col = (
    "What is your annual gross salary in U.S. dollars (excluding bonuses, commission, or overtime)?\n\n\n\n"
    "Enter your salary WITHOUT dollar signs or commas.\n\n\n\n"
    "For example, enter 20000.57 NOT $20,000.57 or 20,000.57"
)

# Step 1: Clean and subset
df_sub = df[[gpa_col, salary_col, major_col]].dropna()
df_sub = df_sub[(df_sub[gpa_col] != "") & (df_sub[salary_col] != "")]
df_sub[gpa_col] = pd.to_numeric(df_sub[gpa_col], errors='coerce')
df_sub[salary_col] = pd.to_numeric(df_sub[salary_col], errors='coerce')
df_sub = df_sub.dropna()

# Step 2: Create binary indicators
df_sub['High_GPA'] = (df_sub[gpa_col] > 3.0).astype(int)
mean_salary_by_major = df_sub.groupby(major_col)[salary_col].transform('mean')
df_sub['High_Salary'] = (df_sub[salary_col] > mean_salary_by_major).astype(int)

# Step 3: Top 10 most common majors
top_majors = df_sub[major_col].value_counts().nlargest(10).index
df_top_majors = df_sub[df_sub[major_col].isin(top_majors)].copy()

# Step 4: Create acronyms for Major1
acronyms = {
    maj: ''.join([w[0] for w in maj.split() if w[0].isalpha()]).upper()
    for maj in df_top_majors[major_col].unique()
}
df_top_majors['Major1_Acronym'] = df_top_majors[major_col].map(acronyms)

# Step 5: Plot salary distribution by GPA category for top 10 majors
plt.figure(figsize=(14, 6))
sns.boxplot(data=df_top_majors, x="Major1_Acronym", y=salary_col, hue="High_GPA")
plt.xticks(rotation=45)
plt.xlabel("Major (Acronym)")
plt.ylabel("Salary")
plt.title("Salary Distribution by GPA Category (High vs Low) for Top 10 Majors (Acronyms)")
plt.legend(title="High GPA")
plt.tight_layout()
plt.savefig("/mnt/data/salary_by_gpa_top10_majors_acronyms.png")
plt.close()
