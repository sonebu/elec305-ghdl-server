library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity hw2_q3_dut_tb is
end hw2_q3_dut_tb;
architecture Behavioral of hw2_q3_dut_tb is
    component dut
        Generic ( param_up : integer;
                  param_down : integer);
        Port ( signal_in : in  std_logic;
               clk : in  std_logic;
               signal_out : out  std_logic);
    end component;
    signal signal_in_tb : std_logic := '0';
    signal clk_tb : std_logic := '0';
    signal signal_out_tb : std_logic := '0';
    constant param_up_tb : integer := 2;
    constant param_down_tb : integer := 4;
begin
    dut_module: dut
            generic map(param_up => param_up_tb, param_down => param_down_tb)
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
        assert false report "Running testbench" severity note;
    
        wait for 5 ns; -- offset everything to see rising edges clearly
        signal_in_tb <= '0';
        wait for 10 ns; -- 15ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0, but it didn't happen" severity error;
        signal_in_tb <= '1'; 
        wait for 10 ns; -- 25ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0, but it didn't happen" severity error;
        signal_in_tb <= '0'; 
        wait for 10 ns; -- 35ns 
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0, but it didn't happen" severity error;
        signal_in_tb <= '1';
        wait for 10 ns; -- 45ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0, but it didn't happen" severity error;
        wait for 20 ns; -- 65ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1, but it didn't happen" severity error;
        wait for 10 ns; -- 75ns
        signal_in_tb <= '0';
        wait for 10 ns; -- 125ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1, but it didn't happen" severity error;
        wait for 10 ns; -- 125ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1, but it didn't happen" severity error;
        wait for 10 ns; -- 125ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1, but it didn't happen" severity error;
        wait for 10 ns; -- 125ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1, but it didn't happen" severity error;
        wait for 10 ns; -- 125ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0, but it didn't happen" severity error;
        wait for 5 ns;  -- 130ns
        wait;
    end process;
end Behavioral;
