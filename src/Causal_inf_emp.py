# Consolidated Python Code: Causal Inference Using IPW + Covariate Balance Check

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ---------------------------
# STEP 1: Load and Clean Data
# ---------------------------

file_path = "/Users/gloryekbote/Desktop/work/research project/data/Final24PGS.xlsx"
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Identify correct columns by partial match (column names contain line breaks)
internship_col = [col for col in df.columns if 'how many internships did you complete' in col.lower()][0]
employment_col = [col for col in df.columns if 'primary activity' in col.lower()][0]

# Define what counts as "Employed"
employed_statuses = [
    "Employed full-time (on average 30 hours or more per week) (including artists and others who intend to freelance/gig as their primary source of income)",
    "Employed part-time (on average less than 30 hours per week)"
]

# Create binary treatment and outcome columns
df['Internship_Completed'] = df[internship_col].notna().astype(int)
df['Employed'] = df[employment_col].isin(employed_statuses).astype(int)

# ---------------------------
# STEP 2: Define Covariates and Subset Data
# ---------------------------

covariates = ['GPA', 'School', 'Major1']
df_model = df[['Internship_Completed', 'Employed'] + covariates].copy()
df_model = df_model.dropna()

X = df_model[covariates]
T = df_model['Internship_Completed']
Y = df_model['Employed']

# ---------------------------
# STEP 3: Estimate Propensity Scores
# ---------------------------

# One-hot encode categorical features
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), ['School', 'Major1'])
], remainder='passthrough')

# Pipeline for logistic regression
ps_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('logreg', LogisticRegression(solver='lbfgs', max_iter=1000))
])

ps_model.fit(X, T)
propensity_scores = ps_model.predict_proba(X)[:, 1]

# ---------------------------
# STEP 4: Compute IPW Weights
# ---------------------------

df_model['weights'] = np.where(T == 1, 1 / propensity_scores, 1 / (1 - propensity_scores))

treated = df_model[T == 1]
control = df_model[T == 0]

# Estimate ATE
ate_ipw = (
    np.average(treated['Employed'], weights=treated['weights']) -
    np.average(control['Employed'], weights=control['weights'])
)

# ---------------------------
# STEP 5: Visualize Result
# ---------------------------

emp_rate_treated = np.average(treated['Employed'], weights=treated['weights'])
emp_rate_control = np.average(control['Employed'], weights=control['weights'])

plt.figure(figsize=(7, 5))
bars = plt.bar(['Internship', 'No Internship'], [emp_rate_treated, emp_rate_control])
plt.ylabel('Employment Rate (Weighted)')
plt.title('Employment Probability by Internship Status (IPW Adjusted)')
plt.ylim(0, 1)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02, f'{bar.get_height():.2%}', ha='center')
plt.tight_layout()
plt.show()

# ---------------------------
# STEP 6: Love Plot (Covariate Balance)
# ---------------------------

from scipy.spatial.distance import euclidean

def standardized_mean_diff(x_treat, x_control):
    mean_diff = x_treat.mean() - x_control.mean()
    pooled_std = np.sqrt((x_treat.var() + x_control.var()) / 2)
    return mean_diff / pooled_std

X_encoded = preprocessor.fit_transform(X)
X_encoded_df = pd.DataFrame(X_encoded)

smd_unweighted = []
smd_weighted = []

for i in range(X_encoded_df.shape[1]):
    smd_unweighted.append(
        standardized_mean_diff(
            X_encoded_df.iloc[T.values == 1, i],
            X_encoded_df.iloc[T.values == 0, i]
        )
    )
    smd_weighted.append(
        standardized_mean_diff(
            X_encoded_df.iloc[T.values == 1, i] * treated['weights'].values,
            X_encoded_df.iloc[T.values == 0, i] * control['weights'].values
        )
    )

plt.figure(figsize=(8, 6))
plt.axvline(x=0, color='gray', linestyle='--')
plt.axvline(x=0.1, color='red', linestyle='--', label='Threshold (|SMD| = 0.1)')
plt.axvline(x=-0.1, color='red', linestyle='--')
plt.scatter(smd_unweighted, range(len(smd_unweighted)), label='Before Weighting', color='blue')
plt.scatter(smd_weighted, range(len(smd_weighted)), label='After Weighting', color='green')
plt.yticks(range(len(smd_unweighted)), [f"V{i+1}" for i in range(len(smd_unweighted))])
plt.xlabel('Standardized Mean Difference')
plt.title('Love Plot: Covariate Balance Before and After IPW')
plt.legend()
plt.tight_layout()
plt.show()

# Return the ATE value
print(ate_ipw)
