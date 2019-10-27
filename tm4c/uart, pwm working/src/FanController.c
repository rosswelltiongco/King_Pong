
#include <assert.h>
#include "FanController.h"
#include "HAL.h"
#include "Display.h"
//#include "Thermistor.h"
//#include "TemperatureSettings.h"
#include "Console.h"


// At 80MHz, this is the number of bus cycles for a 25kHz PWM frequency.
#define PWM_PERIOD		3200

// The number of times an ADC channel should be read before using the value.
#define MAX_ADC_SAMPLES 	150

// Pointers to the IO configuration and temperature settings, 
//	used by multiple functions.
static FanController_IOConfig_t* pIOConfig_;
static TemperatureSettings_t controlSettings_;

// Holds the bit-band alias address of the display switches.
static volatile uint32_t* pTempDisplaySwitch_;
static volatile uint32_t* pTachDisplaySwitch_;

// Holds the bit-band alias address of the fan mode switches.
static volatile uint32_t* pManualModeSwitch_;
static volatile uint32_t* pAutoModeSwitch_;

// Holds the bit-band address of the fan relay.
static volatile uint32_t* pFanRelay_;

// Holds the bit-band address of the heartbead LED.
static volatile uint32_t* pHeartbeatLED_;

// Holds the current RPM value.
static uint32_t tachRPM_;
		
float percentage = 0.0;
		
// Names for the fan modes.
typedef enum {
		ROW1,
		ROW2,
		ROW3,
		ROW4,
		OFF
} FanMode_t;

// Names for the display modes.
typedef enum {
		DISPLAYMODE_TACH,
		DISPLAYMODE_SPEED
} DisplayMode_t;


// Catch-all error handler.
void ErrHandler(void) 
{
		// Spin...
		while (1);
}
	
	
// This function is called back an interval timer every second.  It's purpose
//	is to read the input edge counter and calculated the RPM of the fan.
//	It also toggles the "heartbeat" LED.
static void RpmTimerCallback(void)
{

	// Read the accumulated pulse count.
	uint32_t tachPulseCount = Timer_ReadCounterValue(pIOConfig_->tachCounter);

	// The Tachometer outputs 2 pulses per revolution.  So, divide by 2 to get
	//	revolutions per seconds, then multiply by 60 secs. to approximate RPM.
	tachRPM_ = (tachPulseCount / 2) * 60;
	
	// Reset the timer to zero and start over.
	Timer_ResetInputCounter(pIOConfig_->tachCounter);
	
	// Toggle the red onboard LED.
	*pHeartbeatLED_ = !(*pHeartbeatLED_);
	
}

// This function takes the IOConfig structure and initialize all hardware
//	and service modules used by this FanController.
static int InitHardware(FanController_IOConfig_t* pIOConfig)
{
	// If the pConfig pointer wasn't set by the caller, then abort.
	if (!pIOConfig) {
		return -1;
	}
	
	// Disable interrupts globally while configuring the hardware.
	__disable_irq();
	
	// Enable the PLL for 80MHz.
	PLL_Init80MHz();

	// Enable digital Inputs
	GPIO_EnableDI(pIOConfig->tempDisplaySwitch.port, pIOConfig->tempDisplaySwitch.pin, PULL_UP);
	GPIO_EnableDI(pIOConfig->tachDisplaySwitch.port, pIOConfig->tachDisplaySwitch.pin, PULL_UP);
	GPIO_EnableDI(pIOConfig->manualModeSwitch.port, pIOConfig->manualModeSwitch.pin, PULL_UP);
	GPIO_EnableDI(pIOConfig->tempModeSwitch.port, pIOConfig->tempModeSwitch.pin, PULL_UP);

	// Enable digital Outputs
	GPIO_EnableDO(pIOConfig->heartBeatLED.port, pIOConfig->heartBeatLED.pin, DRIVE_2MA, PULL_DOWN);
	GPIO_EnableDO(pIOConfig->fanRelay.port, pIOConfig->fanRelay.pin, DRIVE_2MA, PULL_DOWN);

	// Enable ADC Speed Pot
	ADC_Enable(pIOConfig->speedPot.module, pIOConfig->speedPot.channel);
	
	
	// Enable the PWM output. The PWM period is calculated to be the number of ticks required
	//	to achieve a frequency of 25kHz, which is the nominal frequency for the fan.
	PWM_Enable(pIOConfig->pwm.module, pIOConfig->pwm.channel, PWM_PERIOD, PWM_PERIOD / 2);
	
	// Enable the RPM timer.  At 80MHz, there are 80 million system ticks in one second.
	//	Second highest interrupt priority.  The Display will take the highest.
	Timer_EnableTimerPeriodic(pIOConfig->rpmTimer, 80000000, 2, RpmTimerCallback);
	
	// Enable and reset the tach pulse input counter.
	Timer_EnableInputCounter(pIOConfig->tachCounter);
	Timer_ResetInputCounter(pIOConfig->tachCounter);
	
	// Initialize the free-running timer.
	SysTick_Init();
	
	// Enable the Flash module.
	Flash_Enable();
	
	// Initialize the display module.
	Display_Initialize(pIOConfig->displaySSI, pIOConfig->displayTimer);
	
	// Initialize the console.
	Console_Init(pIOConfig->uart);
	
	// Store the bit-band addresses for the digital IO.
	pTempDisplaySwitch_ = GPIO_GetBitBandIOAddress(pIOConfig->tempDisplaySwitch);
	pTachDisplaySwitch_ = GPIO_GetBitBandIOAddress(pIOConfig->tachDisplaySwitch);	
	pManualModeSwitch_ = GPIO_GetBitBandIOAddress(pIOConfig->manualModeSwitch);
	pAutoModeSwitch_ = GPIO_GetBitBandIOAddress(pIOConfig->tempModeSwitch);	
	pFanRelay_ = GPIO_GetBitBandIOAddress(pIOConfig->fanRelay);	
	pHeartbeatLED_ = GPIO_GetBitBandIOAddress(pIOConfig->heartBeatLED);
		
	// Enable interrupts globally.
	__enable_irq();
	
	return 0;
}


