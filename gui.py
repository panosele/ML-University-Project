import tkinter
from tkinter import END, messagebox, Canvas, PhotoImage
import pandas
from model_training import ModelTraining
from data_to_predict import Prediction


class UserInterface:
    def __init__(self):
        self.FONT = ("Courier", 10)
        self.root = tkinter.Tk()
        self.root.wm_minsize(600, 400)
        self.root.maxsize(2000, 1800)
        self.root.title("Campaign Prediction")
        self.root.configure(bg="#ca91ff", padx=30, pady=30)
        self.trained_model = None
        self.prediction = None

        self.canvas = Canvas(width=400, height=350, bg="#ca91ff", highlightthickness=0)
        logo_img = PhotoImage(file="logo1.png")
        self.canvas.create_image(200, 175, image=logo_img)
        self.canvas.grid(row=2, column=0, rowspan=2, columnspan=2, pady=30)

        self.train_label = tkinter.Label(text="Click to train model", font=self.FONT, width=20, pady=20, bg="#ca91ff")
        self.train_label.grid(row=0, column=0)
        self.train_label_button = tkinter.Button(text="Train", font=self.FONT, command=self.train_model)
        self.train_label_button.grid(row=1, column=0)

        self.accur = tkinter.Label(text="Show accuracy", font=self.FONT, width=30, bg="#ca91ff")
        self.accur.grid(row=0, column=1)
        self.show_accur = tkinter.Button(text="Show", font=self.FONT, command=self.show_accuracy)
        self.show_accur.grid(row=1, column=1)

        self.show_plot = tkinter.Label(text="Show accuracy plot", font=self.FONT, width=25, bg="#ca91ff")
        self.show_plot.grid(row=0, column=2)
        self.show_plt = tkinter.Button(text="Show", font=self.FONT, command=self.show_accur_plt)
        self.show_plt.grid(row=1, column=2)

        self.new_data_prediction = tkinter.Label(text="Calculate new campaign", font=self.FONT, width=32, bg="#ca91ff")
        self.new_data_prediction.grid(row=0, column=3)
        self.new_data_prediction_button = tkinter.Button(text="Predict", font=self.FONT, command=self.new_data_predict)
        self.new_data_prediction_button.grid(row=1, column=3)

        self.new_data_to_show = tkinter.Label(text="See predicted data", font=self.FONT, width=30, bg="#ca91ff")
        self.new_data_to_show.grid(row=0, column=4)
        self.new_data_to_show_button = tkinter.Button(text="Show", font=self.FONT, command=self.show_predicted_data)
        self.new_data_to_show_button.grid(row=1, column=4)

        self.stats_label = tkinter.Label(text="Click on statistics you want to see 🢂", font=("Arial", 12), width=28, bg="#ca91ff")
        self.stats_label.grid(row=2, column=2)

        self.listbox = tkinter.Listbox(height=10, width=40, bg="#ca91ff",font=("Arial", 12), highlightthickness=0, highlightcolor="blue", selectmode="SINGLE")
        predictions = ["Logged in last 4 weeks and will join the campaign",
                       "Logged in last 6 months and will join the campaign",
                       "Bought in last 4 weeks and will join the campaign",
                       "Bought in last 6 months and will join the campaign",
                       "Bought at least 1 time and will join the campaign",
                       "Men who will join the campaign",
                       "Women who will join the campaign"]
        for item in predictions:
            self.listbox.insert(predictions.index(item), item)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_used)
        self.listbox.grid(row=2, column=3)

        self.stats_answer_label = tkinter.Label(text="ANSWER 🢂", font=("Arial", 14), width=28, pady=20, bg="#ca91ff")
        self.stats_answer_label.grid(row=3, column=2)

        self.stats_answer_text = tkinter.Label(text="", font=("Arial", 12, "bold"), width=40, pady=20, bg="#ca91ff", wraplength=400)
        self.stats_answer_text.grid(row=3, column=3)

        self.stats_label = tkinter.Label(text="Show statistics plot", font=("Arial", 14), width=28, pady=20, bg="#ca91ff")
        self.stats_label.grid(row=4, column=0)
        self.stats_button = tkinter.Button(text="Show", font=self.FONT, command=self.show_statistiscs_plot)
        self.stats_button.grid(row=5, column=0)

        self.exit_button = tkinter.Button(text="EXIT", width=14, font=("Arial", 12), command=self.exit_the_programm)
        self.exit_button.grid(row=5, column=4)

        self.root.mainloop()

    def show_statistiscs_plot(self):
        if self.prediction is not None:
            self.prediction.show_stats_graph()
        else:
            messagebox.showerror(title="No trained model", message="No trained model yet!\n\n"
                                                                   "You should train a model first and then predict the result.")

    def listbox_used(self, event):
        if self.prediction is not None:
            if self.listbox.curselection()[0] == 0:
                per = self.prediction.percent_of_yes_for_login4weeks()
                self.stats_answer_text.config(text=f"Percentage of those who logged in last 4 weeks and will join the campaign is {per:.2f}%")
            elif self.listbox.curselection()[0] == 1:
                per = self.prediction.percent_of_yes_forlogin6months()
                self.stats_answer_text.config(text=f"Percentage of those who logged in last 6 months and will join the campaign {per:.2f}%")
            elif self.listbox.curselection()[0] == 2:
                per = self.prediction.percent_of_yes_for_bying_4weeks()
                self.stats_answer_text.config(text=f"Percentage of those who bought in last 4 weeks and will join the campaign {per:.2f}%")
            elif self.listbox.curselection()[0] == 3:
                per = self.prediction.percent_of_yes_for_bying_6months()
                self.stats_answer_text.config(text=f"Percentage of those who bought in last 6 months and will join the campaign {per:.2f}%")
            elif self.listbox.curselection()[0] == 4:
                per = self.prediction.percent_of_yes_sunolo_agorwn()
                self.stats_answer_text.config(text=f"Percentage of those who bought at least 1 time and will join the campaign {per:.2f}%")
            elif self.listbox.curselection()[0] == 5:
                per = self.prediction.percent_of_yes_males()
                self.stats_answer_text.config(text=f"Percentage of men who will join the campaign {per:.2f}%")
            elif self.listbox.curselection()[0] == 6:
                per = self.prediction.percent_of_yes_females()
                self.stats_answer_text.config(text=f"Percentage of women who will join the campaign {per:.2f}%")
        else:
            messagebox.showerror(title="No trained model", message="No trained model yet!\n\n"
                                                          "You should train a model first and then predict the result.")

    def exit_the_programm(self):
        exit(0)

    def train_model(self):
        self.trained_model = ModelTraining()
        self.train_label.config(text="Trained")

    def show_accuracy(self):
        if self.trained_model is not None:
            self.accur.config(text=f"Model accuracy:{self.trained_model.accuracy}")
        else:
            messagebox.showerror(title="No trained model", message="No trained model yet!\n\n"
                                                          "You should train a model first.")

    def show_accur_plt(self):
        if self.trained_model is not None:
            self.trained_model.show_prediction_test_graph()
        else:
            messagebox.showerror(title="No trained model", message="No trained model yet!\n\n"
                                                          "You should train a model first and then predict the result.")

    def new_data_predict(self):
        if self.trained_model is not None:
            self.prediction = Prediction()
            self.new_data_prediction.config(text=f"Prediction Done.Accuracy: {self.prediction.accuracy}")
        else:
            messagebox.showerror(title="No trained model", message="No trained model yet!\n\n"
                                                           "You should train a model first and then predict the result.")

    def show_predicted_data(self):
        if self.prediction is not None:
            try:
                pr_data = pandas.read_csv("NEW_DATA.csv").to_string(index=True, columns=['Ηλικία', 'Φύλο', 'Περιοχή', 'Email', 'Χρήση Κινητού',
                              'Logins τις τελευταίες 4 εβδομάδες', 'Logins τους τελευταίους 6 μήνες', 'Αγορές τις τελευταίες 4 εβδομάδες',
                              'Αγορές τους τελευταίους 6 μήνες', 'Σύνολο Αγορών', 'Ανταπόκριση'])
            except FileNotFoundError:
                messagebox.showerror(title="No Data", message="No data found.There is no file with data.\n\n")
            else:
                top = tkinter.Toplevel(self.root, pady=10)
                top.title("Predicted data")
                top.config(width=1000, height=600)
                text = tkinter.Text(top, width=1200, height=600, pady=20)
                text.insert(END, pr_data)
                text.pack()
                top.mainloop()
        else:
            messagebox.showerror(title="No predicted data.", message="No predicted data.\n\nYou should train a model "
                                                                     "first and then predict the result.")

