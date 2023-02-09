#Update -period with clock period (in nanoseconds) of the clock driving the fpga
create_clock -name sopc_clk -period 20 [get_ports iCLK_50]

#Setting LED outputs as false path, since no timing requirement
set_false_path -from * -to [get_ports oLEDG[*]]

#Constraining JTAG interface
#TCK port
create_clock -name altera_reserved_tck -period 100 [get_ports altera_reserved_tck]
#cut all paths to and from tck
set_clock_groups -exclusive -group [get_clocks altera_reserved_tck]
#constrain the TDI port
set_input_delay -clock altera_reserved_tck 20 [get_ports altera_reserved_tdi]
#constrain the TMS port
set_input_delay -clock altera_reserved_tck 20 [get_ports altera_reserved_tms]
#constrain the TDO port
set_output_delay -clock altera_reserved_tck 20 [get_ports altera_reserved_tdo]