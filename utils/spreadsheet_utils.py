"""Utilities for creating, loading, writing, saving, finding 
    occupied rows and columns and inserting headers to Spreadsheets
    """

import os
from openpyxl import Workbook


def create_workbook():
    """Function creates a workbook from which a
    Spreadsheet is made active for manipulation

        Returns:
            tuple: a Workbook object and Workbook child (sheet)
    """
    workbook = Workbook()
    return workbook


def save_worksheet(workbook: Workbook, filename: str):
    """Save changes to a worksheet

    Args:
        workbook (Workbook): Workbook object to invoke save method
        filename (str): Name to save file as. Specify path to save at particular place
    """
    workbook.save(filename)


def extract_gene_name_from_file(path: str, extension: str = ".mfa"):
    """Extract the name of the proteins from their multiple alignment file (MAF)
    filenames, which are saved by the Gene name and store them in a list

    Args:
        path (str): The directory where the protein files reside
        extension (str, optional): The extension of the multiple alignment files.
                                Defaults to '.mfa'
        first_column_name (str, optional): The name of the first column in the sheet.
                                Defaults to ''.
    """
    filenames = []
    for filename in os.listdir(path):
        if filename.endswith(extension):
            base_filename = os.path.splitext(filename)[0]
            filenames.append(base_filename)

    return filenames


def insert_data_to_excel(
    workbook: Workbook, mutations: list, sheet, start_row: int = 1, start_col: int = 1
):
    """Insert compared sequences into sheet.
    The compared sequences will normally arrive as a list of tuples
    from the compared_aligned_sequences function, which returns the
    sequence ID and the compared sequences.

    Args:
        workbook (Workbook): An instance of OpenpyXL workbook.
        data (list): A list of tuples of compared sequences.
        sheet (Workbook child): The sheet in question.
        start_row (int, optional): The row from which to start writing to. Defaults to 1.
        start_col (int, optional): The column to start writing to. Defaults to 1.
    """
    # Write data, handling the ID and mutation list structure
    for row_index, row_data in enumerate(mutations):
        # Write ID to the first column (adjust start_col if needed)
        sheet.cell(row=start_row, column=start_col + row_index).value = row_data[0]

        # Write mutation list to subsequent columns
        for col_index, char in enumerate(row_data[1]):
            sheet.cell(
                row=start_row + 1 + col_index, column=start_col + row_index
            ).value = char

    save_worksheet(workbook, "Mutation Sheet(2).xlsx")
