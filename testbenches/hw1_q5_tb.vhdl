library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity hw1_q5_tb is
end hw1_q5_tb;

architecture behav of hw1_q5_tb is
  component hw1_q5
    port (A: in std_logic;
          clk: in std_logic; 
          leds: out std_logic_vector(1 downto 0));
  end component;

  for hw1_q5_0: hw1_q5 use entity work.hw1_q5;
  signal A_tb : std_logic := '0';
  signal clk_tb : std_logic := '0';
  signal leds_tb : std_logic_vector(1 downto 0);
  constant clock_period  : time := 10 ns;
begin
  hw1_q5_0: hw1_q5 port map (A => A_tb, clk => clk_tb, leds => leds_tb);

  clk_proc: process
  begin
    assert false report "Running testbench" severity note;
    for i in 0 to 5 loop
      clk_tb <= '0';
      wait for clock_period/2;
      clk_tb <= '1';
      wait for clock_period/2; 
    end loop;
    assert false report "End of testbench run" severity note;
    wait;  -- Wait indefinitely to end the process
  end process;

  state_proc: process
  begin
    A_tb <= '0';
    wait for 1 ns; -- shift waits by 1 ns to not sample exactly on clk rising edge but a bit later
    A_tb <= '0';
    wait for 5 ns; -- wait for first clock rising edge, leds(0) should turn on, i.e., leds = "01"
    assert leds_tb = "01" report "A=0, leds should have been =01 at first rising edge, but it was not" severity error;
    wait for 10 ns; -- wait for second clock rising edge so leds(0) can turn off, i.e., leds = "00"
    assert leds_tb = "00" report "A=0, leds should have been =00 at second rising edge, but it was not" severity error;
    A_tb <= '1';
    wait for 10 ns; -- wait for first clock rising edge, leds(1) should turn on, i.e., leds = "10"
    assert leds_tb = "10" report "A=1, leds should have been =10 at first rising edge, but it was not" severity error;
    wait for 10 ns; -- wait for second clock rising edge so leds(1) can turn off, i.e., leds = "00"
    assert leds_tb = "00" report "A=1, leds should have been =00 at second rising edge, but it was not" severity error;
    wait;
  end process;
  
end behav;
