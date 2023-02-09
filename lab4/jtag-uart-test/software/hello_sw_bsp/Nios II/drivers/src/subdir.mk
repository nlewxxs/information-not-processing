################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../drivers/src/altera_avalon_jtag_uart_fd.c \
../drivers/src/altera_avalon_jtag_uart_init.c \
../drivers/src/altera_avalon_jtag_uart_ioctl.c \
../drivers/src/altera_avalon_jtag_uart_read.c \
../drivers/src/altera_avalon_jtag_uart_write.c \
../drivers/src/altera_avalon_sysid_qsys.c \
../drivers/src/altera_avalon_timer_sc.c \
../drivers/src/altera_avalon_timer_ts.c \
../drivers/src/altera_avalon_timer_vars.c \
../drivers/src/altera_up_avalon_accelerometer_spi.c 

OBJS += \
./drivers/src/altera_avalon_jtag_uart_fd.o \
./drivers/src/altera_avalon_jtag_uart_init.o \
./drivers/src/altera_avalon_jtag_uart_ioctl.o \
./drivers/src/altera_avalon_jtag_uart_read.o \
./drivers/src/altera_avalon_jtag_uart_write.o \
./drivers/src/altera_avalon_sysid_qsys.o \
./drivers/src/altera_avalon_timer_sc.o \
./drivers/src/altera_avalon_timer_ts.o \
./drivers/src/altera_avalon_timer_vars.o \
./drivers/src/altera_up_avalon_accelerometer_spi.o 

C_DEPS += \
./drivers/src/altera_avalon_jtag_uart_fd.d \
./drivers/src/altera_avalon_jtag_uart_init.d \
./drivers/src/altera_avalon_jtag_uart_ioctl.d \
./drivers/src/altera_avalon_jtag_uart_read.d \
./drivers/src/altera_avalon_jtag_uart_write.d \
./drivers/src/altera_avalon_sysid_qsys.d \
./drivers/src/altera_avalon_timer_sc.d \
./drivers/src/altera_avalon_timer_ts.d \
./drivers/src/altera_avalon_timer_vars.d \
./drivers/src/altera_up_avalon_accelerometer_spi.d 


# Each subdirectory must supply rules for building sources it contributes
drivers/src/%.o: ../drivers/src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Nios II GCC C Compiler'
	nios2-elf-gcc -O2 -g -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


