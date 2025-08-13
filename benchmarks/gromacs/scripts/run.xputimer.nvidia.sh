#!/bin/bash
source COMMAND.sh
echo $COMMAND
export ZET_ENABLE_PROGRAM_INSTRUMENTATION=1
export ZE_ENABLE_TRACING_LAYER=1

RESULTS_DIR=KOIPerf
export TOOL_GPU_OUTDIR=$RESULTS_DIR
export TOOL_GPU_PERFOUT=gpu.onkernelperf.out
HPCWL_COMMAND_PREFIX="$PIN_ROOT/pin  -t $(TOOLS)/KOIPerf/NVIDIA-GPU/CPUPinTool/obj-intel64/xpu-pin-nvbit-handler.so -outdir $RESULTS_DIR -perfout cpu.onkernelperf.txt -probemode -nvbittool $(TOOLS)/KOIPerf/NVIDIA-GPU/NVBitTool/NVBitTool.so -- "

LD_PRELOAD=$(TOOLS)/KOIPerf/NVIDIA-GPU/NVBitTool/NVBitTool.so $HPCWL_COMMAND_PREFIX $COMMAND
