# **Exploratory Data Analysis (EDA) GUI Tool**

This project is a simple graphical user interface (GUI) application built with **Python**, **Tkinter**, **Pandas**, and **Matplotlib**.  
It serves as a showcase of my skills in **Python programming**, **basic GUI development**, and **exploratory data analysis (EDA)**.

The tool allows users to load CSV datasets and instantly generate plots and summary information—without writing a single line of code.

<img width="902" height="632" alt="EDA_scatterplot" src="https://github.com/user-attachments/assets/e2c5de00-9652-4dc6-9c4e-1e1a178195ed" />

---

## **Features**

### 🔹 **Load CSV Datasets**
- Enter the dataset name (without the `.csv` extension).
- The program automatically looks for the file in the same directory as the script.
- Displays `df.info()` in the main text area.
- Handles missing or invalid files with clear error messages.

### 🔹 **Automatic Plot Selection**
Based on the number and type of variables entered, the tool automatically chooses the most appropriate plot:

| Number of Variables | Plot Type | Description |
|---------------------|-----------|-------------|
| **1 variable** | Histogram or Bar Plot | Numeric variables → histogram; categorical → bar chart |
| **2 variables** | Scatter Plot | Basic bivariate visualization |
| **3 variables** | Colored Scatter Plot | Scatter plot with color mapping using the third variable |
| **4+ variables** | Correlation Heatmap | Categorical variables are automatically encoded |

### 🔹 **Additional Highlights**
- Automatic type detection for numeric vs. categorical variables  
- Encoding of categorical variables when needed  
- Inline Matplotlib rendering inside the Tkinter window  
- Dynamic plot replacement (old plot removed before rendering a new one)  
- Clean error handling and user feedback panel

---

## **How It Works**

### **1. Load a Dataset**
In the upper-left area of the GUI:
1. Type the dataset name (e.g., `Iris`)
2. Click **"Laden"**

The tool will:
- Read `Iris.csv`
- Display structural information via `df.info()`
- Confirm successful loading

### **2. Generate Plots**
In the right plotting area:
1. Enter one or more column names (separated by spaces)
2. Click **"Ausführen"**

Examples:
```
sepal_length
species
age height
x y z
```

The tool responds dynamically depending on your input.

---

## **GUI Layout**

The interface consists of four main sections:

1. **Dataset Input Panel** – For typing CSV names  
2. **Message Panel** – Displays success/error messages  
3. **Dataset Info Panel** – Shows `df.info()`  
4. **Plot Panel** – Renders Matplotlib figures based on user input  

---

## **Technologies Used**

- **Python 3**
- **Tkinter** – GUI framework  
- **Pandas** – Data handling  
- **Matplotlib** – Plotting  
- **Seaborn** – Heatmap visualization  
- **NumPy** – Numeric utilities  
- **Pathlib** – File path handling  

---

## **Project Structure**

```
Python-GUI-EDA-Tool/
│
├── EDA.py
├── Iris.csv
├── student_exam_scores.csv
├── README.md
```

---

## **How to Run**

1. Clone the repository:
```bash
git clone https://github.com/SchmSe/Python-GUI-EDA-Tool.git
```

2. Install dependencies:
```bash
pip install pandas matplotlib seaborn
```

3. Run the application:
```bash
python EDA.py
```

4. Make sure your CSV files are located in the same directory as `EDA.py`.

---

## **Screenshots**

<img width="902" height="632" alt="EDA_histplot" src="https://github.com/user-attachments/assets/44e91258-7950-4b14-8e9d-98e401b202e0" />
<img width="902" height="632" alt="EDA_heatmap" src="https://github.com/user-attachments/assets/fd71d0cc-5d17-443d-b13d-2c0566dded3b" />

---
