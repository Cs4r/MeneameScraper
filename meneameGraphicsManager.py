import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from pysimplegui import PySimpleGUI as sg

class MeneameGraphicsManager():

    def __init__(self, _path):
        self.path = _path
        self.dataFrame = self.__load_csv()

    def __load_csv(self):
        return pd.read_csv(self.path, sep=";")

    def __show_hist(self):
        """
        Plot the density distribution of the numeric attributes
        """
        fig, axs = plt.subplots(2, 3, figsize=(12, 6))
        fig.delaxes(axs[1,2]) #removed unused axis
        axs[0, 0].hist(self.dataFrame.votes, 100, density=True, facecolor='g', alpha=0.75)
        axs[0, 0].set_title('Votes')
        axs[0, 1].hist(self.dataFrame['down-votes'], 100, density=True, facecolor='r', alpha=0.75)
        axs[0, 1].set_title('Down votes')
        axs[1, 0].hist(self.dataFrame.clicks, 100, density=True, facecolor='orange', alpha=0.75)
        axs[1, 0].set_title('Clicks')
        axs[1, 1].hist(self.dataFrame.comments, 100, density=True, facecolor='blue', alpha=0.75)
        axs[1, 1].set_title('Comments')
        axs[0, 2].hist(self.dataFrame.karma, 100, density=True, facecolor='purple', alpha=0.75)
        axs[0, 2].set_title('Karma')

        for ax in axs.flat:
            ax.set(xlabel='number', ylabel='frequency')

        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        plt.show()
    
    def __show_categorical(self):
        """
        Plot the categorical values frequency distribution
        """
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))
        s_category = self.dataFrame['category'].value_counts()
        s_category.plot.bar(alpha=0.75, rot=30, facecolor='#55a386', ax=axs[0])
        axs[0].set_title("Category")
        s_source = self.dataFrame['source'].value_counts()
        if s_source.size > 20 :
            s_source = s_source[0:20]
        s_source.plot.bar(alpha=0.75, rot=30, facecolor='#fcb100', ax=axs[1])
        axs[1].set_title("Sources (most frequent)")

        for ax in axs.flat:
            ax.set(ylabel='frequency')

        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
        plt.show() 

    def __show_avgTimes(self):
        self.dataFrame['sent-date'] = self.dataFrame['sent-date'].apply(lambda x: int(pd.Timestamp(x).timestamp()))
        self.dataFrame['pub-date'] = self.dataFrame['pub-date'].apply(lambda x: int(pd.Timestamp(x).timestamp()))
        self.dataFrame['diff-time'] = (self.dataFrame['pub-date'] - self.dataFrame['sent-date']).apply(lambda x: abs(x/3600))
        plt.title("Delay between sent and published")
        plt.ylabel("Frequency")
        plt.xlabel("Hours")
        plt.hist(self.dataFrame['diff-time'])
        plt.show()


    def show(self):
        print(self.dataFrame.describe())
        # show the histogram of the data
        self.__show_hist()
        #calculate some statistics of the categorical attributes
        self.__show_categorical()
        #calculate the statistics about the average time between sent and published dates
        self.__show_avgTimes()
