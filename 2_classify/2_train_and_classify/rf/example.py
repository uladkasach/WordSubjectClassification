from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
print(df.head())

train, test = df[df['is_train']==True], df[df['is_train']==False]

features = df.columns[:4]
clf = RandomForestClassifier(n_jobs=2)

y, _ = pd.factorize(train['species'])
clf.fit(train[features], y)

print(train[features]);
print(y);

preds = iris.target_names[clf.predict(test[features])]

print(preds);
##print(pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds']))
