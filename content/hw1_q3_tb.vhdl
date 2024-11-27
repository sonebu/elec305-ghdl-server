library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q3_tb is
end hw1_q3_tb;

architecture behav of hw1_q3_tb is
  component hw1_q3
    port (A: in std_logic; 
          B: in std_logic; 
          C: out std_logic);
  end component;

  for hw1_q3_0: hw1_q3 use entity work.hw1_q3;
  signal A_tb, B_tb, C_tb : std_logic;
begin
  hw1_q3_0: hw1_q3 port map (A => A_tb, B => B_tb, C => C_tb);
  process
  begin
    assert false report "Running testbench" severity note;
    A_tb <= '0';
    B_tb <= '0';
    wait for 1 ns;
    assert C_tb = '0' report "A=0, B=0, C should have been =0, it was =1" severity error;
    A_tb <= '0';
    B_tb <= '1';
    wait for 1 ns;
    assert C_tb = '1' report "A=0, B=1, C should have been =1, it was =0" severity error;
    A_tb <= '1';
    B_tb <= '0';
    wait for 1 ns;
    assert C_tb = '1' report "A=1, B=0, C should have been =1, it was =0" severity error;
    A_tb <= '1';
    B_tb <= '1';
    wait for 1 ns;
    assert C_tb = '0' report "A=1, B=1, C should have been =0, it was =1" severity error;
    assert false report "End of testbench run" severity note;
    wait;
  end process;
end behav;
