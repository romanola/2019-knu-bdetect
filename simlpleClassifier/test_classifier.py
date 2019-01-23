from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import fetch_data

# Rewriting data
fetch_data.fetch('amazon_baby.csv', 2, [0])

# Uploading and splitting dataset
dataset = load_files('data', categories={'+1', '-1'})
docs_train, docs_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.2)

# Making a Pipeline with Count Vectorizer and Logistic
text_clf = Pipeline([
    ('vect', CountVectorizer(token_pattern=r'\b\w+\b')),
    ('clf', LogisticRegression())
])

# Training classifier
text_clf.fit(docs_train, y_train)

# Predict test part of dataset
y_predicted = text_clf.predict(docs_test)

# Checking results
print(metrics.classification_report(y_test, y_predicted,
                                    target_names=dataset.target_names))
cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)




