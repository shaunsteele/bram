# tb_bram.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge
import os


async def single_write(dut, addr, data):
  await FallingEdge(dut.clk)
  dut.waddr.value = addr
  dut.wdata.value = data
  dut.wen.value = 1

  await FallingEdge(dut.clk)
  dut.wen.value = 0


async def single_read(dut, addr):
  await FallingEdge(dut.clk)
  dut.raddr.value = addr
  dut.ren.value = 1

  await FallingEdge(dut.clk)
  dut.ren.value = 0
  assert dut.rvalid.value
  return dut.rdata.value


async def linear_write(dut, ba, data):
  for a, d in enumerate(data):
    await FallingEdge(dut.clk)
    dut.waddr.value = ba + a
    dut.wdata.value = d
    dut.wen.value = 1

  await FallingEdge(dut.clk)
  dut.wen.value = 0


async def linear_read(dut, ba, size):
  data = []
  for a in range(size):
    await FallingEdge(dut.clk)
    dut.raddr.value = ba + a
    dut.ren.value = 1

    if (a):
      assert dut.rvalid.value
      data.append(dut.rdata.value)

  await FallingEdge(dut.clk)
  assert dut.rvalid.value
  data.append(dut.rdata.value)
  dut.ren.value = 0
  return data


@cocotb.test()
async def tb_bram(dut):
  cocotb.log.info(f"Starting {tb_bram.__name__}")
  cocotb.log.info("Parameters:")
  cocotb.log.info(f"\tALEN: {dut.ALEN.value}")
  cocotb.log.info(f"\tDLEN: {dut.DLEN.value}")

  # Start Clock
  dut.clk.value = 0
  cocotb.start_soon(Clock(dut.clk, 10, "ns").start())

  # Initial Values
  dut.rstn.value = 0
  dut.wen.value = 0
  dut.waddr.value = 0
  dut.wdata.value = 0
  dut.ren.value = 0
  dut.raddr.value = 0

  # Complete Reset
  await ClockCycles(dut.clk, 10)
  dut.rstn.value = 1

  # Tests:
  # - Write then read
  await RisingEdge(dut.clk)
  cocotb.log.info("Write then Read test")
  data = os.urandom(1)

  await single_write(dut, 0, data[0])
  test = await single_read(dut, 0)
  assert list(data)[0] == test
  cocotb.log.info("Passed")

  # - Linear write to all spaces with linear read check
  await RisingEdge(dut.clk)
  cocotb.log.info("Linear write then read test")
  data = os.urandom(2 ** dut.ALEN.value)
  await linear_write(dut, 0, data)
  test = await linear_read(dut, 0, 2 ** dut.ALEN.value)
  assert list(data) == test
  cocotb.log.info("Passed")

  await ClockCycles(dut.clk, 10)
