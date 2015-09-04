#!/usr/bin/python
import os, sys
import src
from src import *
import logging
import filter_features.main as ff
import string
import random
import itertools
import shutil
import random

def change_classes(in_file, out_file, border=0, cut=None):
    with open(in_file) as fw:
        pass

def create_temp_folder(base):
    token = ''.join([random.choice(string.hexdigits) for x in range(4)])
    temp_folder = os.path.join(base, 'temp_'+token)
    if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
    logging.info('Temp folder created \n {}'.format(temp_folder))
    return temp_folder

def preparefile(infile, temp_folder, mincount):
    logging.info('Reforming file')
    reformed = os.path.join(temp_folder, 'reformed')
    os.system('sort {} | uniq | shuf > {}'.format(infile, reformed))
    logging.info('Removing features with less than {}'.format(mincount))
    filtered_reformed = os.path.join(temp_folder, 'filtered')
    ff.filter_features(reformed, filtered_reformed, mincount)
    

    return filtered_reformed

def spliting_files(parts, infile, temp_folder):
    file_list = []
    for part in range(parts):
        prefix = '{}_{}'.format(part + 1, parts)
        logging.info('Making files for {}'.format(prefix))
        part_dir = os.path.join(temp_folder, prefix)
        os.makedirs(part_dir)
        part_files = (prefix, 
                os.path.join(part_dir, 'trening.vw'),
                os.path.join(part_dir, 'test.vw'),
                os.path.join(part_dir, 'model.vw'),
                os.path.join(part_dir, 'pred.txt'),
                )
        ftren, ftest = open(part_files[1], 'w'), open(part_files[2], 'w')

        for nr, line in enumerate(open(infile)):
            if nr % parts == part:
                ftest.write(line)
            else:
                ftren.write(line)
        file_list.append(part_files)
    return file_list

def run_vopal(part, temp_folder, options):
    q = query.format(in_file=part[1], out_file=part[3], options=options)
    os.system(q)
    p = pred.format(out_file=part[3], test_file=part[2], pred_file=part[4])
    os.system(p)
    

def crossvalidation(parts, infile, temp_base, outfile, mincount, options, samples=None):
    temp_folder = create_temp_folder(temp_base)
    logging.info('Starting crossvalidation for file : {}'.format(infile) )
    preparedfile = preparefile(infile, temp_folder, mincount)
    splited_files = spliting_files(parts, preparedfile, temp_folder)
    if samples:
        splited_files = random.sample(splited_files, samples)

    for part in splited_files:
        run_vopal(part , temp_folder, options)
    with open(outfile, 'w') as fw:
        for part in splited_files:
            logging.info('Merging part {}'.format(part[0]))
            for line_a, line_b in itertools.izip(open(part[2]), open(part[4])):
                fw.write('\t'.join([line_a.split()[0], line_b.split()[0]] )+'\n')
    try:
        shutil.rmtree(temp_folder)
    except:
        logging.warning('---| rm -rf {}'.format(temp_folder))
#

def main(parts, infile, temp_base, outfile, mincount, options, samples=None):
    crossvalidation(parts, infile, temp_base, outfile,  mincount, options, samples)


if __name__=="__main__":
    config = input_parser._get()
    mincount = config.mincount
    parts = config.parts
    infile = config.in_file
    temp_base = config.temp_location
    outfile = config.out_file
    samples = config.samples
    options = config.options
    #query = "vw {in_file} -k -f {out_file} --cache_file {out_file}_cache -b 22 --passes 10 --meanfield --multitask --nn 13 --keep b --keep h --ignore u --keep r --interactions bb --ftrl --loss_function logistic"
    query = "vw {in_file} -k -f {out_file} --cache_file {out_file}_cache {options}"
    pred = "vw -d {test_file} -t -i {out_file}  -p {pred_file}"
    
    main(parts, infile, temp_base, outfile,  mincount, options, samples)



