"""Entry point of the application
    """

from sys import exit
from utils import compare_aligned_sequences, spreadsheet_utils, arg_parse


def run(protein_alignments_path, extension, output_file_name) -> None:
    """Run the functions in the order needed based on user
    input

    Args:
        protein_alignments_path (str): path to the protein alignments file
        extension (str): extension of the protein alignments file
        output_file_name (str): name of the output file
    @return: None
    """
    print("\nCreating new workbook...")
    workbook, sheet = spreadsheet_utils.create_workbook()
    print("Workbook created!")

    print("\nExtracting protein names as header columns...")
    protein_names = spreadsheet_utils.extract_gene_name_from_file(protein_alignments_path)

    mutation_finder = (
            compare_aligned_sequences.MultiFastaMutationsFinder(
                protein_alignments_path,
                sheet,
                protein_names,
                extension,
            )
    )

    print("Processing Multi Fasta Alignment file...")
    mutation_finder.process_fasta_file()
    print("Inserting headers and Isolate IDs to excel...")
    mutation_finder.insert_ids_to_excel()
    print("Inserting data to excel sheet...")
    mutation_finder.insert_to_excel()

    # Save to spreadsheet
    spreadsheet_utils.save_worksheet(workbook, output_file_name + ".xlsx")
    # Save spreadsheet to csv
    spreadsheet_utils.excel_to_csv(output_file_name + ".xlsx", "Sheet")
    print("\nExiting...")
    exit(0)


if __name__ == "__main__":
    parser = arg_parse.argparser()
    args = parser.parse_args()

    run(args.protein_alignment_dir, args.extension, args.output_excel_file)
