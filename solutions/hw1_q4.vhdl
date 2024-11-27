library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q4 is
  port (A: in std_logic_vector(1 downto 0); 
  			B: out std_logic_vector(2 downto 0));
end hw1_q4;

architecture rtl of hw1_q4 is
begin
  B(0) <= A(0) and A(1);
  B(1) <= A(0) or A(1);
  B(2) <= A(0) xor A(1);
end rtl;