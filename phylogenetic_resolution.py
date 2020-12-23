#! /usr/bin/python

"""
Calculate the phylogenetic resolution of a gene, which is the proportion of monophyletic groups found in a reference tree (such as species tree) that also be found in a determined gene tree. 
For this comparison the trees must be in newick format and the file names must have the extension ".tre".
"""

import argparse,os,sys
import logging
import csv
import re
from ete3 import Tree


class MyParser(argparse.ArgumentParser):
	def error(self, message):
		sys.stderr.write('error: %s\n' % message)
		self.print_help()
		sys.exit(2)

parser=MyParser()
parser.add_argument('--tree_directory', help='Directory containing tree files in newick format and ended by .tre')
parser.add_argument('--log_file', help='Path to the log file')
parser.add_argument('--output_file', help='File containing the results.')
parser.add_argument('--groups_to_test', help='A two columns file, containing the taxa (equal as in the newick file) and group (tab separated file without spaces) to test for monophyly.')
parser.add_argument('--number_taxa', help='Total number of taxa of the tree.')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if args.tree_directory:
	tree_directory = args.tree_directory
	if tree_directory[-1] != "/":
		tree_directory += "/"

if args.output_file:
	output_file = args.output_file

if args.log_file:
	log_file = args.log_file
	
if args.number_taxa:
	number_taxa = int(args.number_taxa)

if args.groups_to_test:
	group_file = args.groups_to_test

		
'''
FUNCTIONS
'''

#Convert the table in groups_to_test file (group_file) into a dictionary.
def table_2_dictionary(group_file):
	group_dict = {}
	with open(group_file, "r") as f:
		for line in f:
			line_list = line.rstrip().split('\t')
			if line_list[1] in group_dict:
				group_dict[line_list[1]].append(line_list[0])
			else:
				group_dict[line_list[1]] = []
				group_dict[line_list[1]].append(line_list[0])
	return group_dict
	
#Test for monophyly using a dictionary of node names as key and leave names as element.
def monophyly_test(groups_for_test,number_of_groups_for_test,tree):
	t = Tree(tree)
	current_result = []
	counter = 0
	for test_group in groups_for_test:
		current_result.append(test_group)
		if t.check_monophyly(values=groups_for_test[test_group], target_attr="name")[0] == True:
			current_result.append("yes")
			counter = counter + 1
		else:
			current_result.append("no")
	#Append the number of monophyletic groups found in the gene tree
	current_result.append(counter)
	#Append the monophyletic resolution
	phylogenetic_resolution = round((float(counter)/float(number_of_groups_for_test))*100, 2)
	current_result.append(phylogenetic_resolution)
	return current_result

#Save the results (final_results) into a tab delimited file. 
def list_2_file(output_file,final_results):
	with open(output_file,"w") as f:
		wr = csv.writer(f,delimiter='\t')
		wr.writerows(final_results)

"""
Check to avoid rewrite previous result and log files.
"""

assert not os.path.exists(log_file), "WARNING: The file " + log_file + " already exist. Please rename or move the previous log file to prevent information loss."
assert not os.path.exists(output_file), "WARNING: The file " + output_file + " already exist. Please rename or move the previous results to prevent information loss."

"""
Variables
"""

#Vector for the final results
final_results = []

#File count
filecount=0

#Create the log file.
logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)

"""
Main
"""

#Create the dictionary from the groups_to_test file (group_file).
groups_for_test = table_2_dictionary(group_file)
number_of_groups_for_test = len(groups_for_test)

#Iterating in the directory
for file in os.listdir(tree_directory):
	filename, file_extension = os.path.splitext(file)
	#Check for extension ".tre"
	if file_extension == ".tre":
		tree_file = tree_directory + file
		#Check for the number of taxa
		if len(Tree(tree_file))==number_taxa:
			filecount += 1
						
			#Test for monophylies
			monophyly_result  = monophyly_test(groups_for_test,number_of_groups_for_test,tree_file)
		
			#Get the filename and use it as ID
			clusterID = [filename]
		
			#Store the results in a list
			current_result = clusterID + monophyly_result
			final_results.append(current_result)
 
	else:
		logging.info(file + ": The file doesn't have the extension .tre)")
		
assert filecount > 0, "No file with .tre extension or does not have the supplied number of taxa."

#Save the results in the output file. 
list_2_file(output_file,final_results)
