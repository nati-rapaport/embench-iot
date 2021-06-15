/*
 * SPDX-License-Identifier: Apache-2.0
 * Copyright 2019-2021 Western Digital Corporation or its affiliates.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/ 

/*
 Linker script
*/

OUTPUT_ARCH( "riscv" )

ENTRY( _start )

MEMORY
{
  ram  (wxa!ri) : ORIGIN = 0x00000000, LENGTH = 64M
  ram2 (wxa!ri) : ORIGIN = 0x04000000, LENGTH = 64M
  dccm (wxa!ri) : ORIGIN = 0xf0080000, LENGTH = 64K
}

PHDRS
{
  rom_load  PT_LOAD;
  ram_init  PT_LOAD;
  ram_load  PT_LOAD;
  dccm_load PT_LOAD;
}


/*----------------------------------------------------------------------*/
/* Sections                            */
/*----------------------------------------------------------------------*/

SECTIONS
{
  /* overall, stacks size here is 4K*2harts = 8K */
  __hart_stack_size = 5K;

  .text.init :
  {
    *(.text.init)
    . = ALIGN(8);
  } > ram : ram_load

  .text :
  {
    *(.text.unlikely .text.unlikely.*)
    *(.text.startup .text.startup.*)
    *(.text .text.*)
    *(.gnu.linkonce.t.*)
    . = ALIGN(4);
  } >ram : ram_load


  . = ORIGIN(dccm);

  .rodata :
  {
    *(.rdata)
    *(.rodata .rodata.*)
    *(.gnu.linkonce.r.*)
    . = ALIGN(4);
  } > dccm : dccm_load
 
  .lalign : 
  {
    . = ALIGN(4);
    PROVIDE( _data_lma = . );
  } > dccm : dccm_load
  
  .dalign :
  {
    . = ALIGN(4);
    PROVIDE( _data = . );
  } > dccm : dccm_load
  
 
  .data :
  {
    *(.data .data.*)
    *(.gnu.linkonce.d.*)
    . += 10; /* fix for linker false error message */
    . = ALIGN(8); 
  } > dccm : dccm_load

  .sdata :
  {
    . = ALIGN(8);
    __global_pointer$ = . + 0x800;
    *(.sdata .sdata.*)
    *(.gnu.linkonce.s.*)
    . = ALIGN(8);
    *(.srodata .srodata.*)
   . = ALIGN(8);
  } > dccm : dccm_load
  
  . = ALIGN(4);
  PROVIDE( _edata = . );
  PROVIDE( edata = . );

  PROVIDE( _fbss = . );
  PROVIDE( __bss_start = . );
  
  .bss :
  {
    *(.sbss .sbss.* .gnu.linkonce.sb.*)
    *(.scommon)
    *(.bss .bss.*) 
    . = ALIGN(8);
  } > dccm : dccm_load

  _end = .;  
 
  .stack_hart0 :
  {
    . = __hart_stack_size; 
    _sp_hart0 = .;
  } > dccm : dccm_load
  
  .stack_hart1 :
  {
    . = _sp_hart0;
    . = __hart_stack_size;
    _sp_hart1 = .;
  }> dccm : dccm_load
}
