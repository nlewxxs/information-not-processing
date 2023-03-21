/*
 * system.h - SOPC Builder system and BSP software package information
 *
 * Machine generated for CPU 'cpu' in SOPC Builder design 'nios_controller'
 * SOPC Builder design path: C:/Users/andre/IP/Coursework/Golden_Top/nios_controller.sopcinfo
 *
 * Generated: Tue Mar 21 16:10:57 GMT 2023
 */

/*
 * DO NOT MODIFY THIS FILE
 *
 * Changing this file will have subtle consequences
 * which will almost certainly lead to a nonfunctioning
 * system. If you do modify this file, be aware that your
 * changes will be overwritten and lost when this file
 * is generated again.
 *
 * DO NOT MODIFY THIS FILE
 */

/*
 * License Agreement
 *
 * Copyright (c) 2008
 * Altera Corporation, San Jose, California, USA.
 * All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 *
 * This agreement shall be governed in all respects by the laws of the State
 * of California and by the laws of the United States of America.
 */

#ifndef __SYSTEM_H_
#define __SYSTEM_H_

/* Include definitions from linker script generator */
#include "linker.h"


/*
 * CPU configuration
 *
 */

#define ALT_CPU_ARCHITECTURE "altera_nios2_gen2"
#define ALT_CPU_BIG_ENDIAN 0
#define ALT_CPU_BREAK_ADDR 0x00040820
#define ALT_CPU_CPU_ARCH_NIOS2_R1
#define ALT_CPU_CPU_FREQ 50000000u
#define ALT_CPU_CPU_ID_SIZE 1
#define ALT_CPU_CPU_ID_VALUE 0x00000000
#define ALT_CPU_CPU_IMPLEMENTATION "tiny"
#define ALT_CPU_DATA_ADDR_WIDTH 0x13
#define ALT_CPU_DCACHE_LINE_SIZE 0
#define ALT_CPU_DCACHE_LINE_SIZE_LOG2 0
#define ALT_CPU_DCACHE_SIZE 0
#define ALT_CPU_EXCEPTION_ADDR 0x00020020
#define ALT_CPU_FLASH_ACCELERATOR_LINES 0
#define ALT_CPU_FLASH_ACCELERATOR_LINE_SIZE 0
#define ALT_CPU_FLUSHDA_SUPPORTED
#define ALT_CPU_FREQ 50000000
#define ALT_CPU_HARDWARE_DIVIDE_PRESENT 0
#define ALT_CPU_HARDWARE_MULTIPLY_PRESENT 0
#define ALT_CPU_HARDWARE_MULX_PRESENT 0
#define ALT_CPU_HAS_DEBUG_CORE 1
#define ALT_CPU_HAS_DEBUG_STUB
#define ALT_CPU_HAS_ILLEGAL_INSTRUCTION_EXCEPTION
#define ALT_CPU_HAS_JMPI_INSTRUCTION
#define ALT_CPU_ICACHE_LINE_SIZE 0
#define ALT_CPU_ICACHE_LINE_SIZE_LOG2 0
#define ALT_CPU_ICACHE_SIZE 0
#define ALT_CPU_INST_ADDR_WIDTH 0x13
#define ALT_CPU_NAME "cpu"
#define ALT_CPU_OCI_VERSION 1
#define ALT_CPU_RESET_ADDR 0x00020000


/*
 * CPU configuration (with legacy prefix - don't use these anymore)
 *
 */

#define NIOS2_BIG_ENDIAN 0
#define NIOS2_BREAK_ADDR 0x00040820
#define NIOS2_CPU_ARCH_NIOS2_R1
#define NIOS2_CPU_FREQ 50000000u
#define NIOS2_CPU_ID_SIZE 1
#define NIOS2_CPU_ID_VALUE 0x00000000
#define NIOS2_CPU_IMPLEMENTATION "tiny"
#define NIOS2_DATA_ADDR_WIDTH 0x13
#define NIOS2_DCACHE_LINE_SIZE 0
#define NIOS2_DCACHE_LINE_SIZE_LOG2 0
#define NIOS2_DCACHE_SIZE 0
#define NIOS2_EXCEPTION_ADDR 0x00020020
#define NIOS2_FLASH_ACCELERATOR_LINES 0
#define NIOS2_FLASH_ACCELERATOR_LINE_SIZE 0
#define NIOS2_FLUSHDA_SUPPORTED
#define NIOS2_HARDWARE_DIVIDE_PRESENT 0
#define NIOS2_HARDWARE_MULTIPLY_PRESENT 0
#define NIOS2_HARDWARE_MULX_PRESENT 0
#define NIOS2_HAS_DEBUG_CORE 1
#define NIOS2_HAS_DEBUG_STUB
#define NIOS2_HAS_ILLEGAL_INSTRUCTION_EXCEPTION
#define NIOS2_HAS_JMPI_INSTRUCTION
#define NIOS2_ICACHE_LINE_SIZE 0
#define NIOS2_ICACHE_LINE_SIZE_LOG2 0
#define NIOS2_ICACHE_SIZE 0
#define NIOS2_INST_ADDR_WIDTH 0x13
#define NIOS2_OCI_VERSION 1
#define NIOS2_RESET_ADDR 0x00020000


