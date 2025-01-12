#!/usr/bin/env python
# coding: utf-8

# In[116]:


#Our Libraries
import pandas as pd # used for handling the dataset
import numpy as np #used for handling numbers
import matplotlib.pyplot as plt #checking for outliers
import seaborn as sns #checking for outliers
from sklearn.impute import SimpleImputer #handles missing data

print("Complete")


# In[117]:


#create dataframe
df = pd.read_excel(r'C:\Users\tyler\OneDrive - SNHU\WGU\Data Preparation and Exploration\Employee Turnover Dataset.xlsx')
print("df complete")


# In[118]:


#check df
df.info()


# In[119]:


# NumCompaniesPreviouslyWorked,  AnnualProfessionalDevHrs, TextMessageOptIn all have null values
#find zero values for each
rows_0_prev = df['NumCompaniesPreviouslyWorked'] == 0
rows_0_annual = df['AnnualProfessionalDevHrs'] == 0
#check for zero
any_0_rev = rows_0_prev.any()
any_0_annual = rows_0_annual.any()
print("Prev:", any_0_rev)
print("Annual:", any_0_annual)


# In[120]:


#No actual 0 values for either NumCompaniesPreviouslyWorked and AnnualProfessionalDevHrs
#Knowing what these values represent, we can tell these are probably equal to zero.
#Set Nulls to 0
df['NumCompaniesPreviouslyWorked'] = df['NumCompaniesPreviouslyWorked'].fillna(0)
df['AnnualProfessionalDevHrs'] = df['AnnualProfessionalDevHrs'].fillna(0)
#check
df.info()


# In[121]:


#It doesn't appear that there are no "no" in the TextMessageOptIn
#Check for No'
rows_no_text = df['TextMessageOptIn'] == "No"
#check for zero
any_no_text = rows_no_text.any()
print("Any No in texts:", any_no_text)


# In[122]:


#There are No's in the text column. We can assume that these Null values are No
#As they would have checked yes otherwise.
#change Nulls to No
df['TextMessageOptIn'] = df['TextMessageOptIn'].fillna("No")
df.info()


# In[123]:


#set duplicates for employee id
duplicate_counts = df['EmployeeNumber'].value_counts()
#filter to show only EmployeeNumbers that appear more than once
duplicates = duplicate_counts[duplicate_counts > 1]

#check with a conditional
if duplicates.empty:
    print("No duplicates found in EmployeeNumber.")
else:
    print("Duplicates found in EmployeeNumber:")
    print(duplicates)


# In[124]:


#There are many duplicates. Looks to be 99.
#remove EmployeeNumber Dupes
df = df.drop_duplicates(subset='EmployeeNumber', keep='first')
#df afer
df.info()


# In[125]:


#Make sure no dupes
#set duplicates for employee id
duplicate_counts = df['EmployeeNumber'].value_counts()
#filter to show only EmployeeNumbers that appear more than once
duplicates = duplicate_counts[duplicate_counts > 1]

#check with a conditional
if duplicates.empty:
    print("No duplicates found in EmployeeNumber.")
else:
    print("Duplicates found in EmployeeNumber:")
    print(duplicates)


# In[126]:


#Consistencies will best be found via unique values
#CompensationType First
print(df['CompensationType'].unique())


# In[127]:


print(df['JobRoleArea'].unique())


# In[128]:


#IT and HR need to be consistent data points
#change them all to IT aand HR accordingly
df['JobRoleArea']=df['JobRoleArea'].replace({
    'Information_Technology': 'IT',
    'Information Technology': 'IT',
    'InformationTechnology': 'IT',
    'Human_Resources': 'HR',
    'HumanResources': 'HR',
    'Human Resources': 'HR'
})
#check it
print(df['JobRoleArea'].unique())


# In[129]:


print(df['Gender'].unique())


# In[130]:


#Gender is good
print(df['MaritalStatus'].unique())


# In[131]:


#Marital Status good
print(df['PaycheckMethod'].unique())


# In[132]:


#Mail Check and Direct Deposit need to be consistent data points
#change them all to IT aand HR accordingly
df['PaycheckMethod']=df['PaycheckMethod'].replace({
    'Mail_Check': 'Mail Check',
    'Mailed Check': 'Mail Check',
    'MailedCheck': 'Mail Check',
    'Direct_Deposit': 'Direct Deposit',
    'DirectDeposit': 'Direct Deposit'
})
#check it
print(df['PaycheckMethod'].unique())


# In[133]:


#Payment Method is now good
print(df['TextMessageOptIn'].unique())


# In[134]:


#Formatting Errors next
#start with column names
print(df.columns)


# In[135]:


#Hourly Rate has a space after
#delete the space
df.columns = df.columns.str.strip()

#check
print(df.columns)


# In[136]:


#I know Hourly Rate has a dollar sign that may lead to more trouble down the line
#And I know AnnualSalary did not have the right amount of decimal spaces
#Removing dollar signs and commas
df['HourlyRate'] = df['HourlyRate'].replace({r'\$': '', ',': ''}, regex=True)
#Convert column to numeric
df['HourlyRate'] = pd.to_numeric(df['HourlyRate'], errors='coerce')
#check
print(df['HourlyRate'].unique())


# In[137]:


#Two decimal points on Annual Salary
df['AnnualSalary'] = df['AnnualSalary'].apply(lambda x: f"{x:.2f}")

# Check the result
print(df['AnnualSalary'].unique())


# In[138]:


#check data type
print(df.dtypes)


# In[139]:


#AnnualProfessionalDevHrs should be in integer form. No need for decimals. Change to Int
df['AnnualProfessionalDevHrs'] = df['AnnualProfessionalDevHrs'].astype(int)
# Check the result
print(df['AnnualProfessionalDevHrs'].unique())


# In[140]:


#Now that the formatting is accurate, next comes the outliers
#I will be using boxplots to search for outliers
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Age'])
plt.title('Box plot for Age')
plt.show()


# In[141]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Tenure'])
plt.title('Box plot for Tenure')
plt.show()


# In[142]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['HourlyRate'])
plt.title('Box plot for HourlyRate')
plt.show()


# In[143]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['HoursWeekly'])
plt.title('Box plot for HoursWeekly')
plt.show()


# In[144]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['AnnualSalary'])
plt.title('Box plot for AnnualSalary')
plt.show()


# In[145]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['NumCompaniesPreviouslyWorked'])
plt.title('Box plot for NumCompaniesPreviouslyWorked')
plt.show()


# In[146]:


plt.figure(figsize=(10, 6))
sns.boxplot(x=df['AnnualProfessionalDevHrs'])
plt.title('Box plot for AnnualProfessionalDevHrs')
plt.show()


# In[115]:


#download csv of new df
df.to_csv('msmith_employee_data.csv', index=False)
print('complete')


# In[ ]:




