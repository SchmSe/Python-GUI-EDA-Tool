import tkinter as tk
import pandas as pd
from pathlib import Path
from contextlib import redirect_stdout
import io
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

canvas= None

#Only two functions needed: one to display the most important characteristics, and one for the plots
def laden():
    '''
    This function loads the csv-dataset, which is specified by the user via textinput.
    The dataset gets saved as "df", a pandas dataframe.
    There are two outputs: a success promt in the information area of the GUI,
    and df.info() inside the big "anzeige_frame".
    In case of Errors, both widows show differrent texts.
    '''
    global df
    global output_text_widget
    try:
        #Reading the user input
        output_text_widget.delete('1.0', tk.END)
        eingabe = eingabe_datensatz.get()
        eingabe = eingabe + ".csv"
        #Getting the path, where the script is executed
        skript_pfad = Path(__file__).parent
        dateipfad = skript_pfad / eingabe
        df = pd.read_csv(dateipfad)
        #Writing the df.info into a displayable format
        f = io.StringIO()
        with redirect_stdout(f):
            df.info()
        info_string = f.getvalue()
        #Ouputs
        output_text_widget.insert('1.0', info_string)
        output_text.set(f"Datensatz {eingabe} geladen!")

    #Try/except in case a file doesn't exist or an unexpectet error occures
    except FileNotFoundError:
        output_text_widget.delete('1.0', tk.END) 
        output_text_widget.insert('1.0', f"FEHLER: Datei '{eingabe}' nicht gefunden.")
        output_text.set("Fehler!")
    except Exception as e:
        output_text_widget.delete('1.0', tk.END)
        output_text_widget.insert('1.0', f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        output_text.set("Fehler!")

#The second function is the more important one. Some features were added after the initial idea.
#In a new programm, ideally anzeige() would call smaller functions for each len(var_liste).

def anzeige():
    '''
    This functions gets variable inputs by the user and prints plots to the "bild_frame" window.
    If one variable with an int/float datatype is entered, the function shows a plt.hist with up to 10 bins.
    If one variable with a categorial datatype is entered, the function shows a barplot.
    For two variables, the function shows a scatterplot
    For three variables, the function shows a scatterplot, colored by the third variable.
    For four and more variables, the function shows a regression heatmap.
    '''
    global df
    global eingabe_bild
    global output_text
    global bild_frame
    global canvas

    #Clearing canvas first, in case its not the first use after opening the programm.
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

    #Try/except in case of errors.
    try:
        #Showing massages for common mistakes.
        if "df" not in globals():
            output_text.set("Fehler, bitte erst den Datensatz laden!")
            return

        #Reading input
        variable = eingabe_bild.get().strip()
        if not variable:
            output_text.set("Fehler, bitte erst einen Variablennamen eingeben!")
            return
        
        #Splitting the input for more then one variable. Doesn't make a difference, if len() = 1.
        var_liste = variable.split()
        anzahl = len(var_liste)

        #Checking of misspelled variable names.
        for name in var_liste:
            if name not in df.columns:
                output_text.set("Fehler, kann Variable nicht finden!")
                return
    
        #len() = 1 : Barplot/hist, depending on datatype.
        if anzahl == 1:
            #setting up the area to draw the plot in.
            fig = Figure(figsize=(5,4), dpi = 100)
            fig.set_facecolor("#f0f0f0")
            ax = fig.add_subplot(111)
            #plot for int and float data         
            if df[variable].dtype in ["float64", "int64"]:
                ax.hist(df[variable], bins = 10, edgecolor = "black")
                ax.set_xlabel(variable)
                ax.set_ylabel("Häufigkeit")
            #plot for categorial data
            else:
                haufigkeiten = df[variable].value_counts().sort_index()
                haufigkeiten.plot(kind = "bar", ax = ax)
                ax.set_xlabel(variable)
                ax.set_ylabel("Anzahl")
            #tight layout and xlabel roatation to fit in the "bild_frame"
            fig.autofmt_xdate(rotation = 45)
            fig.tight_layout()
            #text for the small text window. df.info() stays at the "anzeige_frame"
            output_text.set(f"Verteilung für {variable} wird angezeigt.")

        #len() = 2 : Scatterplot
        elif anzahl == 2:
            #getting variables-names from the list
            var_x = var_liste[0]
            var_y = var_liste[1]
            #setting up the area to draw the plot in.
            fig = Figure(figsize=(4,3.5), dpi=100)
            fig.set_facecolor("#f0f0f0")
            ax = fig.add_subplot(111)
            #scatterplot, point size 20
            scatter = ax.scatter(df[var_x], df[var_y], s = 20)
            #x/y label, tight layout
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)
            fig.tight_layout()
            #text for the small text window. df.info() stays at the "anzeige_frame"
            output_text.set(f"Scatter Plot für '{var_x}', '{var_y}' erstellt.")

        #len() = 3 : Scatterplot colored by a third variable
        elif anzahl == 3:
            #getting variables-names from the list
            var_x = var_liste[0]
            var_y = var_liste[1]
            var_col = var_liste[2]

            #transforming the third variable, if it isnt int or float and setting up cmap
            if df[var_col].dtype == "object" or isinstance(df[var_col].dtype, pd.CategoricalDtype):
                c_data = df[var_col].astype("category").cat.codes
                cmap_name = "viridis"
                discrete_cbar = True
            else:
                c_data = df[var_col]
                cmap_name = "viridis"
                discrete_cbar = False
            #setting up the area to draw the plot in.
            fig = Figure(figsize=(4,3.5), dpi=100)
            fig.set_facecolor("#f0f0f0")
            ax = fig.add_subplot(111)
            #scatterplot. pointsize 20, colored by third variable
            scatter = ax.scatter(df[var_x], df[var_y], c=c_data, cmap=cmap_name, s = 20)
            cbar = fig.colorbar(scatter, ax=ax, label=var_col)
            #colorbar labels and range for previous categorial variables
            if discrete_cbar:
                category_names = df[var_col].astype("category").cat.categories
                cbar.set_ticks(np.unique(c_data))
                cbar.set_ticklabels(category_names)
            #labels and layout
            ax.set_xlabel(var_x)
            ax.set_ylabel(var_y)
            fig.tight_layout()
            #text for the small text window. df.info() stays at the "anzeige_frame"
            output_text.set(f"Scatter Plot für '{var_x}', '{var_y}', '{var_col}' erstellt.")
        
        #len() = 3 : Correlation Heatmap
        elif anzahl > 3:
            #copy of df for transformations
            df_neu = df[var_liste].copy()
            #transformation of all variables in var_liste, if not float or int (for cor())
            for column in df_neu.columns: 
                if df_neu[column].dtype == "object" or isinstance(df_neu[column].dtype, pd.CategoricalDtype):
                    df_neu[column] = df_neu[column].astype("category").cat.codes
            corr = df_neu.corr()
            #setting up the area to draw the plot in.
            fig = Figure(figsize=(5,4), dpi=100)
            fig.set_facecolor("#f0f0f0")
            ax = fig.add_subplot(111)
            #heatmap for corr()
            sns.heatmap(corr, annot = True, cmap = "YlGnBu", square = True, ax = ax)
            #labels and layout
            ax.tick_params(axis='x', rotation=45) 
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()
            #text for the small text window. df.info() stays at the "anzeige_frame"
            output_text.set("Heatmap erstellt!")

        else:
            #if not except, minor error
            #text for the small text window. df.info() stays at the "anzeige_frame"
            output_text.set("Fehler, kann Befehl nicht ausführen!")
            return

        #drawing the plot in "bild_frame"
        canvas = FigureCanvasTkAgg(fig, master=bild_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand = True)
        canvas.draw()
    
    except Exception as e:
        #text for the small text window. df.info() stays at the "anzeige_frame"
        output_text.set(f"Fehler: {e}")


