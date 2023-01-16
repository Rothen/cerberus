#pragma once

#define ASYNCDELAY_VERSION "1.1.2"

/*
 * A timer implementation for the Arduino which is safe from the
 * effects of rollover. See
 * http://arduino.cc/playground/Code/TimingRollover for details. This
 * class conveniently encapsulates that behaviour.
 */
#include "esphome.h"
// using namespace esphome;

class AsyncDelay {
public:
  enum units_t {
    MICROS,
    MILLIS,
  };

  // Have default delay to be zero so that timer is already expired.
  inline AsyncDelay(void) : delayTime(0), unit(MILLIS)
  {
    expires = millis() + delayTime;
  }
  
  inline AsyncDelay(unsigned long d, units_t u): delayTime(d), unit(u)
  {
    if (unit == MICROS)
      expires = micros() + delayTime;
    else
      expires = millis() + delayTime;
  }
  
  inline bool isExpired(void) const {
    if (unit == MICROS)
      return (long(micros() - expires) >= 0);
    else
      return (long(millis() - expires) >= 0);
  }

  inline bool isExpired(void) const volatile {
    if (unit == MICROS)
      return (long(micros() - expires) >= 0);
    else
      return (long(millis() - expires) >= 0);   
  }

  inline void start(unsigned long d, units_t u) {
    delayTime = d;
    unit = u;
    if (unit == MICROS)
      expires = micros() + delayTime;
    else
      expires = millis() + delayTime;
  }

  inline void start(unsigned long d, units_t u) volatile {
    delayTime = d;
    unit = u;
    if (unit == MICROS)
      expires = micros() + delayTime;
    else
      expires = millis() + delayTime;
  }

  // Restart the delay from when it expired (not now).
  inline void repeat(void) {
    expires += delayTime;
  }

  // Restart the delay from when it expired (not now).
  inline void repeat(void) volatile {
    expires += delayTime;
  }

  // Restart the delay from now.
  inline void restart(void) {
    if (unit == MICROS)
      expires = micros() + delayTime;
    else
      expires = millis() + delayTime;
  }

  // Restart the delay from now.
  inline void restart(void) volatile {
    if (unit == MICROS)
      expires = micros() + delayTime;
    else
      expires = millis() + delayTime;
  }

  // Force a delay to be expired.
  inline void expire(void) {
    if (unit == MICROS)
      expires = micros();
    else
      expires = millis();   
  }

  // Force a delay to be expired.
  inline void expire(void) volatile {
    if (unit == MICROS)
      expires = micros();
    else
      expires = millis();   
  }

  inline unsigned long getDelay(void) const {
    return delayTime;
  }

  inline unsigned long getDelay(void) const volatile {
    return delayTime;
  }

  inline void getDelay(unsigned long &d, units_t &u) const {
    d = delayTime;
    u = unit;
  }

  inline void getDelay(unsigned long &d, units_t &u) const volatile {
    d = delayTime;
    u = unit;
  }

  inline units_t getUnit(void) const {
    return unit;
  }

  inline units_t getUnit(void) const volatile {
    return unit;
  }

  inline unsigned long getExpiry(void) const {
    return expires;
  }

  inline unsigned long getExpiry(void) const volatile {
    return expires;
  }

  // Return how long has elapsed since the timer was started.
  inline unsigned long getDuration(void) const {
    if (unit == MICROS)
      return micros() - expires;
    else
      return millis() - expires;
  }

  inline unsigned long getDuration(void) const volatile {
    if (unit == MICROS)
      return micros() - expires;
    else
      return millis() - expires;
  }

private:
  unsigned long delayTime;
  unsigned long expires;
  units_t unit;
  
};
