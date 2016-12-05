#!/bin/bash

#DEBUG_FLAG=--debug-flag=TLB,CoherentBus

#./build/ALPHA_MESI_CMP_directory/gem5.opt --debug-flag=InOrderExecute -d tests/${1}/${2} configs/spec2k6/run.py --cpu-type=inorder --caches -b ${2} --maxinsts=${3}

#./build/ALPHA_MESI_CMP_directory/gem5.opt --debug-flag=InOrderCachePort -d tests/${1}/sjeng configs/test/run.py --cpu-type=inorder --caches -b sjeng --maxinsts=10000
gdb --args ./build/ALPHA_MESI_CMP_directory/gem5.opt ${DEBUG_FLAG} -d tests/test1/sjeng configs/spec2k6_classic/run.py --cpu-type=inorder --caches -b sjeng --maxinsts=1000000
#./build/ALPHA_MESI_CMP_directory/gem5.opt -d tests/test1/sjeng configs/spec2k6_classic/run.py --cpu-type=inorder --caches -b sjeng --maxinsts=1000000000
#gdb -args ./build/ALPHA_MESI_CMP_directory/gem5.opt --debug-flag=TLB --debug-flag=InOrderCachePort --debug-flag=InOrderTLB -d tests/test1/sjeng configs/spec2k6_classic/run.py --cpu-type=inorder --caches -b sjeng --maxinsts=1
#./build/ALPHA_MESI_CMP_directory/gem5.opt --debug-flag=TLB --debug-flag=BusAddrRanges --debug-flag=CoherentBus --debug-flag=InOrderCachePort --debug-flag=InOrderTLB --debug-flag=Cache -d tests/${1}/sjeng configs/spec2k6_classic/run.py --cpu-type=inorder --caches -b sjeng --maxinsts=${2}
#./build/ALPHA_MESI_CMP_directory/gem5.opt --debug-flag=InOrderTLB -d tests/${1}/${2} configs/spec2k6/run.py --cpu-type=inorder --caches -b ${2} --maxinsts=${3}
