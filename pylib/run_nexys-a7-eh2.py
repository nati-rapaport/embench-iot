#!/usr/bin/env python3

# Python module to run programs on a run_nexys-a7-eh2 board

# Copyright (C) 2021 Embecosm Limited
#
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Embench module to run benchmark programs.

This version is suitable for a gdb with nexys-a7 eh2.
"""

__all__ = [
    'get_target_args',
    'build_benchmark_cmd',
    'decode_results',
]

import argparse
import re
import os
import subprocess
import shlex
import time

from embench_core import log

cpu_mhz = 50
openocd_proc = None

def get_target_args(remnant):
    """Parse left over arguments"""
    parser = argparse.ArgumentParser(description='Get target specific args')

    parser.add_argument(
        '--gdb-command',
        type=str,
        default='riscv64-unknown-elf-gdb',
        help='Command to invoke GDB',
    )
    parser.add_argument(
        '--openocd-command',
        type=str,
        default='openocd',
        help='Command to invoke the openocd',
    )
    parser.add_argument(
        '--cpu-mhz',
        type=int,
        default=1,
        help='Processor clock speed in MHz'
    )

    return parser.parse_args(remnant)

# perform flush
def flush(flush_cmd, str_path):
   try:
      log.info("Flushing nexys-a7-eh2 ...")
      # flush command
      flush_cmd = "%s -c \"set BITFILE swervolf_eh2.bit\" -f swervolf_nexys_program.cfg" % (os.path.join(".", flush_cmd))
      #flush_cmd = "%s -c \"set BITFILE swervolf_eh2_jdport.bit\" -f swervolf_nexys_program.cfg" % (os.path.join(".", flush_cmd))
      # start the flush process
      proc = subprocess.Popen(shlex.split(flush_cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=False, cwd=str_path)
      # wait for the flush to complete
      data, err = proc.communicate()
      # did we get an error
      if "DONE!!!" not in str(err) + str(data):
        log.error("error in fulshing device")
        log.debug(data)
        log.debug(err)
        exit(1)
   except Exception as e:
      log.debug("exception flush")
      print("lkjshlaksjhflaksjfhlaksdhflakjsdhflkasdhflkahsdlkahglkahfglkjadhf")
      raise e

def build_benchmark_cmd(bench, args):
    """Construct the command to run the benchmark.  "args" is a
       namespace with target specific arguments"""
    global cpu_mhz
    global openocd_proc
    cpu_mhz = args.cpu_mhz

    str_path = os.path.join(os.getcwd(),"config", "riscv32", "boards", "nexys-a7-eh2")
    cmd = f'{args.openocd_command}'
    # flush the device
    flush(cmd, str_path)
    # start openocd
    log.info("Execting %s with nexys-a7-eh2 ..." % bench)
    
    openocd_cmd = ("%s -f %s" % (os.path.join(str_path, cmd), os.path.join(str_path, "swervolf_nexys_eh2_debug.cfg")))
    print("ronen1")
    print(openocd_cmd)
    print("ronen1")
    #file_ = open("openocd_run_nexys-a7-eh2.txt", 'w')
    openocd_proc = subprocess.Popen(shlex.split(openocd_cmd), 
         stdin=subprocess.PIPE,
         stdout=subprocess.PIPE,
         #stdout=file_,
         stderr=subprocess.PIPE,
         #stderr=file_,
         cwd=None)
    time.sleep(3)
    """
    openocd_cmd = ("%s -f %s -c \"reg csr_MHARTSTART 0x3\" -c \"shutdown\"" % (os.path.join(str_path, cmd), os.path.join(str_path, "swervolf_nexys_eh2_debug_jdport_dual_hart_smp.cfg")))
    print(openocd_cmd)
    file_ = open("openocd_run_nexys-a7-eh2.txt", 'w')
    openocd_proc = subprocess.Popen(shlex.split(openocd_cmd), 
         stdin=subprocess.PIPE,
         #stdout=subprocess.PIPE,
         stdout=file_,
         #stderr=subprocess.PIPE,
         stderr=file_,
         cwd=None)
    #print("start openocd_proc.communicate()")
    openocd_proc.communicate()
    print("end openocd_proc.communicate()")
    time.sleep(2)

    openocd_cmd = ("%s -f %s" % (os.path.join(str_path, cmd), os.path.join(str_path, "swervolf_nexys_eh2_debug_jdport_dual_hart_smp.cfg")))

    print(openocd_cmd)
    openocd_proc = subprocess.Popen(shlex.split(openocd_cmd), 
         stdin=subprocess.PIPE,
         #stdout=subprocess.PIPE,
         stdout=file_,
         #stderr=subprocess.PIPE,
         stderr=file_,
         cwd=None)
    print("openocd_proc")
    
    time.sleep(2)
