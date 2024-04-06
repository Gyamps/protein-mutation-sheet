## General Info

This project takes a Multiple Sequence Alignment file, parses it
and compares each isolate's gene sequence to that of the reference
sequence to check for mutations, which are stored in an excel spreadsheet.

If a position in the isolate's sequence matches exactly with that
of the reference or it does not exist ("X"), then the final sheet has an
"X" placed there.

In the event of a mutation, the original letter in the reference sequence
is written then the position where the mutation happened is included and
then the mutation itself is written. So, say in the reference, at position
1, a "V" exists, but in the isolate's sequence, a "P" exists instead, it is
recorded as "V1P".

## Technologies

The project is created with:

- Python: 3.11.5
- biopython 1.83
- openpyxl: 3.1.2

Any Python 3 version might suffice actually

## Setup

To run this project, you have to first install the core modules needed
for its proper functioning from the "requirements.txt" file, then run
the tool from its entry point and voila!!

Make sure you're doing all these form the projects root directory.

```
$ pip install -r requirements.txt
$ python3 app.py
```
