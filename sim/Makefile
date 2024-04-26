# CocoTB Makefile

REPO_DIR := /home/shaun/repos/bram

IF_DIR	:= $(REPO_DIR)/interfaces
RTL_DIR := $(REPO_DIR)/rtl
SIM_DIR := $(REPO_DIR)/sim

SIM ?= verilator

# EXTRA_ARGS += --timing
EXTRA_ARGS += --coverage
EXTRA_ARGS += --trace --trace-structs


TOPLEVELLANG ?= verilog

VERILOG_SOURCES += $(IF_DIR)/mem_if.sv
VERILOG_SOURCES += $(RTL_DIR)/bram.sv
VERILOG_SOURCES += $(SIM_DIR)/tb_bram_top.sv

TOPLEVEL = tb_bram_top

MODULE = tb_bram

include $(shell cocotb-config --makefiles)/Makefile.sim

WAVES = dump.vcd

.PHONY: waves
waves:
	gtkwave $(WAVES)

# .PHONY: clean
# clean:
# 	rm -rf __pycache__/
