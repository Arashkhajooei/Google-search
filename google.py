from googlesearch import search
import requests
import re
import csv
import pandas as pd


class Search:
    def __init__(self):
        self.sentence = None
        self.result_number = None
        self.result = 0
        self.headers = []
        self.final_result = []

        self.File_Write_instance = CSVWriter("data.csv")

    
    def get_input(self):
        try:
            self.sentence = input("Enter a sentence: ")
        except Exception as e:
            print(f"Error: {e}")
    
    def get_result_number(self):
        try:
            self.result_number = int(input("Enter the result number: "))
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer.")
        except Exception as e:
            print(f"Error: {e}")

    def searching(self):
        self.result=list(search(self.sentence, tld="co.in", num=self.result_number, stop=self.result_number, pause=2))


        for i in range(self.result_number):
         self.headers.append(len(re.findall(New.sentence, requests.get(self.result[i]).text)))

        for i in range(self.result_number):
         self.final_result.append([self.headers[i],self.result[i]])

        return self.result 


    def run(self):
        self.get_input()
        self.get_result_number()
        self.searching()
        self.print_result()
        self.File_Write_instance.write(self.final_result)
        print(f"Original sentence: {self.sentence}")
        print(f"Custom function result: {self.result}")
        self.File_Write_instance.to_dataframe(self.headers,self.result)

    def print_result(self):
      for j in self.result:
        print(j)


class CSVWriter:
    def __init__(self, filename, header=None):
        self.filename = filename
        self.header = header

    def write(self, data):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for element in data:
              writer.writerow([element])
            #writer.writerow(data)
        print("write csv file complete!")

    def to_dataframe(self,list1,list2):
        df = pd.DataFrame({'Column1': list1, 'Column2': list2})
        df.to_csv('/out.csv') 
        return df


New = Search()
New.run()