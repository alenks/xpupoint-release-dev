#!/usr/bin/env python3

import os
import argparse
import threadsplit
import concat_xpu_vectors
import run_simpoint
import gen_insweights

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--cputhreads", type=int, default=8, help="Number of CPU threads")
    parser.add_argument("-w", "--gputhreads", type=int, default=32, help="Number of GPU threads")
    parser.add_argument("-c", "--cpudir", type=str, default=".", help="CPU profile directory (.)")
    parser.add_argument("-g", "--gpudir", type=str, default=".", help="GPU profile directory")
    parser.add_argument("-o", "--outdir", type=str, help="Output directory")
    parser.add_argument("--gpu-only", action='store_true', default=False, help="Use only GPU regions for clustering")
    parser.add_argument("-m", "--maxk", type=int, default=20, help="maxK for Kmeans clustering (20)")
    parser.add_argument("-d", "--dim", type=int, default=15, help="Number of reduced dimensions (15)")
    parser.add_argument("--simpoint-only", action='store_true', default=False, help="Run only SimPoint clustering")
    parser.add_argument("--fixed-length", type=str, default="on", help="Passed to SimPoint -fixedLength (on)/off")

    args = parser.parse_args()
    return args

def run_gpu_only(gpu_basedir, maxk, dim, out_basedir, simpoint_only, fixed_length):
    if not os.path.isfile(os.path.join(gpu_basedir, 'global.bbv')):
        print('Error: global.bbv not found at %s' % gpu_basedir)
        exit(1)
    gpuout_basedir = os.path.join(gpu_basedir, 'gpu-perthread')
    if not simpoint_only:
        threadsplit.main(num_gpu_threads, gpu_basedir, gpuout_basedir)
        concat_xpu_vectors.main(num_gpu_threads, cpu_basedir, gpuout_basedir, gpuout_basedir, "gpu")
    run_simpoint.main(maxk, dim, os.path.join(gpuout_basedir, 'global.bbv'), out_basedir, gpu_only=True, fixed_length=fixed_length)
    gen_insweights.main(out_basedir, os.path.join(gpuout_basedir, 'global.bbv'))
    return

def main(num_cpu_threads, num_gpu_threads, cpu_basedir, gpu_basedir, out_basedir, maxk, dim, simpoint_only, fixed_length):
    if not simpoint_only:
        gpuout_basedir = os.path.join(gpu_basedir, 'gpu-perthread')
        threadsplit.main(num_gpu_threads, gpu_basedir, gpuout_basedir)
        concat_xpu_vectors.main(num_gpu_threads, cpu_basedir, gpuout_basedir, gpuout_basedir, "gpu")
        concat_xpu_vectors.main(num_cpu_threads+1, cpu_basedir, gpuout_basedir, out_basedir, "xpu")
    run_simpoint.main(maxk, dim, os.path.join(out_basedir, 'T.global.hv'), out_basedir, fixed_length=fixed_length)
    gen_insweights.main(out_basedir)
    return

if __name__=='__main__':
    args = get_args()
    num_cpu_threads = args.cputhreads
    num_gpu_threads = args.gputhreads
    cpu_basedir = args.cpudir
    gpu_basedir = args.gpudir
    if args.outdir:
        out_basedir = args.outdir
    else:
        if args.gpu_only:
            out_basedir = args.gpudir
        else:
            out_basedir = args.cpudir
    maxk = args.maxk
    dim = args.dim
    if args.gpu_only:
        run_gpu_only(gpu_basedir, maxk, dim, out_basedir, args.simpoint_only, args.fixed_length)
    else:
        main(num_cpu_threads, num_gpu_threads, cpu_basedir, gpu_basedir, out_basedir, maxk, dim, args.simpoint_only, args.fixed_length)

