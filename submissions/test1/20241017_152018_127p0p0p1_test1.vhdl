library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity lab0main is
    Port ( led : out  STD_LOGIC_VECTOR (15 downto 0);
           sw  : in   STD_LOGIC_VECTOR (15 downto 0);
           seg : out  STD_LOGIC_VECTOR (0 to 6);
           an  : out  STD_LOGIC_VECTOR (0 to 3)
           );
end lab0main;

architecture ahmetmehmet of lab0main is
-- constants etc.
begin
    seg(0 to 6) <= (others => '0');
    an(0 to 3)  <= '0011'; --(3 => '1', 2=> '0', 1=> '0', 0=> '1'); -- '0011';
    led(15 downto 0) <= not sw(15 downto 0);
end ahmetmehmet;
