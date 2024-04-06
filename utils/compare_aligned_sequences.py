"""Utilities for manipulating Multiple Sequence Alignment
    and comparing the characters at each position to account for
    mutations.
    """

import os
from Bio import SeqIO
from utils.spreadsheet_utils import insert_data_to_excel


def compare_aligned_sequences(isolate_seq: str, ref_seq: str):
    """Compare the sequences of the alignments to the reference seq,
    for mutations.
    If all the characters match that of the ref, then write an 'X',
    If all characters match but an 'X' exists along, then
    store an 'X' just like before.
    If a different character is present aside that in the reference,
    then indicate the original character in ref, the position of the
    mutation and the mutation character.
    NB: At each position, there may exist multiple mutations so note that.

    Args:
        isolate_seq (str): The isolate's sequence.
        ref_seq (str): The reference sequence.
    """
    mutations = []
    for i, _ in enumerate(isolate_seq):
        if isolate_seq[i] == "X" or (isolate_seq[i] == ref_seq[i]):
            mutations.append("X")
        elif isolate_seq[i] != ref_seq[i]:
            mutations.append(f"{ref_seq[i]}{i+1}{isolate_seq[i]}")

    return mutations


def parse_msa(
    path: str, workbook, ref_id: str, protein_names: list, extension: str = ".mfa"
):
    """Iterate through the protein list, then parse the Multi Sequence
    Alignment using Biopython's SeqIO, compare aligned sequences and
    then insert to corresponding excel sheet.

    Args:
        path (str): The path to the multi sequence alignment files.
        workbook: The OpenpyXL workbook object.
        ref_id (str): The reference sequence ID.
        protein_names (list): A list of the protein names (extracted from the MSA files).
        extension (str, optional): The extension of the MAF. Defaults to '.mfa'.
    """
    for protein in protein_names:
        print(f"\nCreating {protein} sheet...")
        sheet = workbook.create_sheet(title=protein)
        print("Done!")

        mutations = list()
        file = os.path.join(path, protein + extension)
        if file.endswith(extension):
            # Create a dictionary with record IDs as keys
            # and sequence as value.
            with open(file, "r") as handle:
                sequences = {
                    record.id: str(record.seq)
                    for record in SeqIO.parse(handle, "fasta")
                }

                # try to get the ref sequences using the ref ID from the
                # sequences dict. If it's not found, then get its equivalent,
                # which is "H37Rv", else, return an empty string
                if ref_id in sequences:
                    ref_seq = sequences[ref_id]
                else:
                    ref_seq = sequences.get("H37Rv", "")

                if ref_seq:
                    print("Done parsing MSA!")
                    print("Comparing aligned sequences...")

                    # Iterate through sequences dictionary, check
                    # if current ID is that of the reference. If not,
                    # create tuple of sequence ID and comparison of
                    # isolate's seq to ref seq and append to list.
                    for seq_id, seq in sequences.items():
                        if seq_id != ref_id:
                            mutations.append(
                                (seq_id, compare_aligned_sequences(seq, ref_seq))
                            )
                    print("\nNow inserting data to excel...")
                    insert_data_to_excel(workbook, mutations, sheet)
                    print("Mutations successfully inserted into sheet...")
                    print("Done with insertion!")
                else:
                    print("\nCould not find reference!")
                    print("Exiting...")
                    return False

    return True
