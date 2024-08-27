#!/usr/bin/env python

"""
Utility for extracting certain genes from the Mycobacterium Tuberculosis
genome (isolates and reference) and saving the resultant files according to the
protein names in a specified directory.
"""

import subprocess
import sys
import os
import glob
import shutil
import csv
from os import PathLike

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from termcolor import colored
import arg_parse


class ExtractDrGenes:
    """
    Extract M. Tuberculosis genes from a multi-FASTA file
    containing the isolates' and reference genome.
    The output is a directory containing a multi-FASTA file of
    each protein and the sequences that relate to it.
    """

    def __init__(self, fasta_file: PathLike[str]) -> None:
        """
        Constructor

        @param fasta_file: A multi-FASTA file containing the genome of
        the isolates and that of the reference genome.
        """
        self.fasta_file = fasta_file
        self.temp_files = []

    def process_fasta_file(self) -> None:
        """
        Process the multi-FASTA file containing the genome of the TB isolates
        and the reference to extract the necessary genes - this is based on the
        "direction (of gene/protein on genome), start position and stop position"
        @return: None
        """
        with open(self.fasta_file) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                seq_id = record.id
                seq = record.seq

                record = SeqRecord(Seq(seq), id=seq_id)
                temp_file_name = seq_id + ".fasta"
                self.temp_files.append(temp_file_name)
                self.write_sequences_to_temp_file(record, temp_file_name)

                # Loop through each row in the CSV
                for row in self.parse_gene_data():
                    direction = row['direction'].lower()
                    gene_name = row['geneName']
                    start = int(row['start'])
                    stop = int(row['stop'])

                    if direction == "rev":
                        self.extract_and_process(temp_file_name, start, stop, gene_name, reverse=True)
                    elif direction == "forw":
                        self.extract_and_process(temp_file_name, start, stop, gene_name)
                    else:
                        sys.exit(f"Invalid direction: {direction}. Must be either 'rev' or 'forw'.")

                    self.append_to_mfa(gene_name, seq_id)

    def extract_and_process(self, seq_file: PathLike[str], start: int, stop: int, gene_name: str,
                            reverse: bool = False) -> None:
        """
        Extract the genes from the isolate's genome via the start and stop
        position, then, depending on the direction the gene is found, you get
        the reverse compliment of the gene, then you translate them into their
        Amino Acid equivalents, or you translate them straight away.
        All these are stored in intermediate files.

        @param seq_file: Temporary FASTA file containing the Isolate's or reference's genome
        @param start: The start point on the genome where the gene is located.
        @param stop: The stop point on the genome where the gene is located.
        @param gene_name: The name of the gene (or Protein).
        @param reverse: Boolean value to determine whether to find the reverse compliment of the gene or not.
        @return: None
        """
        outseq_file = f"{gene_name}.{'rvc' if reverse else 'rv'}.fasta"

        # Run extractseq command
        result = self.run_emboss_command('extractseq', '-sequence', f'{seq_file}', '-regions', f"{start}-{stop}",
                                         '-outseq',
                                         outseq_file)
        if result.returncode != 0:
            sys.exit(f"Error in extractseq: {result.stderr}")

        # If reverse if ture, run revseq
        if reverse:
            revseq_file = f"{gene_name}.rvc_RV.fasta"
            result = self.run_emboss_command('revseq', '-sequence', outseq_file, '-outseq', revseq_file)
            if result.returncode != 0:
                sys.exit(f"Error in revseq: {result.stderr}")

            outseq_file = revseq_file

        # Run transeq command
        result = self.run_emboss_command('transeq', '-sequence', outseq_file, '-outseq', f'{gene_name}.transl.fasta')
        if result.returncode != 0:
            sys.exit(f"Error in transeq: {result.stderr}")

    @staticmethod
    def write_sequences_to_temp_file(seq_record, file_name):
        SeqIO.write(seq_record, file_name, "fasta")

    @staticmethod
    def run_emboss_command(command, *args):
        # Construct the full command with arguments
        full_command = [command] + list(args)

        # Run the command
        result = subprocess.run(full_command, capture_output=True, text=True)

        return result

    @staticmethod
    def parse_gene_data():
        """
        Parse the csv file containing information on the gene
        and its location in the genome.
        """
        # Get directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Path to the CSV file
        csv_file_path = os.path.join(script_dir, "../bash_scripts/Genes4DRanalysis.csv")

        # Normalize the path
        csv_file_path = os.path.normpath(csv_file_path)

        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            data = list(csv_reader)

        return data

    @staticmethod
    def append_to_mfa(gene_name, seq_id):
        """Append the output of transeq to the `gene_name.fasta` file"""
        with open(f"{gene_name}.transl.fasta", 'r') as transeq_file:
            transl_fasta = transeq_file.read()
        with open(f"{gene_name}.mfa", 'a') as fasta_file:
            fasta_file.write(transl_fasta)

    def clean_up(self):
        """
        Delete temporary files as well as intermediate files used.
        """
        print("Cleaning up temp files")
        files_to_delete = []

        extractseq_rvc_files = glob.glob("*.rvc.fasta")
        extractseq_rv_files = glob.glob("*.rv.fasta")
        revseq_files = glob.glob("*.rvc_RV.fasta")
        transeq_files = glob.glob("*.transl.fasta")

        files_to_delete.extend(extractseq_rvc_files)
        files_to_delete.extend(extractseq_rv_files)
        files_to_delete.extend(revseq_files)
        files_to_delete.extend(transeq_files)
        files_to_delete.extend(self.temp_files)

        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted {file}")

    @staticmethod
    def move_files():
        """Move protein .mfa files into a protein_mfa directory"""
        print("Moving .mfa files")
        protein_mfa = []

        os.mkdir("protein_mfa")
        protein_mfa.extend(glob.glob("*.mfa"))

        for file in protein_mfa:
            shutil.move(file, "./protein_mfa/")

    @staticmethod
    def commands_exist():
        """Check if EMBOSS commands exists on the system."""

    emboss_commands = ["extractseq", "revseq", "transeq"]
    command_installed = []

    for command in emboss_commands:
        command_installed.append(subprocess.call(f"command -v {command}", shell=True, stdout=subprocess.DEVNULL,
                                                 stderr=subprocess.DEVNULL) == 0)

    if all(command_installed):
        print('Commands "extractseq", "revseq", and "transeq" exist on the system.')
    else:
        error_text = f"One or more commands in {emboss_commands} are missing."
        print(colored("ERROR ", "red", "on_white", attrs=["bold"]) + colored(error_text, "red"))
        sys.exit(1)


if __name__ == "__main__":
    parser = arg_parse.dr_genes_argparser()
    arguments = parser.parse_args()

    extract_genes = ExtractDrGenes(arguments.input_fasta_file)
    extract_genes.commands_exist()
    extract_genes.process_fasta_file()
    extract_genes.move_files()
    extract_genes.clean_up()
