#!/usr/bin/env python3

import os
import argparse
import re

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nthreads", type=int, help="Number of threads")
    parser.add_argument("-g", "--gpudir", type=str, default=".", help="GPU profile directory")
    parser.add_argument("-o", "--outdir", type=str, default="gpu-perthread", help="Output directory created inside <gpudir>")

    args = parser.parse_args()
    return args

def get_num_threads(gpu_basedir):
    nthreads = 0
    threadfile = os.path.join(gpu_basedir, 'thread.bbv')
    if not os.path.isfile(threadfile):
        print('%s not found.' %threadfile)
        exit(1)
    with open(threadfile, 'r') as readf:
        for line in readf:
            if line.startswith('tid'):
                linekey = line.split(':')[0]
                mat = re.match(r"([a-z]+)([0-9]+)", linekey, re.I)
                if mat:
                    items = mat.groups()
                if (int(items[1]) > nthreads):
                    nthreads = int(items[1])
    return nthreads+1

def main(num_threads, gpu_basedir, out_basedir):
    print('Using %s threads '% str(num_threads))
    try:
        os.makedirs(out_basedir, exist_ok=True)
        print("Directory '%s' created successfully" % out_basedir)
    except OSError as error:
            print("Directory '%s' can not be created" % out_basedir)

    f = []
    for i in range(0, num_threads):
        temp = open(os.path.join(out_basedir, 'T.%s.bb' % str(i)), 'w')
        f.append(temp)
    threadfile = os.path.join(gpu_basedir, 'thread.bbv')
    with open(threadfile, 'r') as readf:
        for line in readf:
            if line.startswith('#') or line.startswith('M:') or line.startswith('S:'):
                for i in range(0, num_threads):
                    f[i].write(line)
            elif line.startswith('tid'):
                thread = 0
                linekey = line.split(':')[0]
                mat = re.match(r"([a-z]+)([0-9]+)", linekey, re.I)
                if mat:
                    items = mat.groups()
                    thread = int(items[1])
                line = line.split(' ', 1)[-1]
                f[thread].write(line)
    return

if __name__=='__main__':
    args = get_args()
    gpu_basedir = args.gpudir
    if args.nthreads:
        num_threads = args.nthreads
    else:
        num_threads = get_num_threads(gpu_basedir)
    out_basedir = os.path.join(gpu_basedir, args.outdir)

    main(num_threads, gpu_basedir, out_basedir)

