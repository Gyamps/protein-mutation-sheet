#!/usr/bin/env bash

# The line below only applies when working on an HPC
# module load bioinfo/emboss/6.6

# Set the output of CSV file with "geneName, direction, start and stop"
# from python script.
output=$(./parse_gene_data.py)

# Path to MTBC Isolate FASTA files, defaulting to "../MTBC_fastafiles/" if not provided as an argument.
FASTA_FILES_LOC="${1:-"./MTBC_fastafiles/"}"

SUCCESS=0
ERR_CD=10
ERR_CMD_MISSING=20
ERR_INVALID_DIRECTION=30

# Create a directory for protein FASTA files if it doesn't exist.
mkdir -vp "protein_fastafiles"
# Exit program if directory to change into doesn't exist.
cd "protein_fastafiles" || exit "$ERR_CD"


# Check if commands for the work exist
# Redirection to /dev/null is more for me than you.
# It discards the all data written to it and hence the output
# from "command -v ..." is discard/disappears.
# shellcheck disable=SC2073
if [ "$(command -v extractseq)" > /dev/null ] && \
    [ "$(command -v revseq)" > /dev/null ] && \
    [ "$(command -v transeq)" > /dev/null ];
then
    echo "Commands \"extractseq\", \"revseq\" and \"transeq\" exist on system."
else
    echo "One or more commands in [\"extractseq\", \"revseq\" and \"transeq\"] are missing."
    exit "$ERR_CMD_MISSING"
fi


# Iterate through your sample's fast files (should normally be the consensus sequence)
for FILE in "${FASTA_FILES_LOC}"*.fas; do
    # Extract the base name of the file (name of file without extension)
    base=$(basename "$FILE" .fas)

    echo "Processing $base"

    # Create new directory for sample and cd into it
    mkdir -vp "$base"
    abs_file_path=$(realpath "$FILE")
    cd "$base" || exit "$ERR_CD"
    
    # Modify sequence by replacing all '-' and "X" with an "N".
    # Redirect output into a file.
    # shellcheck disable=SC2026
    sed s'/-/N/'g "$abs_file_path" | sed s'/X/N/'g > "$base".noX.fas
    
    # Loop through each line of the output and check if the direction is
    # reverse or forward, then perform appropriate functions on it.
    while IFS=, read -r geneName direction start stop; do
        mkdir -vp "$geneName"
        cd "$geneName" || exit "$ERR_CD"

        if [[ "${direction}" == "rev" ]]; then
            extractseq -sequence "$abs_file_path" -regions "$start-$stop" -outseq "$base"."$geneName".rvc.fasta;

            #Copy the reverse compliment of the extracted gene from the reverse sequence
            revseq -sequence "$base"."$geneName".rvc.fasta -outseq "$base"."$geneName".rvc_RV.fasta

            # Translate DNA nucleotides to amino acids. Same action performed for forward.
            transeq -sequence "$base"."$geneName".rvc_RV.fasta -outseq "$base"."$geneName".transl.fasta
        elif [[ $direction == "forw" ]]; then
            extractseq -sequence "$abs_file_path" -regions "$start-$stop" -outseq "$base"."$geneName".rv.fasta;
            
            transeq -sequence "$base"."$geneName".rv.fasta -outseq "$base"."$geneName".transl.fasta
        else
            echo "Invalid direction: $direction. Must be 'forw' or 'rev'!"
            exit "$ERR_INVALID_DIRECTION"
        fi

        # Ensure multi_fasta directory exists and append translated sequences
        mkdir -vp ../../multi_fasta/
        cat "$base"."$geneName".transl.fasta >> "../../multi_fasta/$geneName.mfa"

        cd ..
    done <<< "$output"

    cd ..    
done

exit "$SUCCESS"
