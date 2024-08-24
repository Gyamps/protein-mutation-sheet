## General Info

These scripts are written to aid in the entire TB pipeline.
The scripts are meant to extract stretches of the DNA sequence (genes) and then
translate them into **amino acids**. The results are then appended into a 
**Multi-FASTA** file whose names are that of the protein for which the gene
encodes.

The script takes genome *isolates* that have been aligned against the _M. TB_
reference genome and the _reference genome_ itself as inputs. You already know
how the output is supposed to be like from earlier, so here's a screen-recording of
that below:

![A Multi-FASTA file containing sequences of amino acids that translate to the
katG protein](./images/protein_mfa_lower.gif)

So the screen-recording above is the sequence of _amino acids_ that encode for
the **katG protein** in _M. Tuberculosis_. The isolates that were sequenced have
their IDs appearing before each sequence as shown and at the very bottom, the
reference has its own being included as well.

From here, the saved _".mfa"_ file is then used as inputs to the python scripts
which check for possible mutations.

There are two scripts at work here:
- The **parse_gene_data.py** script,
- and the **extract_DR_genes.sh** script.

## How the Scripts work
### _parse_gene_data.py_
This python script parses a csv file containing data on the proteins in TB.
The files headers are **_drug, geneName, direction, start, stop_**
- **drug**: This refers to the drug typically used to counter the protein in
question.
- **geneName**: Refers to the gene that encodes for the protein.
- **direction**: Refers to the direction on the DNA that is read to code for
the gene (protein).
- **start**: The point on the DNA where reading starts to prepare to code for
the gene (protein).
- **stop**: The point on the DNA where reading stops so the transcription and
translation can occur to produce the gene (protein).

This script iterates through the csv file and prints out the values that belong
to these headers. The output is passed to the bash script next.

 **NB: I am not a biology expert, so forgive me or correct me if possible when
I have made a blunder in my explanation.**

### _extract_DR_genes.sh_
This script takes the output of that above as well as the directory that 
contains the isolates' FASTA files and then extracts the sequence from
the start to the end codon. Based on the direction, finds the reverse compliment
of the extracted sequence and then finally translates the sequence into amino
acids.

**_NOTE_** that the script depends on these 3 commandline tools
**_extractseq, revseq and transeq_**, which perform the actions described above
and can be obtained from the
**EMBOSS (European Molecular Biology Open Software Suite)** package.

I use _Ubuntu_, a Linux distro that uses **apt** and **apt-get** to manage its
packages. Hence, the tools are downloaded using the command:
```commandline
sudo apt-get install emboss
```
You can then very the installation by running these one at a time:
```commandline
extractseq -h
revseq -h
transeq -h
```
Or, check this directory to see if your tools were installed:
```
/usr/lib/emboss/
```

The csv file which contains the headers listed earlier is included. It's saved
as **Genes4DRanalysis.csv**. Its equivalent Excel file is also included.
