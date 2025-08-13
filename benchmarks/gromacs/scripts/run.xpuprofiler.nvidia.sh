#!/bin/bash
source COMMAND.sh
echo $COMMAND
ulimit -s unlimited
TOOLBASE=$(TOOLS)/XPU-Sampler/NVIDIA-GPU
GROMACS_LIB=$(TOOLS)/workloads/HPC/Gromacs/Install/lib
RESULTS_DIR=BasicBlocks
LD_PRELOAD=$TOOLBASE/NVBitTool/NVBitTool.so $PIN_ROOT/pin -t $TOOLBASE/CPUPinTool/obj-intel64/xpu-pin-kernelsampler.so -filter_allow_lib /lib64/ld-linux-x86-64.so.2 -filter_allow_lib /lib/x86_64-linux-gnu/libdl.so.2 -filter_allow_lib /lib/x86_64-linux-gnu/libm.so.6 -filter_allow_lib /lib/x86_64-linux-gnu/libc.so.6 -filter_allow_lib $GROMACS_LIB/libgromacs.so.8 -filter_allow_lib $GROMACS_LIB/libmuparser.so.2 -filter_allow_lib /usr/local/cuda-11.4/lib64/libcufft.so.10 -bbprofile -bbfocusthread 0 -emit_vectors 0 -bbverbose 1  -nvbittool  $TOOLBASE/NVBitTool/NVBitTool.so -- $COMMAND

#LD_PRELOAD=$TOOLBASE/NVBitTool/NVBitTool.so $PIN_ROOT/pin -t $TOOLBASE/CPUPinTool/obj-intel64/xpu-pin-nvbit-handler.so -nvbittool  $TOOLBASE/NVBitTool/NVBitTool.so -- $COMMAND

