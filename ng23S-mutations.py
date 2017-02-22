#!/usr/bin/env python
# Script by Jason Kwong
# Script to identify 23S mutations in NG

# Use modern print function from python 3.x
from __future__ import print_function

# Import modules
import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import csv
import subprocess
from subprocess import Popen

# Usage
parser = argparse.ArgumentParser(
	formatter_class=RawTextHelpFormatter,
	description='Script to identify 23S mutations in NG (reports E.coli numbering)',
	usage='\n  %(prog)s <snippy1> <snippy2> ... <snippyN>')
parser.add_argument('snippy', metavar='DIR', nargs='+', help='Snippy directories (required)')
parser.add_argument('--prefix', metavar='PREFIX', nargs=1, default='snps', help='Snippy .tab output prefix (default="snps")')
parser.add_argument('--version', action='version', version=
	'=====================================\n'
	'%(prog)s v0.1\n'
	'Updated 10-Aug-2016 by Jason Kwong\n'
	'Dependencies: Python 2.x\n'
	'=====================================')
args = parser.parse_args()

# Functions
# Log a message to stderr
def msg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# Log an error to stderr and quit with non-zero error code
def err(*args, **kwargs):
	msg(*args, **kwargs)
	sys.exit(1);

# Check file exists
def check_file(f):
	if os.path.isfile(f) == False:
		err('ERROR: Cannot find "{}". Check file exists in the specified directory.'.format(f))

def dir_check(dir, filename):
	file = os.path.join(dir, filename)
	check_file(file)
	return file

def write_snps(data, file):
	with open(file, 'w') as f:
		f.write(data)
	check_file(file)

def ploidy_snippy(dir, prefix):
	refdir = os.path.join(dir, 'reference')
	if os.path.isdir(refdir) == False:
		err('ERROR: Check directory is a Snippy directory')
	reffa = dir_check(refdir, 'ref.fa')
	snps_raw = os.path.join(dir, prefix+'.raw.vcf')
	vcf_to_tab = subprocess.Popen(['snippy-vcf_to_tab', '--ref', reffa, '--vcf', snps_raw], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	tab_out = vcf_to_tab.communicate()[0]
	write_snps(tab_out, os.path.join(dir, prefix+'.ploidy.tab'))

sep = '\t'
for dir in args.snippy:
	dir = dir.rstrip('/')
	if os.path.isdir(dir) == False:
		err('ERROR: Cannot find "{}". Check directory exists.'.format(dir))
	prefix = args.prefix
	ploidy_snippy(dir, prefix)
	with open(os.path.join(dir, prefix+'.ploidy.tab'), 'r') as tab:
		snps = csv.reader(tab, delimiter='\t')
		next(snps)
		for row in snps:
			if row[2] == 'snp':
				if int(row[1]) >= 1956488 and int(row[1]) <= 1959377:
					locus = int(row[1]) - 1956487 + 14
					ref_allele = row[3]
					alt_allele = row[4]
					snp = ref_allele + str(locus) + alt_allele
					evidence = row[5].split()
					alt = int(evidence[0].split(':')[1])
					ref = int(evidence[1].split(':')[1])
					if ref > alt:
						if ref > 10 * alt:
							ratio = '4:0'
						else:
							ratio = str(int(round(float(ref)/alt))) + ':1'
					else:
						if alt > 10 * ref:
							ratio = '0:4'
						else:
							ratio = '1:' + str(int(round(float(alt)/ref)))
					print(sep.join([dir, row[1], snp, evidence[1], evidence[0], ratio]))
