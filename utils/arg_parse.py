import argparse, sys, os

class ParseWithErrors(argparse.ArgumentParser):
    def error(self, message):
        print('{0}\n\n'.format(message))
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
            parser.error("The file %s does not exist!" % arg)
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
            parser.error("The directory does not exist!" % arg)
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