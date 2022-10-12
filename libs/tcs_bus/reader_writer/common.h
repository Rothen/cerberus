#pragma once
#include <stdint.h>
#include <iostream>
#include <wiringPi.h>
#include <functional>
#define byte uint8_t

#define TCS_MSG_START_MS 6 // a new message
#define TCS_ONE_BIT_MS 4 // a 1-bit is 4ms long
#define TCS_ZERO_BIT_MS 2 // a 0-bit is 2ms long