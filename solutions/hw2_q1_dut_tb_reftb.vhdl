library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity reference_tb is
end reference_tb;
architecture Behavioral of reference_tb is
    component dut_tb
        Port ( signal_in_tb_p : out  std_logic;
               clk_tb_p : out  std_logic;
               signal_out_tb_p : out  std_logic);
    end component;
    signal signal_in_tb_p : std_logic := '0';
    signal clk_tb_p : std_logic := '0';
    signal signal_out_tb_p : std_logic := '0';
begin
    dut_tb_module: dut_tb
            port map(signal_in_tb_p => signal_in_tb_p, signal_out_tb_p => signal_out_tb_p, clk_tb_p => clk_tb_p);
    clk_process : process
    begin
        wait for 1 ns; -- 1ns shift to get settled values
        assert clk_tb_p = '1' report "Clock =0 when it should have been =1" severity error;
        wait for 5 ns;
        assert clk_tb_p = '0' report "Clock =1 when it should have been =0" severity error;
        wait for 4 ns;
    end process;
    sim_process : process
    begin
        assert false report "Running testbench" severity note; 
        wait for 6 ns; -- 1ns shift to get settled values
        assert signal_in_tb_p = '1'  report "expected input =1, got =0" severity error;
        assert signal_out_tb_p = '0' report "expected output =0, got =1" severity error;
        wait for 20 ns;
        assert signal_in_tb_p = '0'  report "expected input =0, got =1" severity error;
        assert signal_out_tb_p = '0' report "expected output =0, got =1" severity error;
        wait for 20 ns;
        assert signal_in_tb_p = '1'  report "expected input =1, got =0" severity error;
        assert signal_out_tb_p = '0' report "expected output =0, got =1" severity error;
        wait for 45 ns;
        assert signal_out_tb_p = '1' report "expected output =1, got =0" severity error;
        wait for 15 ns;
        assert signal_in_tb_p = '0' report "expected input =0, got =1" severity error;
        wait for 20 ns;
        assert signal_in_tb_p = '1'  report "expected input =1, got =0" severity error;
        assert signal_out_tb_p = '1' report "expected output =1, got =0" severity error;
        wait for 60 ns;
        assert signal_in_tb_p = '0'  report "expected input =0, got =1" severity error;
        assert signal_out_tb_p = '1' report "expected output =1, got =0" severity error;
        wait for 45 ns;
        assert signal_out_tb_p = '0' report "expected output =0, got =1" severity error;
        assert false report "Testbench completed" severity note; 
        wait;
    end process;
end Behavioral;
