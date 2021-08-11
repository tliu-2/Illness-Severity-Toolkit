from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import pandas as pd
import Data_Headers as d
import Calculator as calc

entries = []
entrylabels = []
titles = []
dataset = None

def labels_for_entries():
    global entrylabels
    entrylabels.append('Study ID')
    entrylabels.append('Age')
    entrylabels.append('Cirrhosis')
    entrylabels.append('Cancer')
    entrylabels.append('AKI')
    entrylabels.append('Immunosup')
    entrylabels.append('GCS Visual')
    entrylabels.append('GCS Verbal')
    entrylabels.append('GCS Motor')
    entrylabels.append('Pulse High')
    entrylabels.append('Pulse Low')
    entrylabels.append('BP High')
    entrylabels.append('BP Low')
    entrylabels.append('Temp High')
    entrylabels.append('Temp Low')
    entrylabels.append('Resp Rate High')
    entrylabels.append('Resp Rate Low')
    entrylabels.append('High Art pO2')
    entrylabels.append('Low Art pO2')
    entrylabels.append('Mech Vent')
    entrylabels.append('High Art FiO2')
    entrylabels.append('Low Art FiO2')
    entrylabels.append('pCO2 High pH')
    entrylabels.append('pCO2 Low pH')
    entrylabels.append('High Hematocrit')
    entrylabels.append('Low Hematocrit')
    entrylabels.append('High WBC')
    entrylabels.append('Low WBC')
    entrylabels.append('High Na')
    entrylabels.append('Low Na')
    entrylabels.append('High Albumin')
    entrylabels.append('Low Albumin')
    entrylabels.append('Total Bilirubin')
    entrylabels.append('High Gluc')
    entrylabels.append('Low Gluc')
    entrylabels.append('High BUN')
    entrylabels.append('Low BUN')
    entrylabels.append('High Creatinine')
    entrylabels.append('Low Creatitine')
    entrylabels.append('Daily Outs')
    entrylabels.append('Lowest pH')
    entrylabels.append('Organtx')
    entrylabels.append('Sct')
    entrylabels.append('HIV')
    entrylabels.append('CD4')
    entrylabels.append('Prednisone')
    entrylabels.append('Prednisone Dose')


def runGUI():
    global entries, entrylabels

    x_ref = 0
    y_ref = 20
    x_dif = 100
    y_dif = 20

    lbl = Label(root, text="Import a .csv file from RedCap for APACHE scores.")
    lbl.pack(side=TOP)

    labels_for_entries()

    # Titles: For manual input of titles uncomment the for loop.

    # for i in range(len(entrylabels)):
    #     label = Label(root, text=entrylabels[i])
    #     label.place(x=x_ref, y=y_ref + i * y_dif)
    #     entry = tk.Entry(root)
    #     entry.place(x=x_ref + x_dif, y=y_ref + i * y_dif)
    #     entries.append(entry)


def quit():
    import sys
    sys.exit()


def getCSV():
    global entries, titles, dataset
    csvfile = filedialog.askopenfilename(title="Select a CSV File", filetypes=(("csv files", "*.csv"),))
    csvdf = pd.read_csv(csvfile)
    dataset = d.Data(csvdf)
    # calc.run(dataset)

def run():
    calc.run(dataset)

def retrieve_inputs():
    global entries, titles
    titles.clear()
    for x in range(len(entries)):
        entry = entries[x]
        titles.append(entry.get())


def apache_tab(tab_root):
    run_button = ttk.Button(tab_root, text='Run', command=run)
    run_button.pack()
    import_button = ttk.Button(tab_root, text='Import File', command=getCSV)
    import_button.pack()


if __name__ == '__main__':
    root = Tk()

    root.geometry("300x300")

    runGUI()

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


