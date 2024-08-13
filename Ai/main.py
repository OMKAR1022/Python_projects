from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# load the iris dataset
iris = datasets.load_iris()

# create feature and target arrays
X = iris.data
y = iris.target

# split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create the KNN classifier
knn = KNeighborsClassifier(n_neighbors=3)

# train the classifier with the training data
knn.fit(X_train, y_train)

# make predictions with the test data
y_pred = knn.predict(X_test)

# evaluate the accuracy of the classifier
accuracy = knn.score(X_test, y_test)
print("Accuracy:", accuracy)
