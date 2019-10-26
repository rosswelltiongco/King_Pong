// main.c
// Runs on LM4F120/TM4C123
// Test main for Lab 11
// January 15, 2016

// this connection occurs in the USB debugging cable
// U0Rx (PA0) connected to serial port on PC
// U0Tx (PA1) connected to serial port on PC
// Ground connected ground in the USB cable

#include "UART.h"
#include "PLL.h"
#include <stdint.h>	
#include "tm4c123gh6pm.h"

//-------------------------------------------------------------------
// LED Status Variable
#define LED  						 		(*((volatile unsigned long *)0x400253FC))	
//-------------------------------------------------------------------
// COLORS of LED:
#define RED 	      0x02
#define BLUE 	      0x04
#define GREEN       0x08
#define OFF 	      0x00
//-------------------------------------------------------------------

void EnableInterrupts(void);  // Enable interrupts
void PortF_Init(void);

// do not edit this main
// your job is to implement the UART_OutUDec UART_OutDistance functions 
int main(void){ 
	unsigned char KEY = 'n';
  PLL_Init();								// set system clock to 80 MHz
	PortF_Init();							// Setup LEDs
  UART_Init();              // initialize UART
  EnableInterrupts();       // needed for TExaS
	LED = BLUE;
 
  while(1){
		KEY = UART_InChar();
    if(KEY=='g'){
			LED = GREEN;
			UART_OutChar('1');
		}
  }
}

//*******************************************************************
// Subroutine to initialize port F pins for input and output
// PF4 is input SW1 
// PF3,PF2,PF1 are outputs to the LEDs
//*******************************************************************
void PortF_Init(void){ volatile unsigned long delay;
	SYSCTL_RCGC2_R 	|= 0x00000020; 		// 1) F clock
	delay = SYSCTL_RCGC2_R; 					// dummy delay
	GPIO_PORTF_LOCK_R = 0x4C4F434B; 	// 2) unlock PortF PF4
	GPIO_PORTF_CR_R |= 0x0E; 					// allow changes to PF4 
	GPIO_PORTF_AMSEL_R &= ~0x0E; 			// 3) disable analog function on PF4 
	GPIO_PORTF_PCTL_R &= ~0x0000FFF0; // 4) GPIO clear bit PCTL
	GPIO_PORTF_DIR_R |= 0x0E; 				// 5) PF1,PF2,PF3 output
	GPIO_PORTF_AFSEL_R &= ~0x0E; 			// 6) no alternate function
	GPIO_PORTF_DEN_R |= 0x0E; 				// 7) enable digital pins PF4
	GPIO_PORTF_PUR_R &= ~0x11; 				// disable pullup resistors on PF4/0
	/*
	// Initialize Port F Interupt Registers for PF4 and PF0 Switches: 
	GPIO_PORTF_IS_R &= ~0x10; 				// (d) PF4 is edge-sensitive
	GPIO_PORTF_IBE_R &= ~0x10; 				// PF4 is not both edges
	GPIO_PORTF_IEV_R &= ~0x10; 				// PF4 falling edge event
	GPIO_PORTF_ICR_R = 0x10; 					// (e) clear flag4
	GPIO_PORTF_IM_R |= 0x10; 					// (f) arm interrupt on PF0 and PF1
	*/
	NVIC_PRI7_R = (NVIC_PRI7_R&0xFF1FFFFF)|0x00A00000; // (g) priority 5
	NVIC_EN0_R = 0x40000000; 					// (h) enable interrupt 30 in NVIC
}

