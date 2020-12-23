# phylogenomics
###################################
#     Phylogenetic resolution     #
###################################

Phylogenetic resolution
Created By: Carlos Congrains and Reinaldo Brito
Email: carloscongrains@gmail.com

##########################

This Python script was developed to compare the internal topology of each gene tree against the tooplogy of a refence tree (such as species tree) to estimate the congruence between them by calculating how many lineages that are resolved in the former that agrees with the latter. Based on that comparison we defined Phylogenetic resolution of a gene,as the percentage of nodes in each gene tree that agrees with the reference tree topology. If you use this script, please cite: Phylogenomic approach reveals intense signatures of introgression in the rapid radiation of Neotropical true fruit flies (Anastrepha: Tephritidae).

REQUIREMENTS:

We developed and tested this script using Python version 2.7 and the following modules and libraries:

- sys
- os
- argparse
- csv
- ete3

If you need to install these libraries, we recommend to use pip as follows:
pip install ete3
Where ete3 is the library name.

ARGUMENT OPTIONS:

-h, --help        show this help message and exit
--tree_directory  Directory containing tree files in newick format and ended by ".tre"
--log_file        Path to a log file.
--output_file     File containing the results.
--groups_to_test  A two columns file, containing the taxa (equal as in the newick file) and group (tab separated file without spaces) to test for monophyly.
--number_taxa     Total number of taxa of the tree.

 
##########################

Example:

python2 phylogenetic_resolution.py  --tree_directory example/trees --log_file log_file.out --output_file ouput --branch_tested example/groups_for_test --number_taxa 17

WARNINGS:
The example/trees directory must contain tree in newick formats and the file names must end in ".tre". 
All of these trees must have the same number of samples, which is indicated in the option --number_taxa.
The tested groups must be indicated in a tabular file, see the file example/groups_for_test for an example.
