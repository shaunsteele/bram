// tb_bram.sv

`default_nettype none

module tb_bram_top #(
  parameter int ALEN = 2,
  parameter int DLEN = 8
)(
  input var                     clk,
  input var                     rstn,

  input var                     wen,
  input var         [ALEN-1:0]  waddr,
  input var         [DLEN-1:0]  wdata,

  input var                     ren,
  input var         [ALEN-1:0]  raddr,
  output var logic  [DLEN-1:0]  rdata,
  output var logic              rvalid
);

// BRAM Interface
mem_if #(.ALEN(ALEN), .DLEN(DLEN)) mem(.clk(clk), .rstn(rstn));

// Connect Interface with Ports
assign mem.wen = wen;
assign mem.waddr = waddr;
assign mem.wdata = wdata;
assign mem.ren = ren;
assign mem.raddr = raddr;
assign rdata = mem.rdata;
assign rvalid = mem.rvalid;

// DUT
bram u_DUT(
  .clk  (clk),
  .rstn (rstn),
  .mem  (mem)
);

endmodule
