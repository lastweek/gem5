./build/ALPHA_MESI_CMP_directory/gem5.opt  \
	--debug-flags=InOrderCachePort,InOrderTLB \
	configs/spec2k6_classic/run.py --cpu-type=inorder --caches \
	-b bzip2 --maxinsts=1

