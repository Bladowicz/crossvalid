import argparse
import logging
import os
import sys

def validate_args(conf):
    conf.in_file = conf.in_file[0]
    conf.out_file = conf.out_file[0]
    conf.parts = int(conf.parts)
    if conf.samples != None:
        conf.samples = int(conf.samples)
    else:
        conf.sample = conf.parts
    if conf.samples > conf.parts:
        logging.fatal('WTF')
        sys.exit(1)
#    conf.product = conf.product[0]
#    if not os.path.exists(conf.in_file):
#        logging.error('Input file does not exist')
#        sys.exit()
#    else:
#        if not os.access(conf.in_file, 4):
#            logging.error('Dont have permissions to read input file.')
#            sys.exit()
#
#    if os.path.exists(conf.out_file):
#        if conf.force_overwrite:
#            logging.warning('Output file exists - overwriting.')
#            if not os.access(conf.out_file, 2):
#                logging.error('Dont have permissions to write in output file.')
#                sys.exit()
#        else:
#            logging.error('Output file already exists. Please change name, of add -F')
#            sys.exit()
#


def _get():
    parser = argparse.ArgumentParser()
 #   sp = parser.add_subparsers()
#    method = parser.add_mutually_exclusive_group(required=True)    

    parser.add_argument(action='store', dest='in_file',
                                help='Input file in Vopal Wabbit input format',
                                nargs=1,
                                )

    parser.add_argument(action='store', dest='out_file',
                                help='Output file.',
                                nargs=1,
                                )


    parser.add_argument('-c', action='store', dest='mincount',
                                help='Min count of occurences',
                                default=250)


    parser.add_argument('-s', action='store', dest='samples',
                                help='Samples to draw fro parts',
                                default=None)


    parser.add_argument('-p', action='store', dest='parts',
                                help='Parts to fold',
                                default=4)


    parser.add_argument('-t', action='store', dest='temp_location',
                                help='Location for calculations',
                                default="/home/model/.crossvalidation/")


    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    out =  parser.parse_args()
    validate_args(out)
    return out
#results = _get()
