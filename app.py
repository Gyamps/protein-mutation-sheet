"""Entry point of the application
    """

import sys
from utils import compare_aligned_sequences, spreadsheet_utils


def run():
    """Run the functions in the order needed based on user
    input
    """
    print("\t\tWELCOME TO THE ALIGNMENT CLUBHOUSE.\n")
    print("If you're here, then you want to compare the")
    print("positions of your isolates to the reference to")
    print("identify all the mutations, if any, and where they")
    print("occur.\n\n\n")

    while True:
        try:
            print("These are the options you can choose from:\n")
            print("\t1.Perform new Comparison.\n")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                print("\nCreating new workbook...")
                workbook, sheet = spreadsheet_utils.create_workbook()
                print("Workbook created!")

                print(
                    "\nProvide the path to the directory containing the protein alignments,"
                )
                print(
                    "after, enter the extension of the alignment files (Default is '.mfa')."
                )
                print(
                    "You then provide the reference sequence ID, after which you enter"
                )
                print("The desired name for which you'd like you file to be saved.")

                protein_alignments_path = input(
                    "Provide path to the protein alignments directory: "
                )
                extension = input("Enter the extension (Default is '.mfa'): ")
                ref_id = input("Enter your reference sequence ID: ")
                file_name = input("Output excel file name (DO NOT ADD AN EXTENSION): ")

                print("\nExtracting protein names as header columns...")
                try:
                    protein_names = spreadsheet_utils.extract_gene_name_from_file(
                        protein_alignments_path
                    )
                except FileNotFoundError:
                    print(f"No such file or directory: '{protein_alignments_path}'")
                    protein_alignments_path = input(
                        "Kindly enter the right file or directory: "
                    )
                    protein_names = spreadsheet_utils.extract_gene_name_from_file(
                        protein_alignments_path, extension
                    )

                if extension:
                    mutation_finder = (
                        compare_aligned_sequences.MultiFastaMutationsFinder(
                            protein_alignments_path,
                            sheet,
                            ref_id,
                            protein_names,
                            extension,
                        )
                    )
                else:
                    mutation_finder = (
                        compare_aligned_sequences.MultiFastaMutationsFinder(
                            protein_alignments_path,
                            sheet,
                            ref_id,
                            protein_names,
                            ".mfa",
                        )
                    )

                print("Processing Multi Fasta Alignment file...")
                mutation_finder.process_fasta_file()
                print("Inserting headers and Isolate IDs to excel...")
                mutation_finder.insert_ids_to_excel()
                print("Inserting data to excel sheet...")
                mutation_finder.insert_to_excel()

                # Save to spreadsheet
                spreadsheet_utils.save_worksheet(workbook, file_name + ".xlsx")
                print("\nExiting...")
                sys.exit(0)
            else:
                print("\nYour choice is not among the options listed.")
                print("Enter a choice in the options listed below.\n")
        except ValueError:
            print("\nError: Invalid input. Please enter an integer.\n")


if __name__ == "__main__":
    run()