// Reads and returns the ADC value associated with the manual speed potentiometer.
static int ReadSpeedPot(void)
{
	int adcSpeed = 0;
	
	for (int j = 0; j < MAX_ADC_SAMPLES; j++) {
		adcSpeed += ADC_Sample(pIOConfig_->speedPot.module);		
	}
	
	// Trim off LSBs and scale into range to get a more stable value.	
	adcSpeed /= MAX_ADC_SAMPLES;
	adcSpeed  &= 0xFFFFFFF0;
	adcSpeed  = (float)adcSpeed * 1.00368f;
	
	return adcSpeed;
}


// Checks the state of the fan mode switches and returns the mode.
static FanMode_t GetFanMode(int row)
{
	if (row == 1) {
		return ROW1;
	}
	else if (row == 2) {
		return ROW2;
	}
	else if (row == 3) {
			return ROW3;
	}
	else if (row == 4) {
			return ROW4;
	}
	
	return OFF;
	
}

// Checks the state of the display mode switches and returns the mode.
static DisplayMode_t GetDisplayMode(void)
{
	// Get the display based on the display mode switches.
	if (!(*pTachDisplaySwitch_)) {
		return DISPLAYMODE_TACH;
	}	

	return DISPLAYMODE_SPEED;
}

// Turns on or off the fan and sets the PWM duty cycle.  The on/off state
//	and speed is determined by the mode of the fan which also depends on the
//	speed pot and temperature.


static int SetFanSpeed(int rowNum)
{
    switch(rowNum)
    {
        case 1: percentage = 40; break;
        case 2: percentage = 43; break;
        case 3: percentage = 46; break;
        case 4: percentage = 49; break;
    }
    
    if (percentage <= 0.0f)
    {
        
        // Turn the fan OFF.
        *pFanRelay_ = 0;
    
    }
    
    else
    {
                
        // Don't allow the duty cycle to go to 100% or the fan speed drops,
        //    apparently unable to find an input pulse.
        if (percentage >= 1.0f) {
            percentage = 0.999f;
        }
    
        // Apply the percentage to the PWM period to obtain the duty cycle.
        uint32_t duty = (uint32_t)(percentage * (float)PWM_PERIOD);

        // Set the duty cycle
        PWM_SetDuty(pIOConfig_->pwm.module, pIOConfig_->pwm.channel, duty);
    
        // Turn the fan ON.
        *pFanRelay_ = 1;
    
    }
        
    // Return an integer speed value between 0-100.
    return (int)((percentage * 100.0f) + 0.5f);
}


static int ManualFanSpeed(int speedPot)
{
    // Convert the ADC sample to a percentage of its maximum range.
    //     Map the percentage into 1-100%.
    percentage  = 0.01f + (speedPot / 4096.0f);

    if (percentage <= 0.0f) {
        
        // Turn the fan OFF.
        *pFanRelay_ = 0;
    
    }
    else {
                
        // Don't allow the duty cycle to go to 100% or the fan speed drops,
        //    apparently unable to find an input pulse.
        if (percentage >= 1.0f) {
            percentage = 0.999f;
        }
    
        // Apply the percentage to the PWM period to obtain the duty cycle.
        uint32_t duty = (uint32_t)(percentage * (float)PWM_PERIOD);

        // Set the duty cycle
        PWM_SetDuty(pIOConfig_->pwm.module, pIOConfig_->pwm.channel, duty);
    
        // Turn the fan ON.
        *pFanRelay_ = 1;
    
    }
        
    // Return an integer speed value between 0-100.
    return (int)((percentage * 100.0f) + 0.5f);
}


