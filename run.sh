./build/ALPHA_MESI_CMP_directory/gem5.opt  \
	--debug-flags=InOrderCachePort,InOrderTLB,CoherentBus,NoncoherentBus,DRAM \
	configs/spec2k6/run.py --cpu-type=inorder --caches \
	-b bzip2 --maxinsts=1

