library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity dut_tb is
    Port ( signal_in_tb_p : out  std_logic;
           clk_tb_p : out  std_logic;
           signal_out_tb_p : out  std_logic);
end dut_tb;
architecture Behavioral of dut_tb is
    component dut
        Generic ( param : integer);
        Port ( signal_in : in  std_logic;
               clk : in  std_logic;
               signal_out : out  std_logic);
    end component;
    signal signal_in_tb : std_logic := '0';
    signal clk_tb : std_logic := '0';
    signal signal_out_tb : std_logic := '0';
    constant param_tb : integer := 4;
begin
    dut_module: dut
            generic map(param => param_tb)
            port map(signal_in => signal_in_tb, signal_out => signal_out_tb, clk => clk_tb);
    clk_process : process
    begin
        clk_tb <= '1';
        wait for 5 ns;
        clk_tb <= '0';
        wait for 5 ns;
    end process;
    sim_process : process
    begin
        wait for 5 ns; -- offset everything to see rising edges clearly
        signal_in_tb <= '1'; -- expected output = 0
        wait for 20 ns;      -- expected output = 0
        signal_in_tb <= '0'; -- expected output = 0
        wait for 20 ns;      -- expected output = 0
        signal_in_tb <= '1'; -- expected output = 0
        wait for 60 ns;      -- expected output = 0, but = 1 after 40 ns
        signal_in_tb <= '0'; -- expected output = 1
        wait for 20 ns;      -- expected output = 1
        signal_in_tb <= '1'; -- expected output = 1
        wait for 60 ns;      -- expected output = 1
        signal_in_tb <= '0'; -- expected output = 1, but = 0 after 40 ns
        wait;
    end process;
    signal_in_tb_p <= signal_in_tb;
    signal_out_tb_p <= signal_out_tb;
    clk_tb_p <= clk_tb;
end Behavioral;
