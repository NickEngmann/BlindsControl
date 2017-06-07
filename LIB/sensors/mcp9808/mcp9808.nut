/////////////////////////////////////////////////////////////////////////////
// Microchip MCP9808 temperature sensor class
//
// This work is released under the Creative Commons Zero (CC0) license.
// See http://creativecommons.org/publicdomain/zero/1.0/
/////////////////////////////////////////////////////////////////////////////
class MCP9808
{
    constructor(_i2c, _addr)
    {
        i2c = _i2c;
        addr = _addr; 
    }

    i2c = null;
    addr = 0;
}

/////////////////////////////////////////////////////////////////////////////
// Function:    readTemp
// Description: Read the ambient temperature from the sensor
// Arguments:   None
// Return:      Floating point temperature in Celsius
/////////////////////////////////////////////////////////////////////////////
function MCP9808::readTemp()
{
    i2c.address(addr);
    local data = i2c.read16(0x5) & 0x1fff;
    if (data & 0x1000)
        data -= 0x2000;

    return data / 16.0;
}

/////////////////////////////////////////////////////////////////////////////
// Function:    revision
// Description: Get the device revision number
// Arguments:   None
// Return:      Integer revision number
/////////////////////////////////////////////////////////////////////////////
function MCP9808::revision()
{
  	return i2c.read16(0x0);
}
