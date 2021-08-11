from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import pandas as pd
import Data_Headers as d
import Calculator as calc

global df

def quit():
    import sys
    sys.exit()


def getCSV():
    global df
    csvfile = filedialog.askopenfilename(title="Select a CSV File", filetypes=(("csv files", "*.csv"),))
    csvdf = pd.read_csv(csvfile)
    df = csvdf
    # dataset = d.Data(csvdf)
    # calc.run(dataset)

def run():
    calc.run(dataset)

def apache_tab(tab_root):
    run_button = ttk.Button(tab_root, text='Run', command=run)
    run_button.pack()
    import_button = ttk.Button(tab_root, text='Import File', command=getCSV)
    import_button.pack()


if __name__ == '__main__':
    root = Tk()

    root.geometry("300x300")
    tabControl = ttk.Notebook(root)
    apache = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tabControl.add(apache, text='APACHE')
    tabControl.add(tab2, text='Tab 2')
    tabControl.pack(expand=1, fill="both")

    apache_tab(apache)
    # setitles = Button(root, text='Set Titles', command=retrieve_inputs)

    btn = Button(root, text='Quit', command=quit)
    btn.pack()
    root.title('Wurfel Lab Tools')
    root.mainloop()