/*
 * Define for each module class mastered by the CPU
 *
 */

#define __ALTERA_AVALON_JTAG_UART
#define __ALTERA_AVALON_ONCHIP_MEMORY2
#define __ALTERA_AVALON_PIO
#define __ALTERA_AVALON_SYSID_QSYS
#define __ALTERA_AVALON_TIMER
#define __ALTERA_NIOS2_GEN2
#define __ALTERA_UP_AVALON_ACCELEROMETER_SPI


/*
 * System configuration
 *
 */

#define ALT_DEVICE_FAMILY "MAX 10"
#define ALT_IRQ_BASE NULL
#define ALT_LEGACY_INTERRUPT_API_PRESENT
#define ALT_LOG_PORT "/dev/null"
#define ALT_LOG_PORT_BASE 0x0
#define ALT_LOG_PORT_DEV null
#define ALT_LOG_PORT_TYPE ""
#define ALT_NUM_EXTERNAL_INTERRUPT_CONTROLLERS 0
#define ALT_NUM_INTERNAL_INTERRUPT_CONTROLLERS 1
#define ALT_NUM_INTERRUPT_CONTROLLERS 1
#define ALT_STDERR "/dev/jtag_uart"
#define ALT_STDERR_BASE 0x410a8
#define ALT_STDERR_DEV jtag_uart
#define ALT_STDERR_IS_JTAG_UART
#define ALT_STDERR_PRESENT
#define ALT_STDERR_TYPE "altera_avalon_jtag_uart"
#define ALT_STDIN "/dev/jtag_uart"
#define ALT_STDIN_BASE 0x410a8
#define ALT_STDIN_DEV jtag_uart
#define ALT_STDIN_IS_JTAG_UART
#define ALT_STDIN_PRESENT
#define ALT_STDIN_TYPE "altera_avalon_jtag_uart"
#define ALT_STDOUT "/dev/jtag_uart"
#define ALT_STDOUT_BASE 0x410a8
#define ALT_STDOUT_DEV jtag_uart
#define ALT_STDOUT_IS_JTAG_UART
#define ALT_STDOUT_PRESENT
#define ALT_STDOUT_TYPE "altera_avalon_jtag_uart"
#define ALT_SYSTEM_NAME "nios_controller"


/*
 * accelerometer_spi configuration
 *
 */

#define ACCELEROMETER_SPI_BASE 0x410b0
#define ACCELEROMETER_SPI_IRQ 1
#define ACCELEROMETER_SPI_IRQ_INTERRUPT_CONTROLLER_ID 0
#define ACCELEROMETER_SPI_NAME "/dev/accelerometer_spi"
#define ACCELEROMETER_SPI_SPAN 2
#define ACCELEROMETER_SPI_TYPE "altera_up_avalon_accelerometer_spi"
#define ALT_MODULE_CLASS_accelerometer_spi altera_up_avalon_accelerometer_spi


/*
 * filter_x_in configuration
 *
 */

#define ALT_MODULE_CLASS_filter_x_in altera_avalon_pio
#define FILTER_X_IN_BASE 0x41060
#define FILTER_X_IN_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_X_IN_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_X_IN_CAPTURE 0
#define FILTER_X_IN_DATA_WIDTH 32
#define FILTER_X_IN_DO_TEST_BENCH_WIRING 0
#define FILTER_X_IN_DRIVEN_SIM_VALUE 0
#define FILTER_X_IN_EDGE_TYPE "NONE"
#define FILTER_X_IN_FREQ 50000000
#define FILTER_X_IN_HAS_IN 0
#define FILTER_X_IN_HAS_OUT 1
#define FILTER_X_IN_HAS_TRI 0
#define FILTER_X_IN_IRQ -1
#define FILTER_X_IN_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_X_IN_IRQ_TYPE "NONE"
#define FILTER_X_IN_NAME "/dev/filter_x_in"
#define FILTER_X_IN_RESET_VALUE 0
#define FILTER_X_IN_SPAN 16
#define FILTER_X_IN_TYPE "altera_avalon_pio"