# GUI Part I: General setup 2x2 grid
root = tk.Tk()
root.title("EDA Tool")
root.geometry("900x600")

root.grid_rowconfigure(0, weight=0) 
root.grid_columnconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# GUI Part II: input frame, that asks for the Dataset name and has a button "laden", that executes laden()
linker_frame = tk.Frame(root, width= 400, height= 60)
linker_frame.grid(row=0, column=1, sticky='nw', padx=5, pady=5)
linker_frame.pack_propagate(False)

label_datensatz_laden = tk.Label(linker_frame, text="Datensatz laden:")
label_datensatz_laden.pack(side=tk.TOP, padx=5)

eingabe_datensatz = tk.Entry(linker_frame, width=30)
eingabe_datensatz.pack(side=tk.TOP, padx=5, fill="x")

laden = tk.Button(linker_frame, text="Laden", command=laden)
laden.pack(side=tk.TOP, padx=5)

# GUI Part III: Small text frame. Displays errors while a dataset is loaded (i.e. var not found)
rechter_frame = tk.Frame(root, width= 450, height= 60)
rechter_frame.grid(row=0, column=2, sticky='nw', padx=0, pady=0)
rechter_frame.pack_propagate(False)

label_datensatz_laden = tk.Label(rechter_frame, text="Aktuelle Meldung:")
label_datensatz_laden.pack(side=tk.TOP, padx=5)

output_text = tk.StringVar()
output_text.set("Willkommen! Datensatz-Dateinamen ohne '.csv' eingeben!")

label_output = tk.Label(rechter_frame, textvariable=output_text, justify=tk.LEFT, anchor="center")
label_output.pack(fill="both")

# GUI Part IV: Big text frame, showing df.info(), scrollable
anzeige_frame = tk.Frame(root, width= 400, height= 550, highlightthickness=1, highlightbackground="black", highlightcolor="black", relief=tk.FLAT)
anzeige_frame.grid(row=1, column=1, sticky='nw', padx=5, pady=5)
anzeige_frame.pack_propagate(False)

output_text_widget = tk.Text(anzeige_frame, wrap=tk.WORD, height=20, width=30, bg="#f0f0f0")
output_text_widget.pack(fill="both", expand=True, padx=5, pady=5)

# GUI Part V: frame that consists of the var input for plots and shows the plots
bild_frame = tk.Frame(root, width= 450, height= 550, highlightthickness=1, highlightbackground="black", highlightcolor="black", relief=tk.FLAT)
bild_frame.grid(row=1, column=2, sticky='nw', padx=5, pady=5)
bild_frame.pack_propagate(False)
eingabe_bild_frame = tk.Label(bild_frame, text="Bitte Variable eingeben:")
eingabe_bild_frame.pack(side=tk.TOP, padx=5)

eingabe_bild = tk.Entry(bild_frame)
eingabe_bild.pack(side=tk.TOP, padx=5, fill = "x")

losgehts = tk.Button(bild_frame, text="Ausführen", command=anzeige)
losgehts.pack(side=tk.TOP, padx=5)


# GUI Part VI: Execution of the main loop.
root.mainloop()