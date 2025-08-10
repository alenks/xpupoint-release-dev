#!/usr/bin/env python3

# BEGIN_LEGAL
# The MIT License (MIT)
#
# Copyright (c) 2025, National University of Singapore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# END_LEGAL

import sys
import os
import collections
from functools import reduce
import numpy as np
import argparse

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--cputhreads", type=int, default=8, help="Number of CPU threads")
  parser.add_argument("-w", "--gputhreads", type=int, default=32, help="Number of GPU threads")
  parser.add_argument("-c", "--cpudir", type=str, help="CPU profile directory")
  parser.add_argument("-g", "--gpudir", type=str, help="GPU profile directory")
  parser.add_argument("-o", "--outdir", type=str, help="Output directory")
  args = parser.parse_args()
  return args

def main(num_threads, cpu_basedir, gpu_basedir, out_basedir, mode):
  bb_files = []
  out = []
  num_bb_files = 0
  default_bb_dir = cpu_basedir
  if mode == "cpu":
    num_bb_files = num_threads
  elif mode == "xpu":
    num_bb_files = num_threads - 1
  elif mode == "gpu":
    num_bb_files = num_threads
    default_bb_dir = gpu_basedir
  for f in range(num_bb_files):
      bb_files.append(open("%s/T.%s.bb" % (default_bb_dir,f), "r"))
  if mode == "xpu":
    bb_files.append(open("%s/global.bbv" % (gpu_basedir), "r")) # adding GPU BBV

  # For each T line
  max_bb = int(-1)
  thread_line_count = [int(0)]*(num_threads)
  while True:
    end_of_file = [False]*(num_threads)
    # for each file
    for f in range(num_threads):
      # for each line
      while True:
        line = bb_files[f].readline()
        if line == "":
          end_of_file[f] = True
          break
        if line and line.startswith('T:'):
          thread_line_count[f] += 1;
          max_vals = map(lambda x:int(x.split(':')[1]), filter(lambda x:x, line[1:].rstrip().split(' ')))
          max_bb_tmp = max(max_vals)
          max_bb = max(max_bb, max_bb_tmp)
          break
    if reduce(lambda x,y:x and y, end_of_file):
      break
    # There can be some threads that end early.

  print('max_bb: ', max_bb)

  bb_files = []
  out = []
  for f in range(num_bb_files):
    bb_files.append(open("%s/T.%s.bb" % (default_bb_dir,f), "r"))
  if mode == "xpu":
    bb_files.append(open("%s/global.bbv" % (gpu_basedir), "r")) # adding GPU BBV

  if mode == "xpu":
    out.append(open("%s/T.global.hv" % (out_basedir,), "w"))
  elif mode == "cpu":
    out.append(open("%s/T.global.cv" % (out_basedir,), "w"))
  elif mode == "gpu":
    out.append(open("%s/global.bbv" % (out_basedir,), "w"))
  log = open("%s/concat-vectors.log" % (out_basedir,), "w")

  bb_pieces = {}
  global_kernel_marker = ''
  global_kernel_count_marker = 0
  unfiltered_icount_marker = 0
  marker_dict = {}
  marker_list = []

  # For each T line
  thread_line_count = [int(0)]*(num_threads)
  while True:
    end_of_file = [False]*(num_threads)
    # for each file
    thread_icounts = [int(0)]*(num_threads)
    for f in range(num_threads):
      # for each line
      while True:
        line = bb_files[f].readline()
        if line == "":
          end_of_file[f] = True
          break
        if line and line.startswith('# Slice ending'):
          global_kernel_marker = (line.split()[-3])
          global_kernel_count_marker = int(line.split()[-1])
        elif line and line[0] == 'T':
          thread_line_count[f] += 1;
          if (global_kernel_marker,global_kernel_count_marker) not in bb_pieces:
            bb_pieces[global_kernel_marker,global_kernel_count_marker] = {}
          bb_pieces[global_kernel_marker,global_kernel_count_marker][f] = np.array(list(map(lambda x:':%s:%s'%x, map(lambda x:(int(x.split(':')[1])+(max_bb*f),int(x.split(':')[2])), filter(lambda x:x, line[1:].rstrip().split(' '))))))
          break
    if reduce(lambda x,y:x and y, end_of_file):
      break

  print('Using Thread 0 BBV for event ordering.')
  global_fn = '%s/T.0.bb'%(cpu_basedir)
  if mode == "gpu":
    global_fn = '%s/T.0.bb'%(gpu_basedir)

  try:
    with open(global_fn, 'r') as global_in:
      curr_pcmarker = ''
      for line in global_in:
        if line and line.startswith('# Slice ending at '):
          global_kernel_marker = (line.split()[-3])
          global_kernel_count_marker = int(line.split()[-1])
          marker_list.append((global_kernel_marker,global_kernel_count_marker))
  except IOError as e:
    err_str = 'Unable to open the global BBV file: [%s]' % global_fn
    print(err_str)
    log.write(err_str)

  ordered_bb_pieces = collections.OrderedDict(sorted(bb_pieces.items()))

  #for k,v in ordered_bb_pieces.items():
  for i,k in enumerate(marker_list):
    print (k)
    if i > 0:
      out[0].write('M: %s %s\n' %(marker_list[i-1][0], marker_list[i-1][1]))
    else:
      out[0].write('M: SYS_init 1\n')
    out[0].write('# Slice ending at kernel %s count %s\n' % (k[0], str(k[1])))
    out[0].write('T')

    ordered_thread_bb_pieces = collections.OrderedDict(sorted(ordered_bb_pieces[k].items()))
    thread_ins_contri = [0.0] * (num_threads)
    tot_ins = 0
    for k1, v1 in ordered_thread_bb_pieces.items():
      th_ins = sum([int(el.split(':')[-1]) for el in v1])
      tot_ins += th_ins
      thread_ins_contri[k1] = th_ins
      if len(ordered_thread_bb_pieces[k1]) == 0:
        continue
      out[0].write(' '.join(ordered_thread_bb_pieces[k1]))
      out[0].write(' ')
    out[0].write('\n')

    if tot_ins == 0:
      err_str = 'Found slice without instructions, icounts: %s' % str(k)
      print (err_str)
      log.write(err_str)
  if mode == "xpu":
    out[0].write('M: SYS_exit 1')

    # In this version, it is okay to not have all thread data lengths be the same
    #for f in range(7):
    #  assert(thread_line_count[f] == thread_line_count[f+1])

  out[0].close()
  log.close()

if __name__=='__main__':
  args = get_args()
  mode = "" # cpu,gpu,xpu
  num_threads = 0
  num_cpu_threads = args.cputhreads
  num_gpu_threads = args.gputhreads
  if args.cpudir:
    cpu_basedir = args.cpudir
  else:
    cpu_basedir = ""
  if args.gpudir:
    gpu_basedir = args.gpudir
  else:
    gpu_basedir = ""
  if args.outdir:
    out_basedir = args.outdir
  elif cpu_basedir:
    out_basedir = cpu_basedir
  elif gpu_basedir:
    out_basedir = gpu_basedir

  if cpu_basedir and gpu_basedir:
    num_threads = num_cpu_threads + 1
    mode = "xpu"
  elif cpu_basedir and not gpu_basedir:
    num_threads = num_cpu_threads
    mode = "cpu"
  elif gpu_basedir and not cpu_basedir:
    num_threads = num_gpu_threads
    mode = "gpu"
  else:
    print("Require either CPU or GPU profile directories to continue.")
    exit(1)
  main(num_threads, cpu_basedir, gpu_basedir, out_basedir, mode)


