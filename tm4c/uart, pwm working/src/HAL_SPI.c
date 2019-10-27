// File:  HAL_SPI.c
// Author: JSpicer
// Date:  11/11/17
// Purpose: SPI utilities
// Hardware:  TM4C123 Tiva board

#include "HAL.h"
#include "tm4c123gh6pm.h"

// These are the base IO addresses of the SSI modules.
#define SSI0_REG_BASE 	((volatile uint32_t *)0x40008000)
#define SSI1_REG_BASE		((volatile uint32_t *)0x40009000)
#define SSI2_REG_BASE		((volatile uint32_t *)0x4000A000)
#define SSI3_REG_BASE		((volatile uint32_t *)0x4000B000)

// This structure represents the registers associated with an SSI module.
//	It will be overlayed on top of IO memory so that the structure fields
//	map to the registers.  (See the datasheet for field/register descriptions).
typedef struct {
  uint32_t  CR0;
  uint32_t  CR1;
  uint32_t  DR;
  uint32_t  SR;
  uint32_t  CPSR;
  uint32_t  IM;
  uint32_t  RIS;
	uint32_t  MIS;
  uint32_t  ICR;
  uint32_t  DMACTL;
  uint32_t  RESERVED[1000];
  uint32_t  CC;
} SSIRegs_t;

// This array is a look table to resolve the SSI module name to its base address.
const volatile uint32_t * SSIBaseAddress[] = {
	SSI0_REG_BASE,
	SSI1_REG_BASE,
	SSI2_REG_BASE,
	SSI3_REG_BASE
};

//----------------------- SPI_Enable --------------------------
// Enables the specified SSI module/channel for SPI
// Inputs:  module - the SSI module name.
// Outputs:  none.
int SPI_Enable(SSIModule_t module)
{
	
	// For now, require the bus clock to be 80MHz.
	// TODO:  Will need to work out a way to set an arbitrary bit rate with or
	//	without knowing the bus clock frequency.
	if (PLL_GetBusClockFreq() != 80000000) {
		return -1;
	}
	
	// Overlay the SSI register structure on top of the SSIx memory region...
	volatile SSIRegs_t* ssi = (volatile SSIRegs_t*)SSIBaseAddress[module];
	
	switch (module) {
		
		case SSI0:
			GPIO_EnableAltDigital(PORTA, 0x2C, 0x02);
			break;
		
		case SSI1:
			GPIO_EnableAltDigital(PORTD, 0x0B, 0x02);
			break;
		
		default:
			// TODO:  Implement other SSI modules as needed.
			break;
		
	}
	
	uint8_t moduleBit = 0x1 << ((uint8_t)module);
	
	// Enable clock to SSI module.
	SYSCTL_RCGCSSI_R |= moduleBit;
	
	// Wait for the SSI peripheral to be ready...
	while (!(SYSCTL_PPSSI_R & moduleBit )){}
	
	// Disable SSI module and make it master
	ssi->CR1 = 0;
	
	// Use system clock.
	ssi->CC = 0;
	
	// CPOL=0, CPHA=0, SPI format, 16-bit data.
	ssi->CR0 = SSI_CR0_DSS_8;
	
	// Prescale = 80 => Bitrate = 1MHz, assuming bus clock is 80MHz.
	ssi->CPSR = 80;//200;
	//ssi->CR0 |= (40 << 8);
	
	// Set SSE bit to enable SSI module.
	ssi->CR1 |= SSI_CR1_SSE;
	
	return 0;
}

//----------------------- SPI_Write ---------------------------
// Writes a byte of data to the SPI bus.
// Inputs:  module - the SSI module name.
//          data - the data byte to write.
// Outputs:  none.
void SPI_Write(SSIModule_t module, uint8_t data)
{
	// Overlay the SSI register structure on top of the SSIx memory region...
	volatile SSIRegs_t* ssi = (volatile SSIRegs_t*)SSIBaseAddress[module];
	
	// Wait until FIFO not full.
	while ((ssi->SR & SSI_SR_TNF ) == 0);
	
	// Transmit 8-bits.
	ssi->DR = data;
	
	// Wait until transmission complete.
	while (ssi->SR & SSI_SR_BSY);
	
}

