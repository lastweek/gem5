#!/bin/bash

BENCH=sjeng
OUTPUT_DIR=tests/test1/${BENCH}
NR_MAXINSTS=1000
TLB_MEMORY_LATENCY=30ns
DEBUG_FLAG=--debug-flag=LSQUnit,Cache,TLB,CoherentBus,Fetch

#CPU_MODE=--cpu-type=inorder
CPU_MODE=--cpu-type=detailed

gdb --args \
	./build/ALPHA_MESI_CMP_directory/gem5.opt		\
		${DEBUG_FLAG} -d ${OUTPUT_DIR}			\
		configs/spec2k6_classic/run.py			\
			${CPU_MODE} --caches			\
			-b ${BENCH}				\
			--maxinsts=${NR_MAXINSTS}		\
			-l ${TLB_MEMORY_LATENCY}
