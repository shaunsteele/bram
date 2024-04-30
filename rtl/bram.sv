// bram.sv

`default_nettype none

module bram(
  input var clk,
  input var rstn,
  mem_if.S  mem
);

// Parameter Declaration
localparam int ALEN = mem.ALEN;
localparam int DLEN = mem.DLEN;
localparam int Depth = 2 ** ALEN;

// RAM Array
logic [DLEN-1:0]  ram[Depth];

// Write Interface
always_ff @(posedge clk) begin
  if (mem.wen) begin
    ram[mem.waddr] <= mem.wdata;
  end else begin
    ram[mem.waddr] <= ram[mem.waddr];
  end
end

// Read Interface
always_ff @(posedge clk) begin
  if (!rstn) begin
    mem.rdata <= 0;
  end else begin
    if (mem.ren) begin
      mem.rdata <= ram[mem.raddr];
    end else begin
      mem.rdata <= mem.rdata;
    end
  end
end

endmodule
