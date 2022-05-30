#include "common.h"

class TCSBusReader
{
public:
    /**
     * @brief A reader class to read messages from TCS bus systems.
     *
     * @param readPin the pin that is connected to the data line of the TCS bus.
     */
    TCSBusReader(uint8_t readPin);

    /**
     * @brief Must be called once during setup() phase
     */
    void begin();

    /**
     * @brief Enables the reading of the bus via interrupts.
     *
     */
    void enable();

    /**
     * @brief Disables the reading of the bus via interrupts
     *
     */
    void disable();

    /**
     * @brief Returns true if a new command has been received from the bus.
     *
     * @return true if a new command has been received.
     * @return false if no command is available.
     */
    bool hasCommand();

    /**
     * @brief Reads the last message from the bus and also resets the #hasCommand() flag.
     *
     * @param cmd the pointer where to write the cmd to.
     * @param curCrc the pointer where to write the curCrc to.
     * @param calcCrc the pointer where to write the calcCrc to.
     * @param cmdLength the pointer where to write the length of the command to.
     */
    void read(uint32_t *cmd, uint8_t *curCrc, uint8_t *calcCrc, uint8_t *cmdLength);

private:
    /**
     * @brief The interrupt method that counts the time for each high
     * or low bit and connects it to one big command.
     */
    static void analyzeCMD();

    static volatile uint32_t s_cmd;
    static volatile uint8_t s_crc;
    static volatile uint8_t s_calcCrc;
    static volatile uint8_t s_cmdLength;
    static volatile bool s_cmdReady;
    uint8_t m_readPin;
    bool m_enabled;
};