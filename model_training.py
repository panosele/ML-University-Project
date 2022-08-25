import pandas as pd
from sklearn import neighbors, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


class ModelTraining:

    def __init__(self):
        self.past_data = pd.read_excel("PastCampaignData.xlsx")
        # -------Get Column names for later use
        self.column_names = (list(self.past_data.columns))
        # -------Split  X / yd ata
        self.X = self.past_data.iloc[:, :-1]
        self.y = self.past_data.iloc[:, -1]

        self.data_conversion()

        self.prediction, self.knn, self.accuracy = self.create_model()

    # converting data
    def data_conversion(self):
        # ---------Split past_data to Train and Test data (80% - 20%)
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.20)
        # ----------Preprocess X and y
        # -----'Transformers' will be applied to columns in the order they appear.
        # ------Whatever column is not mentioned in the 'transformers' list of tuples will be placed at the end of the output table, therefore
        # ------if I want to keep the order of columns I have to write a 'passthrough' transformer for the rows I do not want to alter (see below for example).
        # ------if "remainder-'passthrough'" is not included, output will contain only columns matched by the 'transformers'
        transformers = [('Row1', StandardScaler(), [0]), ('Row2', OneHotEncoder(), [1]), ('Row3', OneHotEncoder(), [2]),
                        ('Row4', OneHotEncoder(), [3]), ('Row5', OneHotEncoder(), [4]),
                        ('Row6to10', StandardScaler(), slice(5, 10))]
        self.ct = ColumnTransformer(transformers=transformers, remainder='passthrough')
        # ------Fit X data Preprocessing characteristics on 'ct' based only on X_train data
        self.ct.fit(X_train)
        #-------Transform X_train and X_test data with 'ct
        self.X_train = self.ct.transform(X_train)
        self.X_test = self.ct.transform(X_test)
        # -------Create y data encoder using LabelEncoder() ('le' object)
        # -------Fit y data encoding characteristics on 'le'  based only on y_train data
        self.le = LabelEncoder()
        self.le.fit(y_train)
        # -------Transform y_train and y_test data with 'le
        self.y_train = self.le.transform(y_train)
        self.y_test = self.le.transform(y_test)

    # create model
    def create_model(self):
        # --------Create model ('knn' object)
        knn = neighbors.KNeighborsClassifier(n_neighbors=19, weights="distance")
        # --------Train model with X/y_train data
        knn.fit(self.X_train, self.y_train)
        # --------Run model with X_test data
        prediction = knn.predict(self.X_test)
        # --------Evaluate model performance (accuracy)
        accuracy = metrics.accuracy_score(self.y_test, prediction)

        return prediction, knn, accuracy

    def show_prediction_test_graph(self):
        plt.plot([i for i in range(len(self.y_test))], self.y_test, label="Y_Test")
        plt.plot([i for i in range(len(self.prediction))], self.prediction, label="Prediction")
        plt.title("Σύγκριση Στοιχείων Αληθινά με πρόβλεψη")
        plt.ylabel('Values(0=no, 1=yes)')
        plt.xlabel('Sample of testing')
        plt.legend(fontsize=10)
        plt.show()

