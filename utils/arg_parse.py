import argparse, sys, os
from termcolor import colored

class ParseWithErrors(argparse.ArgumentParser):
    def error(self, message):
        print(colored("ERROR", "red", "on_white", attrs=["bold"]) + " " + colored(f"{message}\n", "red"))
        self.print_help()
        sys.exit(2)

    @staticmethod
    def is_valid_file(parser, arg):
        """
        Check if the file being parsed is valid
        @param parser: an argument parser object
        @param arg: the argument (file) being supplied
        @return: arg
        """
        if not os.path.isfile(arg):
            parser.error(f"The file {arg} does not exist!")
        else:
            return arg

    @staticmethod
    def directory_exists(parser, arg):
        """
        Check if the directory being parsed is valid
        @param parser: an argument parser object
        @param arg: the argument (directory) being supplied
        @return: arg
        """
        if not os.path.isdir(arg):
            parser.error(f'The directory "{arg}" does not exist!')
        else:
            return arg

def argparser():
    """
    Parse argument from command line
    """
    description = """
    A script to parse protein MFA files to
    compare to a translated reference genome for
    mutations. 
    """
    parser = ParseWithErrors(description=description)
    parser.add_argument("-p", "--protein_alignment_dir", required=True,
                        help="path to protein alignments directory",
                        type=lambda x: parser.directory_exists(parser, x))
    parser.add_argument("-e", "--extension", required=False, default=".mfa",
                        help="the multi fasta file extension [Optional] [Default: \".mfa\"]")
    parser.add_argument("-o", "--output_excel_file", required=True,
                        help="output fasta file name WITHOUT extension")

    return parser

def dr_genes_argparser():
    description = """
    A script to parse an aligned genomes Fasta file to
    have its genes extracted into separate files.
    """
    parser = ParseWithErrors(description=description)
    parser.add_argument("-i", "--input_fasta_file", required=True,
                        help="input fasta file",
                        type=lambda x: parser.is_valid_file(parser, x))

    return parser