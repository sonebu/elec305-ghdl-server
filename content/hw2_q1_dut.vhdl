library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity dut is
	Generic ( param : integer range 0 to 63 := 5);
	Port (	signal_in : in  std_logic;
		clk : in std_logic;
		signal_out : out  std_logic);
end dut;
architecture Behavioral of dut is
	signal ctr : integer range 0 to 63 := 0;
	signal out_reg : std_logic := '0';
	constant maxctr : integer range 0 to 63 := param;
begin
	debounce_process : process (clk)
	begin
	if (rising_edge(clk)) then
		if (ctr = maxctr) then
			out_reg <= not(out_reg);
		end if;
	end if;
	end process;
	counter_process : process (clk)
	begin
	if (rising_edge(clk)) then
		if ((out_reg = '1') xor (signal_in = '1')) then
			if (ctr = maxctr) then
				ctr <= 0;
			else
				ctr <= ctr + 1;
			end if;
		else
			ctr <= 0;
		end if;
	end if;
	end process;
	signal_out <= out_reg;
end Behavioral;

