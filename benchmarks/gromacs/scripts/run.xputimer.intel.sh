#!/bin/bash
source COMMAND.sh
echo $COMMAND
export ZET_ENABLE_PROGRAM_INSTRUMENTATION=1
export ZE_ENABLE_TRACING_LAYER=1

GTPIN_RESULTS_DIR=KOIPerf
PIN_KIT=$PIN_ROOT
HPCWL_COMMAND_PREFIX="$PIN_KIT/pin  -t $(TOOLS)/KOIPerf/Intel-GPU/CPUPinTool/obj-intel64/xpu-KOIPerf.so -outdir $GTPIN_RESULTS_DIR  -perfout cpu.onkernelperf.txt -probemode -gtpindir $GTPIN_KIT -gtpintool $(TOOLS)/KOIPerf/Intel-GPU/GTPinTool/build/GTPinKOIPerf.so -gt --gpuoutdir -gt $GTPIN_RESULTS_DIR  -gt --gpu_perfout -gt gpu.onkernelperf.out -gt --perfOnKernel -- "
time $HPCWL_COMMAND_PREFIX $COMMAND