"""
    '''
    cmd = [
        f'{args.gdb_command}',
        #'-ex=\"set confirm off\"',
        '-ex=\"file ' + bench+ '\"',
        '-ex=\"set mem inaccessible-by-default off\"',
        '-ex=\"set remotetimeout 250\"',
        '-ex=\"set arch riscv:rv32\"',
        '-ex=\"target remote :3333"', 
        '-ex=\"load\"',
        #'-ex=\"delete breakpoints\"',
        #'-ex=\"si\"',
        #'-ex=\"si\"',
        #'-ex=\"break start_trigger\"',
        #'-ex=\"break stop_trigger\"',
        #'break _exit',
        #'set $initial_pc = $pc',
        #'thread apply all -q -s set $pc = $initial_pc',
        #'-ex=\"continue\"',
        #'-ex=\"print /u $mcycle\"',
        #'-ex=\"continue\"',
        #'-ex=\"print /u $mcycle\"',
        #'-ex=\"quit\"',
        #'-ex=\"continue\"',
        #'-ex=\"print /x $a0\"',
        #'-ex=\"quit\"'
    ]
    '''
    cmd = [f'{args.gdb_command}']
    gdb_comms = [
        'set confirm off',
        'file {0}',
        'target remote :3333',
        'set mem inaccessible-by-default off',
        'set remotetimeout 250',
        'set arch riscv:rv32',
        'load',
        'delete breakpoints',
        'break start_trigger',
        'break boardsupport.c:37',
        'break _complete',
#        'break _exit',
        'continue',
        'continue',
        'print start_c',
        #'print /u $minstret',
        'print start_i',
        'print end_c',
        #'print /u $minstret',
        'print end_i',
        'continue',
        'print /x $a0',
        'quit',
    ]

    for arg in gdb_comms:
        cmd.extend(['-ex', arg.format(bench)])

    #print (cmd)
    return cmd


def decode_results(stdout_str, stderr_str):
    global openocd_proc
    if openocd_proc.poll() == None:
        # terminate GDB process
        openocd_proc.terminate()
        # wait for process termination
        openocd_proc.wait()

    if stdout_str == None and stderr_str == None:
       return 0

    """Extract the results from the output string of the run. Return the
       elapsed time in milliseconds or zero if the run failed."""
    # Return code is in standard output. We look for the string that means we
    # hit a breakpoint on _exit, then for the string returning the value.

    rcstr = re.search(
        'Breakpoint 2 at.*startup\.S.*\$5 = (\d+)', stdout_str, re.S
    )
    print(rcstr)
    if not rcstr:
        log.debug('Warning: Failed to find return code')
        return 0.0

    # The start and end cycle counts are in the stderr string
    starttime = re.search('\$1 = (\d+)', stdout_str, re.S)
    endtime = re.search('\$3 = (\d+)', stdout_str, re.S)

    if not starttime or not endtime:
        log.debug('Warning: Failed to find timing')
        return 0.0

    # Time from cycles to milliseconds
    global cpu_mhz
    print (stdout_str)
    #print((int(endtime.group(1)) - int(starttime.group(1))))

    startinst = re.search('\$2 = (\d+)', stdout_str, re.S)
    endinst = re.search('\$4 = (\d+)', stdout_str, re.S)

    
    inst = int(endinst.group(1))-int(startinst.group(1))

    cyc = int(endtime.group(1)) - int(starttime.group(1))

    print("inst - %s" % (inst))

    print("ipc - %s" % (inst/cyc))
    
    print((int(endtime.group(1)) - int(starttime.group(1))) / cpu_mhz / 1000.0)
    
    return (int(endtime.group(1)) - int(starttime.group(1))) / cpu_mhz / 1000.0
