# Makefile.benchmark - GROMACS benchmark

GROMACS_VERSION := 2023.3
GROMACS_URL := https://ftp.gromacs.org/gromacs/gromacs-$(GROMACS_VERSION).tar.gz
GROMACS_DIR := gromacs-$(GROMACS_VERSION)
BUILD_DIR := $(GROMACS_DIR)/build
INSTALL_DIR := $(PWD)/Install

ifndef PROJ_ROOT
	PROJ_ROOT := $(abspath $(CURDIR)/../..)
endif
TOOLS_DIR := $(PROJ_ROOT)/tools
CMAKE_VERSION := 3.30.7
CMAKE_URL := https://github.com/Kitware/CMake/releases/download/v$(CMAKE_VERSION)/cmake-$(CMAKE_VERSION)-linux-x86_64.tar.gz
CMAKE_DIR := $(TOOLS_DIR)/cmake-$(CMAKE_VERSION)-linux-x86_64
CMAKE_BIN := $(CMAKE_DIR)/bin/cmake


TEST_DIR := test
BENCHMEM_URL := https://www.mpinat.mpg.de/benchMEM
BENCHMEM_ZIP := benchMEM.zip

.PHONY: all help download build-intel build-nvidia testcase cmake
.PHONY: intel nvidia clean-install clean-test clean-cmake clean

all: help

download:
	@if [ ! -d "$(GROMACS_DIR)" ]; then \
		echo "Downloading GROMACS $(GROMACS_VERSION)"; \
		wget -O - $(GROMACS_URL) --no-check-certificate --quiet --show-progress | tar -xf - -z ; \
	fi

cmake: $(CMAKE_BIN)

$(CMAKE_BIN):
	@echo "Downloading CMAKE $(CMAKE_VERSION)"; \
	wget -O - $(CMAKE_URL) --no-check-certificate --quiet --show-progress | tar -xf - -z -C $(TOOLS_DIR) ; \

build-intel: download cmake
	@mkdir -p $(INSTALL_DIR)
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && \
	$(CMAKE_BIN) .. \
		-DGMX_GPU=SYCL \
		-DGMX_BUILD_OWN_FFTW=ON \
		-DCMAKE_CXX_COMPILER=icpx \
		-DCMAKE_C_COMPILER=icx \
		-DCMAKE_INSTALL_PREFIX=$(INSTALL_DIR) \
		-DGMXAPI=OFF \
		-DGMX_GPU_NB_CLUSTER_SIZE=8 \
		-DGMX_GPU_NB_NUM_CLUSTER_PER_CELL_X=1 \
		-DGMX_FFT_LIBRARY=mkl \
		-DCMAKE_DISABLE_FIND_PACKAGE_MPI=on && \
	$(MAKE) -j$(shell nproc) && \
	$(MAKE) install

build-nvidia: download cmake
	@mkdir -p $(INSTALL_DIR)
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && \
	$(CMAKE_BIN) .. \
		-DGMX_GPU=CUDA \
		-DGMX_BUILD_OWN_FFTW=ON \
		-DCMAKE_INSTALL_PREFIX=$(INSTALL_DIR) \
		-DGMXAPI=OFF \
		-DGMX_GPU_NB_CLUSTER_SIZE=8 \
		-DGMX_GPU_NB_NUM_CLUSTER_PER_CELL_X=2 \
		-DGMX_FFT_LIBRARY=fftw3 \
		-DCMAKE_DISABLE_FIND_PACKAGE_MPI=on && \
	$(MAKE) -j$(shell nproc) && \
	$(MAKE) install

testcase:
	@mkdir -p $(TEST_DIR)
	@cd $(TEST_DIR) && \
	if [ ! -f "$(BENCHMEM_ZIP)" ]; then \
		wget -O $(BENCHMEM_ZIP) $(BENCHMEM_URL) || curl -L -o $(BENCHMEM_ZIP) $(BENCHMEM_URL); \
		if [ -f "$(BENCHMEM_ZIP)" ]; then \
			unzip -q $(BENCHMEM_ZIP) || echo "Note: unzip failed, please extract manually"; \
		else \
			echo "Failed to download benchMEM. Please download manually from $(BENCHMEM_URL)"; \
		fi; \
	fi

intel: build-intel testcase

nvidia: build-nvidia testcase

clean-install:
	-rm -rf $(BUILD_DIR)
	-rm -rf $(INSTALL_DIR)

clean-test:
	-rm -rf $(TEST_DIR)

clean-cmake:
	-rm -rf $(CMAKE_DIR)

clean: clean-install clean-test
	-rm -rf $(GROMACS_DIR)

help:
	@echo "GROMACS Benchmark Setup"
	@echo "======================="
	@echo ""
	@echo "Platform targets:"
	@echo "  intel           - Build benchmark and testcase for Intel GPU"
	@echo "  nvidia          - Build benchmark and testcase for NVIDIA GPU"
	@echo ""
	@echo "Setup targets:"
	@echo "  download      - Download GROMACS source code"
	@echo "  build-intel   - Build GROMACS for Intel GPU"
	@echo "  build-nvidia  - Build GROMACS for NVIDIA GPU"
	@echo "  testcase      - Download benchMEM"
	@echo ""
	@echo "Cleaning targets:"
	@echo "  clean-install   - Clean GROMACS build artifacts"
	@echo "  clean-test      - Clean benchmark test files"
	@echo "  clean           - Clean everything including source"
