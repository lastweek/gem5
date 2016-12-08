#!/bin/bash

#DEBUG_FLAG=--debug-flag=LSQUnit,Cache,TLB,CoherentBus,Fetch


#
# Checkpoints: 100 million
#
CHECKPOINT=1000
TAKE="--take-checkpoint=${CHECKPOINT} --at-instruction --simpoint"
RESTORE="--at-instruction --checkpoint-restore=${CHECKPOINT}"

set -x
set -e

SPEC2006_ALL="perlbench bzip2 gcc mcf gobmk hmmer sjeng libquantum h264ref omnetpp astar xalancbmk"
SPEC2006_1="perlbench bzip2"
SPEC2006_2="gcc mcf"
SPEC2006_3="gobmk hmmer"
SPEC2006_4="sjeng libquantum"
SPEC2006_5="h264ref omnetpp"
SPEC2006_6="astar xalancbmk"
CPU_MODE="--cpu-type=inorder --caches"
TLB_MEMORY_LATENCY=3000ns

NR_MAXINSTS=5000

for i in ${SPEC2006_1}; do
	BENCH=${i}
	OUTPUT_DIR=spec2006/${i}_${TLB_MEMORY_LATENCY}

	./build/ALPHA_MESI_CMP_directory/gem5.opt \
		${DEBUG_FLAG} -d ${OUTPUT_DIR}	\
		configs/spec2k6_classic/run.py  \
			${CPU_MODE} -b ${i} \
			--maxinsts=${NR_MAXINSTS} \
			-l ${TLB_MEMORY_LATENCY}
done
