# Script is called LaTeXTable_from_csv.py
import pandas as pd


''' Beginning of Function latextable_from_csv() '''
def latextable_from_csv(csv_file, txt_file):
    # Save csv information into dataframe and open text file
    dataframe = pd.read_csv(csv_file)
    textfile = open(txt_file, 'w')

    # Writing general beginning of latex table
    textfile.write("\\begin{table}[htbp] \n")
    textfile.write("\t\\centering \n")
    textfile.write("\t\\captionsetup{skip=10pt} "
                   "% Space between caption and table \n")
    textfile.write("\t\\caption{ } \n\n")

    # General table information
    column_names = dataframe.columns.tolist()
    num_rows = len(dataframe)
    num_columns = len(column_names)

    # Beginning of tabular
    tabular_start = "\t\\begin{tabular}{|"
    for i in range(num_columns):
        column_entry = "c|"
        tabular_start = tabular_start + column_entry
    tabular_start = tabular_start + "} \n"
    textfile.write(tabular_start)

    # Entering column names
    textfile.write("\t\t\\hline \n")

    # Inputting warning message
    textfile.write("\t\t% LaTeX doesn't allow for underscores (_), "
                   "please change it before compiling \n")

    string_column_names = f"\t\t"
    for column_number in range(num_columns):
        name_addition = f"\\textbf{{{column_names[column_number]}}} & "
        name_addition = name_addition.replace('_', ' ')
        string_column_names = string_column_names + name_addition
    column_names_entry = string_column_names[:-2] + "\\\\ \n"
    textfile.write(column_names_entry)
    textfile.write("\t\t\\hline \n")

    # Entering table information
    for row_number in range(num_rows):
        row_string = f"\t\t"
        for i in range(num_columns):
            cell_info = dataframe.loc[row_number, column_names[i]]
            # Limiting to two decimal places if a floating point
            if isinstance(cell_info, float):
                cell_info = f"{cell_info:0.3f}"
            if isinstance(cell_info, str):
                cell_info = cell_info.replace('_', ' ')

            cell_entry = f"{cell_info} & "
            row_string = row_string + cell_entry
        # Getting rid of the last '&' and adding '\\'
        row_entry = row_string[:-2] + "\\\\ \n"
        textfile.write(row_entry)
        textfile.write("\t\t\\hline \n")

    textfile.write("\t\\end{tabular} \n")
    textfile.write("\\end{table} \n")

    textfile.close()
    print("csv file has been converted to latex")
    print(f"Result saved to: {txt_file} \n")


''' End of Function latextable_from_csv() '''

# File locations
csv_paths = [
    "Tensile-Results/Table_Categories.csv",
    "Tensile-Results/Table_Sequences_Sorted.csv",
]

txt_paths = [
    "Tensile-Results/Table_Categories.txt",
    "Tensile-Results/Table_Sequences_Sorted.txt",
]

# For loop iteration
for csv_location, txt_location in zip(csv_paths, txt_paths):
    latextable_from_csv(csv_location, txt_location)