#!/usr/bin/env python3

import csv

with open('Genes4DRanalysis.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    # Loop through each row in the CSV
    for row in csv_reader:
        direction = row['direction'].lower()
        gene_name = row['geneName']
        start = int(row['start'])
        stop = int(row['stop'])

        print(f"{gene_name},{direction},{start},{stop}")
