import seaborn as sns
import matplotlib.pyplot as plt

#----------------------------SALARY-------------------------------------------------
# Step 1: Identify the salary column by fuzzy matching since the name is long
salary_cols = [col for col in df_projects.columns if 'salary' in col.lower()]
salary_cols

# Rename for convenience
salary_col = [col for col in df_projects.columns if 'annual gross salary' in col][0]

# Extract GPA and salary columns
df_salary = df_projects[['GPA', salary_col]].copy()

# Convert to numeric
df_salary['GPA'] = pd.to_numeric(df_salary['GPA'], errors='coerce')
df_salary['Salary'] = pd.to_numeric(df_salary[salary_col], errors='coerce')

# Drop missing values
df_salary.dropna(inplace=True)

# Compute correlation
correlation = df_salary['GPA'].corr(df_salary['Salary'])

# Visualize
plt.figure(figsize=(8, 6))
sns.regplot(data=df_salary, x='GPA', y='Salary', scatter_kws={'alpha':0.5})
plt.title(f'GPA vs Salary (Correlation: {correlation:.2f})')
plt.xlabel('GPA')
plt.ylabel('Annual Salary (USD)')
plt.tight_layout()
plt.show()


