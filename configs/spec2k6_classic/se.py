# Copyright (c) 2012 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2006-2008 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Steve Reinhardt

# Simple test script
#
# "m5 test.py"

import optparse
import sys

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal

addToPath('../common')
addToPath('../ruby')
addToPath('../topologies')

import Options
import Ruby
import Simulation
import CacheConfig
from Caches import *
from cpu2000 import *

import spec2k6

def get_processes(options):
    """Interprets provided options and returns a list of processes"""

    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []

    workloads = options.cmd.split(';')
    if options.input != "":
        inputs = options.input.split(';')
    if options.output != "":
        outputs = options.output.split(';')
    if options.errout != "":
        errouts = options.errout.split(';')
    if options.options != "":
        pargs = options.options.split(';')

    idx = 0
    for wrkld in workloads:
        process = LiveProcess()
        process.executable = wrkld

        if len(pargs) > idx:
            process.cmd = [wrkld] + pargs[idx].split()
        else:
            process.cmd = [wrkld]

        if len(inputs) > idx:
            process.input = inputs[idx]
        if len(outputs) > idx:
            process.output = outputs[idx]
        if len(errouts) > idx:
            process.errout = errouts[idx]

        multiprocesses.append(process)
        idx += 1

    if options.smt:
        assert(options.cpu_type == "detailed" or options.cpu_type == "inorder")
        return multiprocesses, idx
    else:
        return multiprocesses, 1


parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

if '--ruby' in sys.argv:
    Ruby.define_options(parser)

(options, args) = parser.parse_args()

if args:
    print "Error: script doesn't take any positional arguments"
    sys.exit(1)

multiprocesses = []
numThreads = 1

if options.bench == 'perlbench':
   process = spec2k6.perlbench
elif options.bench == 'bzip2':
   process = spec2k6.bzip2
elif options.bench == 'gcc':
   process = spec2k6.gcc
elif options.bench == 'bwaves':
   process = spec2k6.bwaves
elif options.bench == 'gamess':
   process = spec2k6.gamess
elif options.bench == 'mcf':
   process = spec2k6.mcf
elif options.bench == 'milc':
   process = spec2k6.milc
elif options.bench == 'zeusmp':
   process = spec2k6.zeusmp
elif options.bench == 'gromacs':
   process = spec2k6.gromacs
elif options.bench == 'cactusADM':
   process = spec2k6.cactusADM
elif options.bench == 'leslie3d':
   process = spec2k6.leslie3d
elif options.bench == 'namd':
   process = spec2k6.namd
elif options.bench == 'gobmk':
   process = spec2k6.gobmk;
elif options.bench == 'dealII':
   process = spec2k6.dealII
elif options.bench == 'soplex':
   process = spec2k6.soplex
elif options.bench == 'povray':
   process = spec2k6.povray
elif options.bench == 'calculix':
   process = spec2k6.calculix
elif options.bench == 'hmmer':
   process = spec2k6.hmmer
elif options.bench == 'sjeng':
   process = spec2k6.sjeng
elif options.bench == 'GemsFDTD':
   process = spec2k6.GemsFDTD
elif options.bench == 'libquantum':
   process = spec2k6.libquantum
elif options.bench == 'h264ref':
   process = spec2k6.h264ref
elif options.bench == 'tonto':
   process = spec2k6.tonto
elif options.bench == 'lbm':
   process = spec2k6.lbm
elif options.bench == 'omnetpp':
   process = spec2k6.omnetpp
elif options.bench == 'astar':
   process = spec2k6.astar
elif options.bench == 'wrf':
   process = spec2k6.wrf
elif options.bench == 'sphinx3':
   process = spec2k6.sphinx3
elif options.bench == 'xalancbmk':
   process = spec2k6.xalancbmk
elif options.bench == 'specrand_i':
   process = spec2k6.specrand_i
elif options.bench == 'specrand_f':
   process = spec2k6.specrand_f


multiprocesses.append(process)

(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)
CPUClass.clock = options.clock
CPUClass.numThreads = numThreads

# Check -- do not allow SMT with multiple CPUs
if options.smt and options.num_cpus > 1:
    fatal("You cannot use SMT with multiple CPUs!")

np = options.num_cpus
system = System(cpu = [CPUClass(cpu_id=i) for i in xrange(np)],
                physmem = SimpleMemory(range=AddrRange("512MB")),
                membus = CoherentBus(), mem_mode = test_mem_mode)

# Sanity check
if options.fastmem and (options.caches or options.l2cache):
    fatal("You cannot use fastmem in combination with caches!")

for i in xrange(np):
    if options.smt:
        system.cpu[i].workload = multiprocesses
    elif len(multiprocesses) == 1:
        system.cpu[i].workload = multiprocesses[0]
    else:
        system.cpu[i].workload = multiprocesses[i]

    if options.fastmem:
        system.cpu[i].fastmem = True

    if options.checker:
        system.cpu[i].addCheckerCpu()

if options.ruby:
    if not (options.cpu_type == "detailed" or options.cpu_type == "timing"):
        print >> sys.stderr, "Ruby requires TimingSimpleCPU or O3CPU!!"
        sys.exit(1)

    options.use_map = True
    Ruby.create_system(options, system)
    assert(options.num_cpus == len(system.ruby._cpu_ruby_ports))

    for i in xrange(np):
        ruby_port = system.ruby._cpu_ruby_ports[i]

        # Create the interrupt controller and connect its ports to Ruby
        # Note that the interrupt controller is always present but only
        # in x86 does it have message ports that need to be connected
        system.cpu[i].createInterruptController()

        # Connect the cpu's cache ports to Ruby
        system.cpu[i].icache_port = ruby_port.slave
        system.cpu[i].dcache_port = ruby_port.slave
        if buildEnv['TARGET_ISA'] == 'x86':
            system.cpu[i].interrupts.pio = ruby_port.master
            system.cpu[i].interrupts.int_master = ruby_port.slave
            system.cpu[i].interrupts.int_slave = ruby_port.master
            system.cpu[i].itb.walker.port = ruby_port.slave
            system.cpu[i].dtb.walker.port = ruby_port.slave
else:
    system.system_port = system.membus.slave
    system.physmem.port = system.membus.master
    CacheConfig.config_cache(options, system)

root = Root(full_system = False, system = system)
Simulation.run(options, root, system, FutureClass)
