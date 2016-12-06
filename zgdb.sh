#!/bin/bash

BENCH=sjeng
OUTPUT_DIR=tests/test1/${BENCH}
NR_MAXINSTS=2
TLB_MEMORY_LATENCY=3000ns
__FLAG=Cache,TLB,CoherentBus
DEBUG_FLAG=--debug-flag=${__FLAG}

gdb --args \
	./build/ALPHA_MESI_CMP_directory/gem5.opt		\
		${DEBUG_FLAG} -d ${OUTPUT_DIR}			\
		configs/spec2k6_classic/run.py			\
			--cpu-type=detailed --caches			\
			-b ${BENCH}				\
			--maxinsts=${NR_MAXINSTS}		\
			-l ${TLB_MEMORY_LATENCY}
