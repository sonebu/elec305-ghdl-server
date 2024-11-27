library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q5 is
  port (A: in std_logic; 
  			clk: in std_logic;
				leds: out std_logic_vector(1 downto 0));
end hw1_q5;

architecture rtl of hw1_q5 is
	signal pulse : std_logic := '0';
begin
	toggle : process(clk)
	begin
		if rising_edge(clk) then
			pulse <= not pulse;
		end if;
	end process toggle;

	sel : process(A, pulse)
	begin
		if A = '0' then
			leds(0) <= pulse;
			leds(1) <= '0';
		else
			leds(0) <= '0';
			leds(1) <= pulse;
		end if;
	end process sel;
end rtl;