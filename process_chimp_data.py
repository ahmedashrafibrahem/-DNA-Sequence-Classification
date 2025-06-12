import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Function to convert sequence strings into k-mer words
def getKmers(sequence, size=6):
    return [sequence[x:x+size].lower() for x in range(len(sequence) - size + 1)]

# Read the chimp data
print("Reading chimp data...")
chimp_data = pd.read_table('chimp_data.txt')

# Convert sequences to k-mers
print("Converting sequences to k-mers...")
chimp_data['words'] = chimp_data.apply(lambda x: getKmers(x['sequence']), axis=1)
chimp_data = chimp_data.drop(['sequence'], axis=1)

# Convert k-mers to text sentences
chimp_texts = list(chimp_data['words'])
for item in range(len(chimp_texts)):
    chimp_texts[item] = ' '.join(chimp_texts[item])
y_data = chimp_data.iloc[:, 0].values

# Create the Bag of Words model
print("Creating Bag of Words model...")
cv = CountVectorizer(ngram_range=(4,4))
X = cv.fit_transform(chimp_texts)

# Split the data
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y_data, test_size=0.20, random_state=42)

# Train the model
print("Training Multinomial Naive Bayes model...")
classifier = MultinomialNB(alpha=0.1)
classifier.fit(X_train, y_train)

# Make predictions
print("Making predictions...")
y_pred = classifier.predict(X_test)

# Print results
print("\nModel Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Print class distribution
print("\nClass Distribution:")
print(chimp_data['class'].value_counts().sort_index()) 