/*
 * filter_x_out configuration
 *
 */

#define ALT_MODULE_CLASS_filter_x_out altera_avalon_pio
#define FILTER_X_OUT_BASE 0x41070
#define FILTER_X_OUT_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_X_OUT_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_X_OUT_CAPTURE 0
#define FILTER_X_OUT_DATA_WIDTH 32
#define FILTER_X_OUT_DO_TEST_BENCH_WIRING 0
#define FILTER_X_OUT_DRIVEN_SIM_VALUE 0
#define FILTER_X_OUT_EDGE_TYPE "NONE"
#define FILTER_X_OUT_FREQ 50000000
#define FILTER_X_OUT_HAS_IN 1
#define FILTER_X_OUT_HAS_OUT 0
#define FILTER_X_OUT_HAS_TRI 0
#define FILTER_X_OUT_IRQ -1
#define FILTER_X_OUT_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_X_OUT_IRQ_TYPE "NONE"
#define FILTER_X_OUT_NAME "/dev/filter_x_out"
#define FILTER_X_OUT_RESET_VALUE 0
#define FILTER_X_OUT_SPAN 16
#define FILTER_X_OUT_TYPE "altera_avalon_pio"


/*
 * filter_y_in configuration
 *
 */

#define ALT_MODULE_CLASS_filter_y_in altera_avalon_pio
#define FILTER_Y_IN_BASE 0x41050
#define FILTER_Y_IN_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_Y_IN_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_Y_IN_CAPTURE 0
#define FILTER_Y_IN_DATA_WIDTH 32
#define FILTER_Y_IN_DO_TEST_BENCH_WIRING 0
#define FILTER_Y_IN_DRIVEN_SIM_VALUE 0
#define FILTER_Y_IN_EDGE_TYPE "NONE"
#define FILTER_Y_IN_FREQ 50000000
#define FILTER_Y_IN_HAS_IN 0
#define FILTER_Y_IN_HAS_OUT 1
#define FILTER_Y_IN_HAS_TRI 0
#define FILTER_Y_IN_IRQ -1
#define FILTER_Y_IN_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_Y_IN_IRQ_TYPE "NONE"
#define FILTER_Y_IN_NAME "/dev/filter_y_in"
#define FILTER_Y_IN_RESET_VALUE 0
#define FILTER_Y_IN_SPAN 16
#define FILTER_Y_IN_TYPE "altera_avalon_pio"


/*
 * filter_y_out configuration
 *
 */

#define ALT_MODULE_CLASS_filter_y_out altera_avalon_pio
#define FILTER_Y_OUT_BASE 0x41040
#define FILTER_Y_OUT_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_Y_OUT_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_Y_OUT_CAPTURE 0
#define FILTER_Y_OUT_DATA_WIDTH 32
#define FILTER_Y_OUT_DO_TEST_BENCH_WIRING 0
#define FILTER_Y_OUT_DRIVEN_SIM_VALUE 0
#define FILTER_Y_OUT_EDGE_TYPE "NONE"
#define FILTER_Y_OUT_FREQ 50000000
#define FILTER_Y_OUT_HAS_IN 1
#define FILTER_Y_OUT_HAS_OUT 0
#define FILTER_Y_OUT_HAS_TRI 0
#define FILTER_Y_OUT_IRQ -1
#define FILTER_Y_OUT_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_Y_OUT_IRQ_TYPE "NONE"
#define FILTER_Y_OUT_NAME "/dev/filter_y_out"
#define FILTER_Y_OUT_RESET_VALUE 0
#define FILTER_Y_OUT_SPAN 16
#define FILTER_Y_OUT_TYPE "altera_avalon_pio"


/*
 * filter_z_in configuration
 *
 */

#define ALT_MODULE_CLASS_filter_z_in altera_avalon_pio
#define FILTER_Z_IN_BASE 0x41030
#define FILTER_Z_IN_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_Z_IN_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_Z_IN_CAPTURE 0
#define FILTER_Z_IN_DATA_WIDTH 32
#define FILTER_Z_IN_DO_TEST_BENCH_WIRING 0
#define FILTER_Z_IN_DRIVEN_SIM_VALUE 0
#define FILTER_Z_IN_EDGE_TYPE "NONE"
#define FILTER_Z_IN_FREQ 50000000
#define FILTER_Z_IN_HAS_IN 0
#define FILTER_Z_IN_HAS_OUT 1
#define FILTER_Z_IN_HAS_TRI 0
#define FILTER_Z_IN_IRQ -1
#define FILTER_Z_IN_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_Z_IN_IRQ_TYPE "NONE"
#define FILTER_Z_IN_NAME "/dev/filter_z_in"
#define FILTER_Z_IN_RESET_VALUE 0
#define FILTER_Z_IN_SPAN 16
#define FILTER_Z_IN_TYPE "altera_avalon_pio"


