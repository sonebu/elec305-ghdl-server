library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity hw2_q2_dut_tb is
end hw2_q2_dut_tb;
architecture Behavioral of hw2_q2_dut_tb is
    component dut
        Generic ( param : integer);
        Port ( signal_in : in  std_logic;
               enable : in std_logic; 
               clk : in  std_logic;
               signal_out : out  std_logic);
    end component;
    signal signal_in_tb : std_logic := '0';
    signal enable_tb : std_logic := '0';
    signal clk_tb : std_logic := '0';
    signal signal_out_tb : std_logic := '0';
    constant param_tb : integer := 4;
begin
    dut_module: dut
            generic map(param => param_tb)
            port map(signal_in => signal_in_tb, signal_out => signal_out_tb, clk => clk_tb, enable => enable_tb);
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
        enable_tb <= '0';
        signal_in_tb <= '0';
        wait for 10 ns; -- 15ns
        assert signal_in_tb = signal_out_tb report "Should have gotten signal_in_tb = signal_out_tb by now, but it didn't happen" severity error;
        wait for 40 ns; -- 55ns
        signal_in_tb <= '1';
        wait for 10 ns; -- 65ns
        assert signal_in_tb = signal_out_tb report "Should have gotten signal_in_tb = signal_out_tb by now, but it didn't happen" severity error;
        wait for 40 ns; -- 105ns
        signal_in_tb <= '0';
        wait for 10 ns; -- 115ns
        assert signal_in_tb = signal_out_tb report "Should have gotten signal_in_tb = signal_out_tb by now, but it didn't happen" severity error;
        wait for 40 ns; -- 155ns
        enable_tb <= '1';
        signal_in_tb <= '1'; 
        wait for 10 ns; -- 165ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0 by now, but it didn't happen" severity error;
        signal_in_tb <= '0'; 
        wait for 10 ns; -- 175ns 
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0 by now, but it didn't happen" severity error;
        signal_in_tb <= '1';
        wait for 55 ns; -- 230ns
        assert signal_out_tb = '1' report "Should have gotten signal_out_tb = 1 by now, but it didn't happen" severity error;
        wait for 5 ns; -- 235ns
        signal_in_tb <= '0';
        wait for 55 ns; -- 290ns
        assert signal_out_tb = '0' report "Should have gotten signal_out_tb = 0 by now, but it didn't happen" severity error;
        wait for 5 ns; -- 295ns
        wait;
    end process;
end Behavioral;
