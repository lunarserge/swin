PROJECT = ''

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn import metrics

dates,titles,affiliations = pd.read_pickle(PROJECT+'-dataset.pickle')
df = pd.DataFrame(data=[(d,t,a) for d,t,a in zip(dates,titles,affiliations)],
                  columns=['Date','Title','Affiliation'])

print(df.head(),end='\n\n')

# train with Intel and Nvidia PRs - filter out everything else
others = []
for i,d,t,a in df.itertuples():
    if a not in ['intel', 'nvidia']:
        others.append(i)
df = df.drop(others)

print(df['Affiliation'].value_counts(),end='\n\n')

X = df['Title']
y = df['Affiliation']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

text_clf = Pipeline([('tfidf', TfidfVectorizer()),('clf', LinearSVC()),])
text_clf.fit(X_train, y_train)

predictions = text_clf.predict(X_test)
print(metrics.confusion_matrix(y_test, predictions))
print(metrics.classification_report(y_test,predictions))
print(metrics.accuracy_score(y_test, predictions))

with open(PROJECT+'-model.pickle', 'wb') as f:
    pickle.dump(text_clf, f)
