library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q2_tb is
end hw1_q2_tb;

architecture behav of hw1_q2_tb is
  component hw1_q2
    port (A: in std_logic; 
          B: out std_logic);
  end component;

  for hw1_q2_0: hw1_q2 use entity work.hw1_q2;
  signal A_tb, B_tb : std_logic;
begin
  hw1_q2_0: hw1_q2 port map (A => A_tb, B => B_tb);
  process
  begin
    assert false report "Running testbench" severity note;
    A_tb <= '0';
    wait for 1 ns;
    assert B_tb = '1' report "A was driven to 0, B should have been driven to 1, B did not get driven to 1" severity error;
    A_tb <= '1';
    wait for 1 ns;
    assert B_tb = '0' report "A was driven to 1, B should have been driven to 0, B did not get driven to 0" severity error;    
    wait for 1 ns;
    assert false report "End of testbench run" severity note;
    wait;
  end process;
end behav;
