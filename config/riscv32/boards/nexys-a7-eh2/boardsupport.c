/* Chip support for No-LibC-NoLibGCC RISC-V configuration

   Copyright (C) 2019 Embecosm Limited and the University of Bristol

   Contributor Graham Markall <graham.markall@embecosm.com>

   This file is part of Embench and was formerly part of the Bristol/Embecosm
   Embedded Benchmark Suite.

   SPDX-License-Identifier: GPL-3.0-or-later */

#include "boardsupport.h"

void
initialise_board ()
{
    __asm__ volatile ("" : : : "memory");
}

volatile unsigned int start_c;
volatile unsigned int end_c;
volatile unsigned int start_i;
volatile unsigned int end_i;

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
start_trigger ()
{
    asm volatile ("csrr %0, mcycle" : "=r" (start_c)  : );
    asm volatile ("csrr %0, minstret" : "=r" (start_i)  : );
}

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
stop_trigger ()
{
    asm volatile ("csrr %0, mcycle" : "=r" (end_c)  : );
    asm volatile ("csrr %0, minstret" : "=r" (end_i)  : );
    asm volatile ("nop");
}
