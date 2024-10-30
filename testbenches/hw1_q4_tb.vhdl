library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q4_tb is
end hw1_q4_tb;

architecture behav of hw1_q4_tb is
  component hw1_q4
    port (A: in std_logic_vector(1 downto 0); 
          B: out std_logic_vector(2 downto 0));
  end component;

  for hw1_q4_0: hw1_q4 use entity work.hw1_q4;
  signal A_tb : std_logic_vector(1 downto 0);
  signal B_tb : std_logic_vector(2 downto 0);
begin
  hw1_q4_0: hw1_q4 port map (A => A_tb, B => B_tb);
  process
  begin
    assert false report "Running testbench" severity note;
    A_tb <= "00";
    wait for 1 ns;
    assert B_tb = "000" report "A=00, B should have been =000, it was not" severity error;
    A_tb <= "01";
    wait for 1 ns;
    assert B_tb = "110" report "A=01, B should have been =110 (note: downto, not to), it was not" severity error;
    A_tb <= "10";
    wait for 1 ns;
    assert B_tb = "110" report "A=10, B should have been =110 (note: downto, not to), it was not" severity error;
    A_tb <= "11";
    wait for 1 ns;
    assert B_tb = "011" report "A=11, B should have been =011 (note: downto, not to), it was not" severity error;
    assert false report "End of testbench run" severity note;
    wait;
  end process;
end behav;
