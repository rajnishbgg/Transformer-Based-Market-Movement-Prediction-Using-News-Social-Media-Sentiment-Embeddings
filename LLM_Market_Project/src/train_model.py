from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_model(data):

    X = data[["Sentiment", "Volume"]]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))

    return model