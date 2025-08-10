#!/usr/bin/env python3
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--maxk", type=int, default=20, help="maxK for Kmeans clustering (20).")
    parser.add_argument("-d", "--dim", type=int, default=15, help="Number of reduced dimensions (15).")
    parser.add_argument("-b", "--bbvfile", type=str, default="./T.global.hv", help="The BBV file to sample (T.global.hv).")
    parser.add_argument("-o", "--outdir", type=str, help="Output directory.")
    parser.add_argument("--no-regions", default=False, action='store_true', help="No xpuregions.csv file will be generated.")
    parser.add_argument("--fixed-length", type=str, default="on", help="Passed to SimPoint -fixedLength (on)/off")
    args = parser.parse_args()
    return args

def main(maxk, dim, globalbbv, outdir, no_regions=False, gpu_only=False, fixed_length="on"):
    sde_kit = os.environ['SDE_BUILD_KIT']
    simpoint = os.path.join(sde_kit, 'pinplay-scripts/PinPointsHome/Linux/bin/simpoint')
    tsimpoints = os.path.join(outdir, 't.simpoints')
    tweights = os.path.join(outdir, 't.weights')
    tlabels = os.path.join(outdir, 't.labels')
    regions_csv = os.path.join(outdir, 'xpuregions.csv')
    if fixed_length != "off":
        fixed_length = "on"
    if gpu_only:
        regions_csv = os.path.join(outdir, 'gpuregions.csv')
    utils_dir = os.path.dirname(os.path.abspath(__file__))

    print('Running SimPoint')
    if not os.path.isfile(os.path.join(sde_kit, 'pinplay-scripts/PinPointsHome/Linux/bin/simpoint')):
        print('Error: Binary to run SimPoint not found in %s' % sde_kit)
    simpoint_cmd = sde_kit + '/pinplay-scripts/PinPointsHome/Linux/bin/simpoint -loadFVFile ' + globalbbv + ' -maxK ' + str(maxk) + ' -dim ' + str(dim) + ' -coveragePct 1.0 -saveSimpoints ' + tsimpoints + ' -saveSimpointWeights ' + tweights + ' -saveLabels ' + tlabels + ' -fixedLength ' + fixed_length + ' -verbose 1'
    os.system(simpoint_cmd)
    if no_regions:
        exit(0)
    print('Generating %s' %regions_csv.split('/')[-1])
    mregions_cmd = utils_dir + '/xpu_regions.py --bbv_file=' + globalbbv + ' --region_file=' + tsimpoints + ' --weight_file=' + tweights + ' --label_file=' + tlabels + ' --csv_region > ' + regions_csv
    os.system(mregions_cmd)

if __name__=='__main__':
    args = get_args()
    maxk = args.maxk
    dim = args.dim
    globalbbv = args.bbvfile
    bbv_path = os.path.dirname(globalbbv)
    if args.outdir:
        outdir = args.outdir
    else:
        outdir = bbv_path
    main(maxk, dim, globalbbv, outdir, args.no_regions, args.fixed_length)

