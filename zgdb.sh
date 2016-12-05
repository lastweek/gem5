#!/bin/bash

BENCH=sjeng
OUTPUT_DIR=tests/test1/${BENCH}
NR_MAXINSTS=2
TLB_MEMORY_LATENCY=40ns
#DEBUG_FLAG=--debug-flag=TLB,CoherentBus,InOrderCPU,Cache

gdb --args \
	./build/ALPHA_MESI_CMP_directory/gem5.opt		\
		${DEBUG_FLAG} -d ${OUTPUT_DIR}			\
		configs/spec2k6_classic/run.py			\
			--cpu-type=inorder --caches		\
			-b ${BENCH}				\
			--maxinsts=${NR_MAXINSTS}		\
			-l ${TLB_MEMORY_LATENCY}
