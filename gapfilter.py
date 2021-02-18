#!coding:utf-8

import os
import sys
import pickle
import argparse
from collections import Counter

if len(sys.argv) == 1:
    os.system('python gapfilter.py --help')
    sys.exit(1)

parser = argparse.ArgumentParser(description='FilterGap')
parser.add_argument('-f', '--MSAfile', help='MSA output file path, as input file')
parser.add_argument('-o', '--output', help='output file path, filter result')
parser.add_argument('-d', '--delete', 
                    help='delect this sequence if there is more the set "-d" continues gap',
                    default=0, type=int)
parser.add_argument('-p', '--precent', 
                    help='Threshold of the percentage of filter site gaps, default=10.0',
                    default=10.0, type=float
                    )
parser.add_argument('-r', '--record', help='record drop gaps index, default=None, if yes, filename needed',
                    default=None)
args = parser.parse_args()


infile = args.MSAfile
outfile = args.output
p_gap = args.precent
n_gap = args.delete
record = args.record

with open(infile) as seqf:
    seqs = seqf.read().split('>')[1:]
seq_list = []
for seq in seqs:
    lines = seq.strip().split('\n')
    name = lines[0]
    seq_line = ''.join(lines[1:]).replace('*', '')
    seq_list.append((name, seq_line))

seq_list = list(zip(*seq_list))
num_seqs = len(seq_list[1])
statues = list(zip(*seq_list[1]))
print('Number of source status: ', len(statues))    

while True:
    statues_cut = []
    record_list = []
    for i, stat in enumerate(statues):
        gap = stat.count('-')*100.0/num_seqs
        if gap < p_gap:
            statues_cut.append(stat)
        elif record:
            record_list.append(i)
            
    print('Number of status after filter', len(statues_cut))
    p_gap = input("\033[1;32mEnter -1 to continue, or modify parameter --precent: \033[0m")
    if not p_gap: break
    p_gap = float(p_gap)
    if p_gap < 0: break

seqs_cut = list(zip(*statues_cut))
seq_cut_list = list(zip(*(seq_list[0], seqs_cut)))
seq_cut_list = [(name, ''.join(seq_line)) for name, seq_line in seq_cut_list]
# delect sequence if there is more gaps
if n_gap:
    seq_cut_list = [(name, seq_line) for name, seq_line in seq_cut_list if '-'*n_gap not in seq_line]

outf = open(outfile, 'w')
for name, seq_line in seq_cut_list:
    line = ">" + name + "\n" + seq_line + '\n'
    outf.write(line)

if record:
	with open(record, 'wb') as recordf:
		pickle.dump(record_list, recordf)

outf.close()
