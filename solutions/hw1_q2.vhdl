library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q2 is
  port (A: in std_logic; 
  		B: out std_logic);
end hw1_q2;

architecture rtl of hw1_q2 is
begin
  B <= not A;
end rtl;