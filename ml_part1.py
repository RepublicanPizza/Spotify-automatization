import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class Predictor:
    def __init__(self, song_info, genres):
        self.song_info = song_info
        self.genres = genres
        self.dataset = pd.read_csv("songs.csv")
        self.le = LabelEncoder()
        self.knn = KNeighborsClassifier(n_neighbors=100, metric="minkowski", p=2)
        self.sc = StandardScaler()
        self.svc = SVC()
        self.lr = LogisticRegression(multi_class="multinomial")
        self.MNB = BernoulliNB()
        self.GNB = GaussianNB()
        self.OVR = OneVsRestClassifier(self.svc)
        self.RFC = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0, max_features="auto",
                                          class_weight="balanced_subsample")

    def predict_all_genres(self):
        results = []
        for genre in self.genres:
            dataset1 = self.dataset.copy()
            dataset1.loc[(dataset1.genre != genre), "genre"] = f"not {genre}"

            X = dataset1.iloc[:, 1:-1].values
            y = dataset1.iloc[:, -1].values

            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

            x_train = self.sc.fit_transform(x_train)
            x_test = self.sc.transform(x_test)

            y_test = self.le.fit_transform(y_test)
            y_train = self.le.fit_transform(y_train)

            # Predictions

            self.svc.fit(x_train, y_train)

            y_pred_svc = self.svc.predict(x_test)

            print("SVC")
            accuracy_svc = accuracy_score(y_test, y_pred_svc)
            svc_prediction = self.le.inverse_transform(self.svc.predict(self.sc.fit_transform([self.song_info])))
            if svc_prediction == genre:
                results.append([svc_prediction, accuracy_svc])

            self.knn.fit(x_train, y_train)

            y_pred_knn = self.knn.predict(x_test)

            print("KNN")
            accuracy_knn = accuracy_score(y_test, y_pred_knn)
            knn_prediction = self.le.inverse_transform(self.knn.predict(self.sc.fit_transform([self.song_info])))
            if knn_prediction == genre:
                results.append([knn_prediction, accuracy_knn])

            self.lr.fit(x_train, y_train)

            y_pred_lr = self.lr.predict(x_test)

            print("LR")
            accuracy_lr = accuracy_score(y_test, y_pred_lr)
            lr_prediction = self.le.inverse_transform(self.lr.predict(self.sc.fit_transform([self.song_info])))
            if lr_prediction == genre:
                results.append([lr_prediction, accuracy_lr])

            self.MNB.fit(x_train, y_train)
            y_pred_mnb = self.MNB.predict(x_test)

            print("MNB")
            accuracy_mnb = accuracy_score(y_test, y_pred_mnb)
            mnb_prediction = self.le.inverse_transform(self.MNB.predict(self.sc.fit_transform([self.song_info])))
            if mnb_prediction == genre:
                results.append([mnb_prediction, accuracy_mnb])

            self.GNB.fit(x_train, y_train)

            y_pred_GNB = self.GNB.predict(x_test)

            print("GNB")
            accuracy_gnb = accuracy_score(y_test, y_pred_GNB)
            gnb_prediction = self.le.inverse_transform(self.GNB.predict(self.sc.fit_transform([self.song_info])))
            if gnb_prediction == genre:
                results.append([gnb_prediction, accuracy_gnb])

            self.RFC.fit(x_train, y_train)

            y_pred_RFC = self.RFC.predict(x_test)

            print("RFC")
            accuracy_rfc = accuracy_score(y_test, y_pred_RFC)
            rfc_prediction = self.le.inverse_transform(self.RFC.predict(self.sc.transform([self.song_info])))
            if rfc_prediction == genre:
                results.append([rfc_prediction, accuracy_rfc])

            self.OVR.fit(x_train, y_train)
            y_pred_OVR = self.OVR.predict(x_test)

            print("OVR")
            accuracy_ovr = accuracy_score(y_test, y_pred_OVR)
            ovr_prediction = self.le.inverse_transform(self.OVR.predict(self.sc.transform([self.song_info])))
            if ovr_prediction == genre:
                results.append([ovr_prediction, accuracy_ovr])

        return results