/*
 * filter_z_out configuration
 *
 */

#define ALT_MODULE_CLASS_filter_z_out altera_avalon_pio
#define FILTER_Z_OUT_BASE 0x41020
#define FILTER_Z_OUT_BIT_CLEARING_EDGE_REGISTER 0
#define FILTER_Z_OUT_BIT_MODIFYING_OUTPUT_REGISTER 0
#define FILTER_Z_OUT_CAPTURE 0
#define FILTER_Z_OUT_DATA_WIDTH 32
#define FILTER_Z_OUT_DO_TEST_BENCH_WIRING 0
#define FILTER_Z_OUT_DRIVEN_SIM_VALUE 0
#define FILTER_Z_OUT_EDGE_TYPE "NONE"
#define FILTER_Z_OUT_FREQ 50000000
#define FILTER_Z_OUT_HAS_IN 1
#define FILTER_Z_OUT_HAS_OUT 0
#define FILTER_Z_OUT_HAS_TRI 0
#define FILTER_Z_OUT_IRQ -1
#define FILTER_Z_OUT_IRQ_INTERRUPT_CONTROLLER_ID -1
#define FILTER_Z_OUT_IRQ_TYPE "NONE"
#define FILTER_Z_OUT_NAME "/dev/filter_z_out"
#define FILTER_Z_OUT_RESET_VALUE 0
#define FILTER_Z_OUT_SPAN 16
#define FILTER_Z_OUT_TYPE "altera_avalon_pio"


/*
 * hal configuration
 *
 */

#define ALT_INCLUDE_INSTRUCTION_RELATED_EXCEPTION_API
#define ALT_MAX_FD 32
#define ALT_SYS_CLK TIMER
#define ALT_TIMESTAMP_CLK none


/*
 * hex_display configuration
 *
 */

#define ALT_MODULE_CLASS_hex_display altera_avalon_pio
#define HEX_DISPLAY_BASE 0x41080
#define HEX_DISPLAY_BIT_CLEARING_EDGE_REGISTER 0
#define HEX_DISPLAY_BIT_MODIFYING_OUTPUT_REGISTER 0
#define HEX_DISPLAY_CAPTURE 0
#define HEX_DISPLAY_DATA_WIDTH 16
#define HEX_DISPLAY_DO_TEST_BENCH_WIRING 0
#define HEX_DISPLAY_DRIVEN_SIM_VALUE 0
#define HEX_DISPLAY_EDGE_TYPE "NONE"
#define HEX_DISPLAY_FREQ 50000000
#define HEX_DISPLAY_HAS_IN 0
#define HEX_DISPLAY_HAS_OUT 1
#define HEX_DISPLAY_HAS_TRI 0
#define HEX_DISPLAY_IRQ -1
#define HEX_DISPLAY_IRQ_INTERRUPT_CONTROLLER_ID -1
#define HEX_DISPLAY_IRQ_TYPE "NONE"
#define HEX_DISPLAY_NAME "/dev/hex_display"
#define HEX_DISPLAY_RESET_VALUE 0
#define HEX_DISPLAY_SPAN 16
#define HEX_DISPLAY_TYPE "altera_avalon_pio"


/*
 * jtag_uart configuration
 *
 */

#define ALT_MODULE_CLASS_jtag_uart altera_avalon_jtag_uart
#define JTAG_UART_BASE 0x410a8
#define JTAG_UART_IRQ 2
#define JTAG_UART_IRQ_INTERRUPT_CONTROLLER_ID 0
#define JTAG_UART_NAME "/dev/jtag_uart"
#define JTAG_UART_READ_DEPTH 64
#define JTAG_UART_READ_THRESHOLD 8
#define JTAG_UART_SPAN 8
#define JTAG_UART_TYPE "altera_avalon_jtag_uart"
#define JTAG_UART_WRITE_DEPTH 64
#define JTAG_UART_WRITE_THRESHOLD 8


/*
 * led configuration
 *
 */

