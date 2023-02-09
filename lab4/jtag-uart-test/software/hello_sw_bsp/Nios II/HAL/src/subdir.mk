################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../HAL/src/alt_alarm_start.c \
../HAL/src/alt_busy_sleep.c \
../HAL/src/alt_close.c \
../HAL/src/alt_dcache_flush.c \
../HAL/src/alt_dcache_flush_all.c \
../HAL/src/alt_dcache_flush_no_writeback.c \
../HAL/src/alt_dev.c \
../HAL/src/alt_dev_llist_insert.c \
../HAL/src/alt_dma_rxchan_open.c \
../HAL/src/alt_dma_txchan_open.c \
../HAL/src/alt_do_ctors.c \
../HAL/src/alt_do_dtors.c \
../HAL/src/alt_ecc_fatal_exception.c \
../HAL/src/alt_env_lock.c \
../HAL/src/alt_environ.c \
../HAL/src/alt_errno.c \
../HAL/src/alt_execve.c \
../HAL/src/alt_exit.c \
../HAL/src/alt_fcntl.c \
../HAL/src/alt_fd_lock.c \
../HAL/src/alt_fd_unlock.c \
../HAL/src/alt_find_dev.c \
../HAL/src/alt_find_file.c \
../HAL/src/alt_flash_dev.c \
../HAL/src/alt_fork.c \
../HAL/src/alt_fs_reg.c \
../HAL/src/alt_fstat.c \
../HAL/src/alt_get_fd.c \
../HAL/src/alt_getchar.c \
../HAL/src/alt_getpid.c \
../HAL/src/alt_gettod.c \
../HAL/src/alt_gmon.c \
../HAL/src/alt_icache_flush.c \
../HAL/src/alt_icache_flush_all.c \
../HAL/src/alt_iic.c \
../HAL/src/alt_iic_isr_register.c \
../HAL/src/alt_instruction_exception_entry.c \
../HAL/src/alt_instruction_exception_register.c \
../HAL/src/alt_io_redirect.c \
../HAL/src/alt_ioctl.c \
../HAL/src/alt_irq_handler.c \
../HAL/src/alt_irq_register.c \
../HAL/src/alt_irq_vars.c \
../HAL/src/alt_isatty.c \
../HAL/src/alt_kill.c \
../HAL/src/alt_link.c \
../HAL/src/alt_load.c \
../HAL/src/alt_log_printf.c \
../HAL/src/alt_lseek.c \
../HAL/src/alt_main.c \
../HAL/src/alt_malloc_lock.c \
../HAL/src/alt_open.c \
../HAL/src/alt_printf.c \
../HAL/src/alt_putchar.c \
../HAL/src/alt_putcharbuf.c \
../HAL/src/alt_putstr.c \
../HAL/src/alt_read.c \
../HAL/src/alt_release_fd.c \
../HAL/src/alt_remap_cached.c \
../HAL/src/alt_remap_uncached.c \
../HAL/src/alt_rename.c \
../HAL/src/alt_sbrk.c \
../HAL/src/alt_settod.c \
../HAL/src/alt_stat.c \
../HAL/src/alt_tick.c \
../HAL/src/alt_times.c \
../HAL/src/alt_uncached_free.c \
../HAL/src/alt_uncached_malloc.c \
../HAL/src/alt_unlink.c \
../HAL/src/alt_usleep.c \
../HAL/src/alt_wait.c \
../HAL/src/alt_write.c \
../HAL/src/altera_nios2_gen2_irq.c 

S_UPPER_SRCS += \
../HAL/src/alt_ecc_fatal_entry.S \
../HAL/src/alt_exception_entry.S \
../HAL/src/alt_exception_muldiv.S \
../HAL/src/alt_exception_trap.S \
../HAL/src/alt_irq_entry.S \
../HAL/src/alt_log_macro.S \
../HAL/src/alt_mcount.S \
../HAL/src/alt_software_exception.S \
../HAL/src/crt0.S 

