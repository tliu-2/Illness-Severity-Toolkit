from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import APACHEIII_Calculator as apache_Calc
import SOFA_Calculator as sofa_Calc
import CCI_Calculator as cci_Calc

global df


def exit_program():
    import sys
    sys.exit()


def get_csv():
    global df
    csvfile = filedialog.askopenfilename(title="Select a CSV File", filetypes=(("csv files", "*.csv"),))
    df = pd.read_csv(csvfile, delimiter=',', encoding="latin1")


def run_apache():
    apache_Calc.run(df)

def run_sofa():
    sofa_Calc.run(df)

def run_cci():
    cci_Calc.run(df)

def apache_tab(tab_root):
    run_button = ttk.Button(tab_root, text='Run', command=run_apache)
    run_button.pack()
    import_button = ttk.Button(tab_root, text='Import File', command=get_csv)
    import_button.pack()


def sofa_tab(tab_root):
    run_button = ttk.Button(tab_root, text='Run', command=run_sofa)
    run_button.pack()
    import_button = ttk.Button(tab_root, text='Import File', command=get_csv)
    import_button.pack()

def cci_tab(tab_root):
    run_button = ttk.Button(tab_root, text="Run", command=run_cci)
    run_button.pack()
    import_button = ttk.Button(tab_root, text='Import File', command=get_csv)
    import_button.pack()

if __name__ == '__main__':
    root = Tk()

    root.geometry("300x300")
    tabControl = ttk.Notebook(root)
    apache = ttk.Frame(tabControl)
    sofa = ttk.Frame(tabControl)
    cci = ttk.Frame(tabControl)
    tabControl.add(apache, text='APACHE')
    tabControl.add(sofa, text='SOFA')
    tabControl.add(cci, text='CCI')
    tabControl.pack(expand=1, fill="both")

    apache_tab(apache)
    sofa_tab(sofa)
    cci_tab(cci)
    # setitles = Button(root, text='Set Titles', command=retrieve_inputs)

    btn = Button(root, text='Quit', command=exit_program)
    btn.pack()
    root.title('Wurfel Lab Tools')
    root.mainloop()