static int RunFanSpeed(void)
{
	int desiredRPM [4] = {2000, 2100, 2500, 3000};
	// percentage is equivalent to the duty cycle.
	float percentage = 0;
	
	int UART_row = 1;
	// Get the fan mode from the mode switches.
  SetFanSpeed(UART_row);
	FanMode_t mode = GetFanMode(UART_row);

	
	switch (mode) {
	
		case ROW1:
	
			if (tachRPM_ > desiredRPM[0])
                percentage -= 0.01;
            
			else if (tachRPM_ < desiredRPM[0])
					percentage += 0.01;
			
		break;
			
		case ROW2:
		
				if (tachRPM_ > desiredRPM[1])
						percentage -= 0.01;
				
				else if (tachRPM_ < desiredRPM[1])
						percentage += 0.01;
				
				break;
				
		case ROW3:
		
				if (tachRPM_ > desiredRPM[2])
						percentage -= 0.01;
				
				else if (tachRPM_ < desiredRPM[2])
						percentage += 0.01;
				
				break;
				
				
		case ROW4:
		
				if (tachRPM_ > desiredRPM[3])
						percentage -= 0.01;
				
				else if (tachRPM_ < desiredRPM[3])
						percentage += 0.01;
				
				break;
			
		case OFF:
				
		default:
			// Fan is off.
			break;
	}

	if (percentage <= 0.0f) {
		
		// Turn the fan OFF.
		*pFanRelay_ = 0;
	
	}
	else {
				
		// Don't allow the duty cycle to go to 100% or the fan speed drops, 
		//	apparently unable to find an input pulse.
		if (percentage >= 1.0f) {
			percentage = 0.999f;
		}
	
		// Apply the percentage to the PWM period to obtain the duty cycle.
		uint32_t duty = (uint32_t)(percentage * (float)PWM_PERIOD);

		// Set the duty cycle
		PWM_SetDuty(pIOConfig_->pwm.module, pIOConfig_->pwm.channel, duty);
	
		// Turn the fan ON.
		*pFanRelay_ = 1;
	
	}
		
	// Return an integer speed value between 0-100.
	return (int)((percentage * 100.0f) + 0.5f);
	
}

// The function checks the current display mode and updates the Display
//	module with a value to display.
static void UpdateDisplay(int fanSpeed, int RPM)
{
	
	int displayValue;
	DisplayMode_t displayMode = GetDisplayMode();
	
	switch (displayMode) {
		
		case DISPLAYMODE_TACH:
			displayValue = RPM;
			break;
		
		case DISPLAYMODE_SPEED:
		default:
			displayValue = fanSpeed;
			break;
	
	}
	
	// Temperature could become a negative number, which isn't supported by the display,
	//	so force it to be positive. 
	if (displayValue < 0) {
		displayValue *= -1;
	}
	
	// Update the display.
	Display_Update(displayValue);			
	
}


// Scan function reads the analog and switch inputs, calculates and sets the fan speed,
//	and updates the display.
static void Scan(void)
{

	// Get the value (0-4095) of the manual speed potentiometer.
	// int speedPot = ReadSpeedPot();

	// Calculate and set the fan speed.
	int fanSpeed = RunFanSpeed();
		
	// Update the display.
	UpdateDisplay(fanSpeed, tachRPM_);
	
}

//----------------------- FanController_Run --------------------------
// Runs the FanController.  This is the main entry point.  Blocks and 
//   doesn't return.  Should be called by the main() function upon startup.
// Inputs:  pIOConfig - a pointer to the IO configuration that the 
//   FanController should use.
// Outputs:  none
void FanController_Run(FanController_IOConfig_t* pIOConfig)
{
	// Initialize the device IO.  If this fails then go no further.
	if (InitHardware(pIOConfig)) {
		ErrHandler();
	}

	// Save a pointer to the IO config.  It will be used again inside the callback functions.
	pIOConfig_ = pIOConfig;

		
	while (1) 
	{			

		// Read inputs, process, and write outputs...
		Scan();

		// Sleep approximately 100ms...
		SysTick_Wait10ms(10);

	}
	
}
