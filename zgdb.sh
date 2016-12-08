#!/bin/bash

BENCH=sjeng
OUTPUT_DIR=spec2006/${BENCH}
NR_MAXINSTS=20000
TLB_MEMORY_LATENCY=30ns
#DEBUG_FLAG=--debug-flag=LSQUnit,Cache,TLB,CoherentBus,Fetch

CPU_MODE=--cpu-type=inorder
#CPU_MODE=--cpu-type=detailed

#
# Checkpoints: 100 million
#
CHECKPOINT=1000
TAKE="--take-checkpoint=${CHECKPOINT} --at-instruction"
RESTORE="--restore-with-cpu inorder --checkpoint-restore=${CHECKPOINT} --at-instruction"

set -x
set -e

SPEC2006="perlbench bzip2 gcc mcf gobmk hmmer sjeng libquantum h264ref omnetpp astar xalancbmk"

gdb --args \
	./build/ALPHA_MESI_CMP_directory/gem5.opt	\
		${DEBUG_FLAG} -d ${OUTPUT_DIR}		\
		configs/spec2k6_classic/run.py		\
			--cpu-type=inorder --caches	\
			-b ${BENCH}			\
			--bench ${BENCH}		\
			${RESTORE}			\
			--maxinsts=${NR_MAXINSTS}