#define ALT_MODULE_CLASS_led altera_avalon_pio
#define LED_BASE 0x41090
#define LED_BIT_CLEARING_EDGE_REGISTER 0
#define LED_BIT_MODIFYING_OUTPUT_REGISTER 0
#define LED_CAPTURE 0
#define LED_DATA_WIDTH 10
#define LED_DO_TEST_BENCH_WIRING 0
#define LED_DRIVEN_SIM_VALUE 0
#define LED_EDGE_TYPE "NONE"
#define LED_FREQ 50000000
#define LED_HAS_IN 0
#define LED_HAS_OUT 1
#define LED_HAS_TRI 0
#define LED_IRQ -1
#define LED_IRQ_INTERRUPT_CONTROLLER_ID -1
#define LED_IRQ_TYPE "NONE"
#define LED_NAME "/dev/led"
#define LED_RESET_VALUE 0
#define LED_SPAN 16
#define LED_TYPE "altera_avalon_pio"


/*
 * onchip_memory configuration
 *
 */

#define ALT_MODULE_CLASS_onchip_memory altera_avalon_onchip_memory2
#define ONCHIP_MEMORY_ALLOW_IN_SYSTEM_MEMORY_CONTENT_EDITOR 0
#define ONCHIP_MEMORY_ALLOW_MRAM_SIM_CONTENTS_ONLY_FILE 0
#define ONCHIP_MEMORY_BASE 0x20000
#define ONCHIP_MEMORY_CONTENTS_INFO ""
#define ONCHIP_MEMORY_DUAL_PORT 0
#define ONCHIP_MEMORY_GUI_RAM_BLOCK_TYPE "AUTO"
#define ONCHIP_MEMORY_INIT_CONTENTS_FILE "nios_controller_onchip_memory"
#define ONCHIP_MEMORY_INIT_MEM_CONTENT 0
#define ONCHIP_MEMORY_INSTANCE_ID "NONE"
#define ONCHIP_MEMORY_IRQ -1
#define ONCHIP_MEMORY_IRQ_INTERRUPT_CONTROLLER_ID -1
#define ONCHIP_MEMORY_NAME "/dev/onchip_memory"
#define ONCHIP_MEMORY_NON_DEFAULT_INIT_FILE_ENABLED 0
#define ONCHIP_MEMORY_RAM_BLOCK_TYPE "AUTO"
#define ONCHIP_MEMORY_READ_DURING_WRITE_MODE "DONT_CARE"
#define ONCHIP_MEMORY_SINGLE_CLOCK_OP 0
#define ONCHIP_MEMORY_SIZE_MULTIPLE 1
#define ONCHIP_MEMORY_SIZE_VALUE 131072
#define ONCHIP_MEMORY_SPAN 131072
#define ONCHIP_MEMORY_TYPE "altera_avalon_onchip_memory2"
#define ONCHIP_MEMORY_WRITABLE 1


/*
 * sysid_qsys configuration
 *
 */

#define ALT_MODULE_CLASS_sysid_qsys altera_avalon_sysid_qsys
#define SYSID_QSYS_BASE 0x410a0
#define SYSID_QSYS_ID -1145324613
#define SYSID_QSYS_IRQ -1
#define SYSID_QSYS_IRQ_INTERRUPT_CONTROLLER_ID -1
#define SYSID_QSYS_NAME "/dev/sysid_qsys"
#define SYSID_QSYS_SPAN 8
#define SYSID_QSYS_TIMESTAMP 1679412155
#define SYSID_QSYS_TYPE "altera_avalon_sysid_qsys"


/*
 * timer configuration
 *
 */

#define ALT_MODULE_CLASS_timer altera_avalon_timer
#define TIMER_ALWAYS_RUN 0
#define TIMER_BASE 0x41000
#define TIMER_COUNTER_SIZE 32
#define TIMER_FIXED_PERIOD 0
#define TIMER_FREQ 50000000
#define TIMER_IRQ 0
#define TIMER_IRQ_INTERRUPT_CONTROLLER_ID 0
#define TIMER_LOAD_VALUE 49999
#define TIMER_MULT 0.001
#define TIMER_NAME "/dev/timer"
#define TIMER_PERIOD 1
#define TIMER_PERIOD_UNITS "ms"
#define TIMER_RESET_OUTPUT 0
#define TIMER_SNAPSHOT 1
#define TIMER_SPAN 32
#define TIMER_TICKS_PER_SEC 1000
#define TIMER_TIMEOUT_PULSE_OUTPUT 0
#define TIMER_TYPE "altera_avalon_timer"

#endif /* __SYSTEM_H_ */
