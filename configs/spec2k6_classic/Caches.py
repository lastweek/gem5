# Copyright (c) 2006-2007 The Regents of The University of Michigan
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
# Authors: Lisa Hsu

from m5.objects import *

class L1Cache(BaseCache):
    assoc = 2
    block_size = 64
    hit_latency = '3ns'
    response_latency = '1ns'
    mshrs = 10
    tgts_per_mshr = 20
    is_top_level = True

    def connectCPU(self, bus):
        self.mem_side = bus.slave

class L1ICache(L1Cache):
    size = '32kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '32kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

class L2Cache(BaseCache):
    size = '256kB'
    assoc = 8
    block_size = 64
    hit_latency = '12ns'
    response_latency = '12ns'
    mshrs = 20
    tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave

class L3Cache(BaseCache):
    size = '4MB'
    assoc = 8
    block_size = 64
    hit_latency = '20ns'
    response_latency = '20ns'
    mshrs = 64
    tgts_per_mshr = 12

class L4Cache(BaseCache):
    size = '64MB'
    assoc = 8
    block_size = 64
    hit_latency = '50ns'
    response_latency = '50ns'
    mshrs = 64
    tgts_per_mshr = 12


#class PageTableWalkerCache(BaseCache):
#    assoc = 2
#    block_size = 64
#    hit_latency = '1ns'
#    response_latency = '1ns'
#    mshrs = 10
#    size = '1kB'
#    tgts_per_mshr = 12
#    is_top_level = True

#class IOCache(BaseCache):
#    assoc = 8
#    block_size = 64
#    hit_latency = '10ns'
#    response_latency = '10ns'
#    mshrs = 20
#    size = '1kB'
#    tgts_per_mshr = 12
#    forward_snoops = False
#    is_top_level = True
