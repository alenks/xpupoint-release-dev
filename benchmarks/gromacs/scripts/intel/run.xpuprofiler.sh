#!/bin/bash
TOOLS=$PROJ_ROOT/tools
SRC=$PROJ_ROOT/src
PIN_ROOT=$TOOLS/pin-3.30-98830-g1d7b601b3-gcc-linux
GTPIN_KIT=$TOOLS/gtpin-4.5.0-linux
source COMMAND.sh
echo $COMMAND
export ZET_ENABLE_PROGRAM_INSTRUMENTATION=1
export ZE_ENABLE_TRACING_LAYER=1

RESULTS_DIR=BasicBlocks
HPCWL_COMMAND_PREFIX="$PIN_ROOT/pin -t $SRC/XPU-Profiler/Intel/CPUPinTool/obj-intel64/xpu-pin-kernelsampler.so -bbdir $RESULTS_DIR -gtpindir $GTPIN_KIT -gtpintool $SRC/XPU-Profiler/Intel/GTPinTool/build/GPUSampler.so -gt --output_dir -gt Local-GTPINDIR -gt --gpubbdir -gt $RESULTS_DIR -- "
time $HPCWL_COMMAND_PREFIX $COMMAND
