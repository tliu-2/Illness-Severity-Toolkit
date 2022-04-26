from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import APACHEIII_Calculator as apache_Calc
import SOFA_Calculator as sofa_Calc
import CCI_Calculator as cci_Calc
import VFDs
import oxygenation

global df


def exit_program():
    import sys
    sys.exit()


def get_csv():
    global df
    csvfile = filedialog.askopenfilename(title="Select a CSV File", filetypes=(("csv files", "*.csv"),))
    df = pd.read_csv(csvfile, delimiter=',', encoding="latin1")


# Run Wrappers.
def run_apache():
    apache_Calc.run(df)


def run_sofa():
    sofa_Calc.run(df)


def run_cci():
    cci_Calc.run(df)


def run_vfds():
    VFDs.run(df)


def run_oi():
    oxygenation.run(df)


def run_button(tab_root, run_type):
    run_button = ttk.Button(tab_root, text='Run', command=run_type)
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
    vfds = ttk.Frame(tabControl)
    oi = ttk.Frame(tabControl)

    tabControl.add(apache, text='APACHE')
    tabControl.add(sofa, text='SOFA')
    tabControl.add(cci, text='CCI')
    tabControl.add(vfds, text="VFDs")
    tabControl.add(oi, text="Oxygenation Index")
    tabControl.pack(expand=1, fill="both")

    run_button(apache, run_apache)
    run_button(sofa, run_sofa)
    run_button(cci, run_cci)
    run_button(vfds, run_vfds)
    run_button(oi, run_oi)
    # setitles = Button(root, text='Set Titles', command=retrieve_inputs)

    btn = Button(root, text='Quit', command=exit_program)
    btn.pack()
    root.title('Wurfel Lab Tools')
    root.mainloop()
