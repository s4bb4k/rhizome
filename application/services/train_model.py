import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from application.services.dataset_generator import generate_dataset


def train():
    df = generate_dataset(500)

    X = df.drop("score", axis=1)
    y = df["score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    print("R2 modelo:", model.score(X_test, y_test))

    joblib.dump(model, "model.pkl")


if __name__ == "__main__":
    train()