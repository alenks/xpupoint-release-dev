#!/usr/bin/env python3
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-dir", type=str, help="SimPoint output directory (require T.global.hv, t.simpoints, t.labels).")
    parser.add_argument("-g", "--global-bbv", type=str, default="T.global.hv", help="The global BBV file used for clustering")
    args = parser.parse_args()
    return args

def main(datadir, globalbbv='T.global.hv'):
    print ("Generating cluster weights based on slice lengths.")
    allrcounts = []
    if globalbbv == 'T.global.hv':
        globalbbv = os.path.join(datadir, globalbbv)
    with open(globalbbv, 'r') as f:
        for line in f:
            rcount = 0
            if line.startswith('T:'):
                linesplit = line.split()
                for el in linesplit:
                    rcount += int(el.split(':')[-1])
                allrcounts.append(rcount)
    sumtot = sum(allrcounts)

    slice_weights = {}
    for i, element in enumerate(allrcounts):
        slice_weights[i] = round(element/sumtot, 9)

    region_slice_map = {}
    with open(os.path.join(datadir, 't.simpoints'), 'r') as f:
        for line in f:
            sliceid, regionid = line.split()
            region_slice_map[int(regionid)] = int(sliceid)

    sliceid = 0
    region_counts = {}
    rep_weights = {}
    with open(os.path.join(datadir, 't.labels'), 'r') as f:
        for line in f:
            regionid, dist = line.split()
            regionid = int(regionid)
            if regionid not in region_counts.keys():
                region_counts[regionid] = 1
            else:
                region_counts[regionid] += 1

    weight_sum = 0
    cluster_weight = []
    for regionid in region_counts.keys():
        curr_wt = round(slice_weights[region_slice_map[regionid]] * region_counts[regionid], 8)
        cluster_weight.append((curr_wt, regionid))
        weight_sum += curr_wt

    cluster_weight.sort(key=lambda tup: tup[1])

    fw = open(os.path.join(datadir, 't.iweights'), 'w+')
    for wt, rid in cluster_weight:
        fw.write("%s %s\n" %(wt, rid))
    print ("Sum of cluster weights: %s" %weight_sum)

if __name__=='__main__':
    args = get_args()
    datadir = args.data_dir
    globalbbv = args.global_bbv
    main(datadir, globalbbv)
