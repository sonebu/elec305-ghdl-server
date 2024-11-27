library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q3 is
  port (A: in std_logic; 
  			B: in std_logic;
				C: out std_logic);
end hw1_q3;

architecture rtl of hw1_q3 is
begin
  C <= A xor B;
end rtl;