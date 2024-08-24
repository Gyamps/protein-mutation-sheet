#!/usr/bin/env python3

import pandas as pd

excel_file = "Genes4DRanalysis.xlsx"

sheet_name = 'Sheet1'

df = pd.read_excel(excel_file, sheet_name=sheet_name)

csv_file = "Genes4DRanalysis.csv"
df.to_csv(csv_file, index=False)
