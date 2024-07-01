import Grassdor_scraper as gs
import pandas as pd
import regex as re
import numpy as np

df = pd.read_csv('glassdoor_jobs.csv')

df = df[df["Salary Estimate"] != "-1"]

# create column hourly and employer_estimated
df["hourly"] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df["employer_provided"] = df['Salary Estimate'].apply(lambda x: 1 if "employer provided salary" in x.lower() else 0)

# create column min, max, average salary
salary_clean = df["Salary Estimate"].apply(lambda x: re.findall("\d+", x))
df["min_salary"] = salary_clean.apply(lambda x: int(x[0]))
df["max_salary"] = salary_clean.apply(lambda x: int(x[1]))
df["average_salary"] = (df["min_salary"] + df["max_salary"]) / 2

# create company_txt
df['company_txt'] = df["Company Name"].apply(lambda x: x.split('\n')[0])

# create state column
df['job_state'] = df['Location'].apply(lambda x: (x.split(',')[1]).strip())
df['job_state'] = df['job_state'].apply(lambda x: 'CA' if 'Los Angeles' in x else x)
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

# create company age column
df['company_age'] = df['Founded'].apply(lambda x: 2020 - x if x>0 else x)

# parse job description
df['Job Description'].values

## Python
# df['python_yn'] = df.apply(lambda x: 1 if 'python' in x['Job Description'] else 0, axis=1)
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['python_yn'].value_counts()
## R
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() else 0)
df['R_yn'].value_counts()
## SQL
df['SQL_yn'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['SQL_yn'].value_counts()
## Spark
df['Spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['Spark'].value_counts()
## AWS
df['AWS'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['AWS'].value_counts()
## Excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if re.search(r'\bexcel\b', x, flags=re.IGNORECASE) else 0)
df['excel'].value_counts()

#drop unname
df.columns
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df.to_csv('data_clean.csv')

data = pd.read_csv("data_eda.csv")

