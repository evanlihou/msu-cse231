'''
Project 6

Prompts the user for a file containing the genes of C. Elegans
Prompts the user for data on all chromosomes, a specific one, or to quit
If all
    Display a table showing mean and std-dev for each chromosome
If one specific
    Display a table showing the mean and std-dev for that chromosome
If quit
    Terminate the program
Otherwise
    Display an error and prompt for another input from the user
'''

import numpy
CHROMOSOMES = ['chri', 'chrii', 'chriii', 'chriv', 'chrv', 'chrx']


def open_file():
    '''
    This function has no parameters.
    Opens a file with error checking. Will reprompt if file is not found.
    Returns: file pointer
    '''
    FILE_PROMPT = "Input a file name: "
    ERR_FILE_NOT_FOUND = "Unable to open file."
    file_str = input(FILE_PROMPT)
    while True:
        try:
            fp = open(file_str)
            return fp
        except FileNotFoundError:
            print(ERR_FILE_NOT_FOUND)
            file_str = input(FILE_PROMPT)


def read_file(fp):
    '''
    Reads a file, ignoring comments, and creating a list.
    fp (file pointer): file to read
    Returns: List of tuples using the format (chromosome, start_loc, end_loc)
    '''
    genes_list = []
    for line in fp:
        if line[0] == "#":
            continue
        gene = line.split('\t')  # Split by tabs
        try:
            start = int(gene[3])
        except ValueError:
            start = 0
        try:
            end = int(gene[4])
        except ValueError:
            end = 0
        relevant_data = (gene[0], start, end)
        genes_list.append(relevant_data)
    fp.close()
    return genes_list


def extract_chromosome(genes_list, chromosome):
    '''
    Extracts and sorts genes on a certain chromosome
    genes_list (list): List of all genes from the read_file function
    chromosome (str): Chromosome to search for
    Returns: sorted list of tuples for that chromosome with format
        (chromosome, start_loc, end_loc)
    '''
    chrom_gene_list = []
    for gene in genes_list:
        if gene[0] == chromosome:  # gene[0] = gene's chromosome
            chrom_gene_list.append(gene)
    chrom_gene_list.sort()
    return chrom_gene_list


def extract_genome(genes_list):
    '''
    Runs extract_chromosome for all chromosomes in a genome, then combines them
    into one list
    genes_list (list): List of all genes from the read_file function
    Returns: list of sorted lists of tuples for each chromosome using the
        format (chromosome, start_loc, end_loc)
    '''
    genome_list = []
    for chromosome in CHROMOSOMES:
        genome_list.append(extract_chromosome(genes_list, chromosome))
    return genome_list
 

def compute_gene_length(chrom_gene_list):
    '''
    Computes the mean and standard deviation for gene lengths of a chromosome
    chrom_gene_list (list): sorted list of tuples for one chromosome with
        format (chromosome, start_loc, end_loc)
    Returns: tuple with format (mean, standard deviation) for that chromosome
    '''
    gene_lengths = []
    for gene in chrom_gene_list:
        gene_lengths.append(gene[2]-gene[1]+1)
    mean = numpy.mean(gene_lengths)
    std_dev = numpy.std(gene_lengths)
    return (mean, std_dev)


def display_data(genes_list, chromosome):
    '''
    Displays a table row of data for a chromosome, using the extract_chromosome
        and compute_gene_length functions
    genes_list (list): List of all genes from the read_file function
    chromosome (str): Chromosome to search for
    Returns: String formatted for a table with col widths of 11, 9, and 9
    '''
    chrom_gene_list = extract_chromosome(genes_list, chromosome)
    chromosome_normalized = chromosome[:3].lower() + chromosome[3:].upper()
    gene_length = compute_gene_length(chrom_gene_list)
    mean = gene_length[0]
    std_dev = gene_length[1]
    print("{:<11s}{:9.2f}{:9.2f}".format(chromosome_normalized, mean, std_dev))


def main():
    '''
    See main program docstring for documentation on this function
    '''
    WELCOME = "Gene length computation for C. elegans.\n"
    SEARCH_PROMPT = "\nEnter chromosome or 'all' or 'quit': "
    TABLE_PRE_HEADER = "\nChromosome Length"
    TABLE_HEADER = "{:<11s}{:>9s}{:>9s}".format(
            "chromosome", "mean", "std-dev")
    CHROM_ERR = "Error in chromosome.  Please try again."
    print(WELCOME)
    genes = read_file(open_file())
    while True:
        search = input(SEARCH_PROMPT)
        if search.lower() in CHROMOSOMES:  # If input is a valid chromosome
            print(TABLE_PRE_HEADER)
            print(TABLE_HEADER)
            display_data(genes, search.lower())
        elif search.lower() == "all":
            print(TABLE_PRE_HEADER)
            print(TABLE_HEADER)
            for chromosome in CHROMOSOMES:
                display_data(genes, chromosome)
        elif search.lower() == "quit":
            break  # Terminate the program
        else:
            print(CHROM_ERR)
    

if __name__ == "__main__":
    main()