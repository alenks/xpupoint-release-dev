#!/bin/bash
source COMMAND.sh
echo $COMMAND
export ZET_ENABLE_PROGRAM_INSTRUMENTATION=1
export ZE_ENABLE_TRACING_LAYER=1
GTPIN_RESULTS_DIR=BasicBlocks
HPCWL_COMMAND_PREFIX="$SDE_BUILD_KIT/sde64 -t64 $(TOOLS)/XPU-Sampler/Intel-GPU/CPUPinTool/obj-intel64/xpu-pin-kernelsampler.so -bbdir $GTPIN_RESULTS_DIR -gtpindir $GTPIN_KIT  -gtpintool $(TOOLS)/XPU-Sampler/Intel-GPU/GTPinTool/build/GPUSampler.so -gt --output_dir -gt Local-GTPINDIR -gt --gpubbdir  -gt $GTPIN_RESULTS_DIR -- "
time $HPCWL_COMMAND_PREFIX $COMMAND