OBJS += \
./HAL/src/alt_alarm_start.o \
./HAL/src/alt_busy_sleep.o \
./HAL/src/alt_close.o \
./HAL/src/alt_dcache_flush.o \
./HAL/src/alt_dcache_flush_all.o \
./HAL/src/alt_dcache_flush_no_writeback.o \
./HAL/src/alt_dev.o \
./HAL/src/alt_dev_llist_insert.o \
./HAL/src/alt_dma_rxchan_open.o \
./HAL/src/alt_dma_txchan_open.o \
./HAL/src/alt_do_ctors.o \
./HAL/src/alt_do_dtors.o \
./HAL/src/alt_ecc_fatal_entry.o \
./HAL/src/alt_ecc_fatal_exception.o \
./HAL/src/alt_env_lock.o \
./HAL/src/alt_environ.o \
./HAL/src/alt_errno.o \
./HAL/src/alt_exception_entry.o \
./HAL/src/alt_exception_muldiv.o \
./HAL/src/alt_exception_trap.o \
./HAL/src/alt_execve.o \
./HAL/src/alt_exit.o \
./HAL/src/alt_fcntl.o \
./HAL/src/alt_fd_lock.o \
./HAL/src/alt_fd_unlock.o \
./HAL/src/alt_find_dev.o \
./HAL/src/alt_find_file.o \
./HAL/src/alt_flash_dev.o \
./HAL/src/alt_fork.o \
./HAL/src/alt_fs_reg.o \
./HAL/src/alt_fstat.o \
./HAL/src/alt_get_fd.o \
./HAL/src/alt_getchar.o \
./HAL/src/alt_getpid.o \
./HAL/src/alt_gettod.o \
./HAL/src/alt_gmon.o \
./HAL/src/alt_icache_flush.o \
./HAL/src/alt_icache_flush_all.o \
./HAL/src/alt_iic.o \
./HAL/src/alt_iic_isr_register.o \
./HAL/src/alt_instruction_exception_entry.o \
./HAL/src/alt_instruction_exception_register.o \
./HAL/src/alt_io_redirect.o \
./HAL/src/alt_ioctl.o \
./HAL/src/alt_irq_entry.o \
./HAL/src/alt_irq_handler.o \
./HAL/src/alt_irq_register.o \
./HAL/src/alt_irq_vars.o \
./HAL/src/alt_isatty.o \
./HAL/src/alt_kill.o \
./HAL/src/alt_link.o \
./HAL/src/alt_load.o \
./HAL/src/alt_log_macro.o \
./HAL/src/alt_log_printf.o \
./HAL/src/alt_lseek.o \
./HAL/src/alt_main.o \
./HAL/src/alt_malloc_lock.o \
./HAL/src/alt_mcount.o \
./HAL/src/alt_open.o \
./HAL/src/alt_printf.o \
./HAL/src/alt_putchar.o \
./HAL/src/alt_putcharbuf.o \
./HAL/src/alt_putstr.o \
./HAL/src/alt_read.o \
./HAL/src/alt_release_fd.o \
./HAL/src/alt_remap_cached.o \
./HAL/src/alt_remap_uncached.o \
./HAL/src/alt_rename.o \
./HAL/src/alt_sbrk.o \
./HAL/src/alt_settod.o \
./HAL/src/alt_software_exception.o \
./HAL/src/alt_stat.o \
./HAL/src/alt_tick.o \
./HAL/src/alt_times.o \
./HAL/src/alt_uncached_free.o \
./HAL/src/alt_uncached_malloc.o \
./HAL/src/alt_unlink.o \
./HAL/src/alt_usleep.o \
./HAL/src/alt_wait.o \
./HAL/src/alt_write.o \
./HAL/src/altera_nios2_gen2_irq.o \
./HAL/src/crt0.o 

C_DEPS += \
./HAL/src/alt_alarm_start.d \
./HAL/src/alt_busy_sleep.d \
./HAL/src/alt_close.d \
./HAL/src/alt_dcache_flush.d \
./HAL/src/alt_dcache_flush_all.d \
./HAL/src/alt_dcache_flush_no_writeback.d \
./HAL/src/alt_dev.d \
./HAL/src/alt_dev_llist_insert.d \
./HAL/src/alt_dma_rxchan_open.d \
./HAL/src/alt_dma_txchan_open.d \
./HAL/src/alt_do_ctors.d \
./HAL/src/alt_do_dtors.d \
./HAL/src/alt_ecc_fatal_exception.d \
./HAL/src/alt_env_lock.d \
./HAL/src/alt_environ.d \
./HAL/src/alt_errno.d \
./HAL/src/alt_execve.d \
./HAL/src/alt_exit.d \
./HAL/src/alt_fcntl.d \
./HAL/src/alt_fd_lock.d \
./HAL/src/alt_fd_unlock.d \
./HAL/src/alt_find_dev.d \
./HAL/src/alt_find_file.d \
./HAL/src/alt_flash_dev.d \
./HAL/src/alt_fork.d \
./HAL/src/alt_fs_reg.d \
./HAL/src/alt_fstat.d \
./HAL/src/alt_get_fd.d \
./HAL/src/alt_getchar.d \
./HAL/src/alt_getpid.d \
./HAL/src/alt_gettod.d \
./HAL/src/alt_gmon.d \
./HAL/src/alt_icache_flush.d \
./HAL/src/alt_icache_flush_all.d \
./HAL/src/alt_iic.d \
./HAL/src/alt_iic_isr_register.d \
./HAL/src/alt_instruction_exception_entry.d \
./HAL/src/alt_instruction_exception_register.d \
./HAL/src/alt_io_redirect.d \
./HAL/src/alt_ioctl.d \
./HAL/src/alt_irq_handler.d \
./HAL/src/alt_irq_register.d \
./HAL/src/alt_irq_vars.d \
./HAL/src/alt_isatty.d \
./HAL/src/alt_kill.d \
./HAL/src/alt_link.d \
./HAL/src/alt_load.d \
./HAL/src/alt_log_printf.d \
./HAL/src/alt_lseek.d \
./HAL/src/alt_main.d \
./HAL/src/alt_malloc_lock.d \
./HAL/src/alt_open.d \
./HAL/src/alt_printf.d \
./HAL/src/alt_putchar.d \
./HAL/src/alt_putcharbuf.d \
./HAL/src/alt_putstr.d \
./HAL/src/alt_read.d \
./HAL/src/alt_release_fd.d \
./HAL/src/alt_remap_cached.d \
./HAL/src/alt_remap_uncached.d \
./HAL/src/alt_rename.d \
./HAL/src/alt_sbrk.d \
./HAL/src/alt_settod.d \
./HAL/src/alt_stat.d \
./HAL/src/alt_tick.d \
./HAL/src/alt_times.d \
./HAL/src/alt_uncached_free.d \
./HAL/src/alt_uncached_malloc.d \
./HAL/src/alt_unlink.d \
./HAL/src/alt_usleep.d \
./HAL/src/alt_wait.d \
./HAL/src/alt_write.d \
./HAL/src/altera_nios2_gen2_irq.d 


# Each subdirectory must supply rules for building sources it contributes
HAL/src/%.o: ../HAL/src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Nios II GCC C Compiler'
	nios2-elf-gcc -O2 -g -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

HAL/src/%.o: ../HAL/src/%.S
	@echo 'Building file: $<'
	@echo 'Invoking: Nios II GCC Assembler'
	nios2-elf-as  -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


