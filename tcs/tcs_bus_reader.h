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
     * @return uint32_t the last command from the bus
     */
    uint32_t read();

    /**
     * @brief Injects a command into the reader that can be read from it directly
     * without being read from the bus.
     *
     * @param cmd the command to inject
     */
    void inject(uint32_t cmd);

private:
    /**
     * @brief The interrupt method that counts the time for each high
     * or low bit and connects it to one big command.
     */
    static void analyzeCMD();

    static volatile uint32_t s_cmd;
    static volatile uint8_t s_cmdLength;
    static volatile bool s_cmdReady;
    uint8_t m_readPin;
    bool m_enabled;
};