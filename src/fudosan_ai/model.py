from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


class Model():
    def __init__(self):
        self._model = None
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None

    def train(
            self,
            one_hot_encoded_df,
            y_column_name='total_rent_price'
        ):
        X = one_hot_encoded_df.drop(y_column_name, axis=1)
        y = one_hot_encoded_df[y_column_name]

        self._X_train, self._X_test, self._y_train, self._y_test = (
            train_test_split(
                X,
                y,
                test_size=0.1,
                random_state=0
            )
        )

        self._model = ensemble.GradientBoostingRegressor(
            n_estimators=1000,
            learning_rate=0.1,
            max_depth=9,
            min_samples_leaf=9,
            max_features=1.0,
            loss='huber',
            random_state=0
        )

        self._model.fit(self._X_train, self._y_train)

    def get_training_set_mean_absolute_error(self):
        return '%.4f' % mean_absolute_error(
            self._y_train,
            self._model.predict(self._X_train)
        )

    def get_test_set_mean_absolute_error(self):
        return '%.4f' % mean_absolute_error(
            self._y_test,
            self._model.predict(self._X_test)
        )
