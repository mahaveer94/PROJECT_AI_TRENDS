# -*- coding: utf-8 -*-
"""AI_Trends_lab.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sqLYIR1oW_8MJMHZOK6-sElJ3EJK7fvd
"""


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
# Add other necessary imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import seaborn as sns  
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder



df=pd.read_csv("txns.txt",header=None)
df.head()

# Rename the columns
df.columns = ['txnno', 'txndate', 'custid', 'amount', 'product', 'category', 'city', 'state', 'spendby']

# Save the DataFrame to a CSV file
df.to_csv("txns.csv", index=False)
df

## EDA Analysis
#Plot histograms or density plots to visualize the distribution of numerical features.
import matplotlib.pyplot as plt

df.hist(figsize=(10, 8))
plt.tight_layout()
plt.savefig('histogram.png')

# pair plots to visualize relationships between numerical features.
import seaborn as sns
sns.pairplot(df)
plt.savefig('pairplot.png')

# bar plots or count plots to visualize the distribution of categorical variables.
sns.countplot(x='spendby', data=df)
plt.savefig('countplot.png')

df.isnull().sum()

# Convert 'txndate' to datetime and extract useful features
df['txndate'] = pd.to_datetime(df['txndate'])
df['day'] = df['txndate'].dt.day
df['month'] = df['txndate'].dt.month
df['year'] = df['txndate'].dt.year

# Drop original 'txndate' column
df.drop('txndate', axis=1, inplace=True)

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = df.select_dtypes(include=['object', 'category']).columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

# Create a mapping dictionary
mapping = {'credit': 0.0, 'cash': 1.0}

# Apply the mapping to the output column
df['spendby'] = df['spendby'].map(mapping)

# Convert the output column to float
df['spendby'] = df['spendby'].astype(float)

X = df.drop(columns=['spendby'])  # Features
y = df['spendby']  # Target

df.head()

# Split Data into Features and Target
X = df.drop(columns=['txnno', 'custid', 'spendby'])  # Features
y = df['spendby']  # Target

# One-hot encode categorical features
X = pd.get_dummies(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test dataset:-
y_pred = model.predict(X_test)

# Evaluate the model:-
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))
