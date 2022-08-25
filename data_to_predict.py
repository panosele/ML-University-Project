import pandas as pd
from model_training import ModelTraining
import matplotlib.pyplot as plt


class Prediction(ModelTraining):
    def __init__(self):
        super().__init__()
        self.new_data = pd.read_excel("NewCampaignData.xlsx", names=self.column_names)
        # -----Split X/y  data(...y data may not be available yet but the column exists in the new data table)
        self.X = self.new_data.iloc[:, :-1]
        self.y = self.new_data.iloc[:, -1]

        self.new_prediction = self.data_conversion_and_predict()

        self.new_data_to_csv()

    # converting data and making prediction
    def data_conversion_and_predict(self):
        # ----Preprocess new X data with 'ct' transformer that was fit only with X_train data characteristics
        self.X = self.ct.transform(self.X)
        # ----Run model with X data
        new_prediction = self.knn.predict(self.X)
        return new_prediction

    # create a csv file with predicted data to show in gui
    def new_data_to_csv(self):
        # ----Inverse prediction data encoding based on the encoding done on Train data
        prediction_inv = self.le.inverse_transform(self.new_prediction)
        # ----change prediction form numpy array to pandas DataFrame and add the correct header name
        df = pd.DataFrame(prediction_inv, columns=[self.column_names[-1]])
        self.new_data.update(df)
        # ----new data to csv
        self.new_data.to_csv("NEW_DATA.csv")

    def percent_of_yes_for_login4weeks(self):
        '''returns the percentage of the people who will join campaign and have logged in last 4 weeks'''
        res = self.new_data.apply(lambda x: True if x['Logins τις τελευταίες 4 εβδομάδες'] > 0 else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(lambda x: True if x['Ανταπόκριση'] == "yes" and x['Logins τις τελευταίες 4 εβδομάδες'] > 0 else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes/num_of_users * 100

    def percent_of_yes_forlogin6months(self):
        '''returns the percentage of the people who will join campaign and have logged in last 6 months'''
        res = self.new_data.apply(lambda x: True if x['Logins τους τελευταίους 6 μήνες'] > 0 else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(
            lambda x: True if x['Ανταπόκριση'] == "yes" and x['Logins τους τελευταίους 6 μήνες'] > 0 else False,axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def percent_of_yes_for_bying_4weeks(self):
        '''returns the percentage of the people who will join campaign and have bought in last 4 weeks'''
        res = self.new_data.apply(lambda x: True if x['Αγορές τις τελευταίες 4 εβδομάδες'] > 0 else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(
            lambda x: True if x['Ανταπόκριση'] == "yes" and x['Αγορές τις τελευταίες 4 εβδομάδες'] > 0 else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def percent_of_yes_for_bying_6months(self):
        '''returns the percentage of the people who will join campaign and have bought in last 6 months'''
        res = self.new_data.apply(lambda x: True if x['Αγορές τους τελευταίους 6 μήνες'] > 0 else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(lambda x: True if x['Ανταπόκριση'] == "yes" and x['Αγορές τους τελευταίους 6 μήνες'] > 0 else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def percent_of_yes_sunolo_agorwn(self):
        '''returns the percentage for those who bouhtgh at least 1 time before and will join the campaign'''
        res = self.new_data.apply(lambda x: True if x['Σύνολο Αγορών'] > 0 else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(
            lambda x: True if x['Ανταπόκριση'] == "yes" and x['Σύνολο Αγορών'] > 0 else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def percent_of_yes_males(self):
        '''returns the percentage of the men who will join campaign'''
        res = self.new_data.apply(lambda x: True if x['Φύλο'] == "male" else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(
            lambda x: True if x['Ανταπόκριση'] == "yes" and x['Φύλο'] == "male" else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def percent_of_yes_females(self):
        '''returns the percentage of the women who will join campaign'''
        res = self.new_data.apply(lambda x: True if x['Φύλο'] == "female" else False, axis=1)
        num_of_users = len(res[res == True].index)

        res = self.new_data.apply(
            lambda x: True if x['Ανταπόκριση'] == "yes" and x['Φύλο'] == "female" else False, axis=1)
        num_of_users_yes = len(res[res == True].index)

        return num_of_users_yes / num_of_users * 100

    def show_stats_graph(self):
        log_4_weeks = self.percent_of_yes_for_login4weeks()
        log_6_months = self.percent_of_yes_forlogin6months()
        buy_4_weeks = self.percent_of_yes_for_bying_4weeks()
        buy_6_months = self.percent_of_yes_for_bying_6months()
        men = self.percent_of_yes_males()
        women = self.percent_of_yes_females()

        category = ["logged last 4 weeks", "logged last 6months", "bought last 4 weeks", "bouhgt last 6 months", "men", "women"]
        stats = [log_4_weeks, log_6_months, buy_4_weeks, buy_6_months, men, women]
        for i in range(len(category)):
            plt.bar(category[i], stats[i], width=0.4)
        plt.yticks([20, 40, 60, 80, 100])
        plt.xticks(fontsize=8, rotation=6)
        plt.ylabel("PERCENTAGE %")
        plt.xlabel("CATEGORY")
        plt.title("Percent who will join campaign based on the characteristics")
        plt.show()
