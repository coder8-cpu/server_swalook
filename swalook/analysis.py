import requests
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
from swalook_backend.settings import BASE_DIR
class Analysis():
        def __init__(self, user):
              self.response = None
              self.api_url = None
              self.user = user

        def monthly_analysis(self,data={}):

                matplotlib.use('agg')
                data = data# converting response into json format
                print(data)
                x_values = []

                y_values = [0]
                for item in data['data']:
                        if item['date_field'] in x_values:
                                pass
                        else:
                                x_values.append(item['date_field']) #giving x field
                i = 0
                value = 0
                for item in data['data']:
                        if x_values[i] == item['date_field']:

                                value = value + float(item['grand_total'])
                        else:
                                print(value)
                                y_values.append(int(value)) #giving y field
                                i = i+1
                                value = 0
                z_value = []
                for i in x_values:
                        txt = i[6:10]
                        txt = txt + " "
                        z_value.append(txt)
                        x_values = z_value
                # giving chart x and y axis labels
                plt.bar(x_values,y_values, color =['green'])
                plt.xlabel("Date")
                plt.ylabel("Total Billing amount")
                # saving plot
                path = os.path.join(BASE_DIR/'media/analysis', "analysis")
                plt.savefig(path+f'monthly_analysis_{self.user}.jpeg')
                return f'monthly_analysis_{self.user}.jpeg'

if __name__ == '__main__':
       a =  Analysis()
