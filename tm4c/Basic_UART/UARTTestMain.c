// UARTTestMain.c
// Runs on LM4F120/TM4C123
// Used to test the UART.c driver
// Daniel Valvano
// September 12, 2013

/* This example accompanies the book
   "Embedded Systems: Real Time Interfacing to Arm Cortex M Microcontrollers",
   ISBN: 978-1463590154, Jonathan Valvano, copyright (c) 2013

 Copyright 2013 by Jonathan W. Valvano, valvano@mail.utexas.edu
    You may use, edit, run or distribute this file
    as long as the above copyright notice remains
 THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED
 OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
 VALVANO SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL,
 OR CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 For more information about my classes, my research, and my books, see
 http://users.ece.utexas.edu/~valvano/
 */

// U0Rx (VCP receive) connected to PA0
// U0Tx (VCP transmit) connected to PA1

#include "tm4c123gh6pm.h"
#include "PLL.h"
#include "UART.h"
#include "SysTick.h"


void EnableInterrupts(void);



int main(void){
	unsigned char x;
  unsigned char i;
  char string[20];  // global to assist in debugging
  unsigned long c;
	unsigned long previous = 'r'; //default r: sawtooth
	
	SysTick_Init();
	Init_PortB();
  
  UART_Init();              // initialize UART
	
	
  OutCRLF();
	
	PORTF_Init();
		EnableInterrupts();          		 	//AFTER inits, 
	
	PLL_Init();
	
  GPIO_PORTF_DATA_R = 0x02; // Red
	
	UART_OutString("UART Initialized"); OutCRLF();
	
  while(1){
	
		
		c = UART_InCharNonBlocking();
		
		
		if (c=='s') {
			UART_OutString("sine wave displayed");
			OutCRLF();
			previous = 's';
			
		}
		else if (c=='t'){
			UART_OutString("triangle wave displayed");
			OutCRLF();
			previous = 't';
		}
		else if (c == 'q'){
			UART_OutString("square wave displayed");
			OutCRLF();
			previous = 'q';
		}
		else if (c == 'r'){
			UART_OutString("Sawtooth wave displayed");
			OutCRLF();
			previous = 'r';
		}
		else if (c=='0'){
			// No message
			previous = previous;
		}
			
    if (previous == 'r'){
			sawtoothWave(5150);
		}
		else if (previous == 't'){
			triangleWave(2550); 
		}
		else if (previous == 's'){
			sineWave(5150);
		}
		else if (previous == 'q'){
			squareWave(2550);
			
		}
		//else { sawtooth default }
  }
}


// Color    LED(s) PortF
// dark     ---    0
// red      R--    0x02
// blue     --B    0x04
// green    -G-    0x08
// yellow   RG-    0x0A
// sky blue -GB    0x0C	
// white    RGB    0x0E
// pink     R-B    0x06

// global variable visible in Watch window of debugger
// increments at least once per button press
void PORTF_Init(void){      
  SYSCTL_RCGC2_R |= 0x00000020;     // 1) F clock
  GPIO_PORTF_LOCK_R = 0x4C4F434B;   // 2) unlock PortF PF0  
  GPIO_PORTF_CR_R = 0x1F;           // allow changes to PF4-0       
  GPIO_PORTF_AMSEL_R = 0x00;        // 3) disable analog function
  GPIO_PORTF_PCTL_R = 0x00000000;   // 4) GPIO clear bit PCTL  
  GPIO_PORTF_DIR_R = 0x0E;          // 5) PF4,PF0 input, PF3,PF2,PF1 output   
  GPIO_PORTF_AFSEL_R = 0x00;        // 6) no alternate function
  GPIO_PORTF_PUR_R = 0x11;          // enable pullup resistors on PF4,PF0       
  GPIO_PORTF_DEN_R = 0x1F;          // 7) enable digital pins PF4-PF0        	
  SYSCTL_RCGC2_R |= 0x00000020; // (a) activate clock for port F
	GPIO_PORTF_LOCK_R = 0x4C4F434B;   // 2) unlock PortF PF0  
  GPIO_PORTF_DIR_R &= ~0x10;    // (c) make PF4 in (built-in button)
  GPIO_PORTF_AFSEL_R &= ~0x10;  //     disable alt funct on PF4
  GPIO_PORTF_DEN_R |= 0x10;     //     enable digital I/O on PF4   
  GPIO_PORTF_PCTL_R &= ~0x000F0000; // configure PF4 as GPIO
  GPIO_PORTF_AMSEL_R = 0;       //     disable analog functionality on PF
  GPIO_PORTF_PUR_R |= 0x10;     //     enable weak pull-up on PF4
  GPIO_PORTF_IS_R &= ~0x10;     // (d) PF4 is edge-sensitive
  GPIO_PORTF_IBE_R &= ~0x10;    //     PF4 is not both edges
  GPIO_PORTF_IEV_R &= ~0x10;    //     PF4 falling edge event
  GPIO_PORTF_ICR_R = 0x10;      // (e) clear flag4
  GPIO_PORTF_IM_R |= 0x10;      // (f) arm interrupt on PF4
  NVIC_PRI7_R = (NVIC_PRI7_R&0xFF00FFFF)|0x00A00000; // (g) priority 5
  NVIC_EN0_R = 0x40000000;      // (h) enable interrupt 30 in NVIC
}


void sawtoothWave(int delay){
	unsigned int i; 
	for (i = 0; i < 256; i++){
		GPIO_PORTB_DATA_R = i ; 	
		SysTick_Wait(5100); 
	}
}

void triangleWave(int delay){
	unsigned int i; 
	for (i = 0; i < 256; i++){
		GPIO_PORTB_DATA_R = i; 
		SysTick_Wait(delay);
	}
	 
	for (i = 255; i>0; i--){
		GPIO_PORTB_DATA_R = i; 
		SysTick_Wait(delay); 
	}
}

void squareWave (int delay){
	unsigned int i; 
	for (i = 0; i < 256; i++){
		GPIO_PORTB_DATA_R = 0xFF; 
		SysTick_Wait(delay);
	}
	 
	for (i = 255; i>0; i--){
		GPIO_PORTB_DATA_R = 0x00; 
		SysTick_Wait(delay); 
	}
}
void sineWave(int delay){	
	unsigned int i ; 
	for(i=0; i<256; i++){
		GPIO_PORTB_DATA_R = sineTable[i]; 
		SysTick_Wait(delay); 
	}
}


void Init_PortB(void){ 
  SYSCTL_RCGC2_R |= 0x00000002;     // 1) B clock
  GPIO_PORTB_CR_R |= 0xFF;           // allow changes to PB7-0      
  GPIO_PORTB_AMSEL_R = 0x00;        // 3) disable analog function
  GPIO_PORTB_PCTL_R = 0x00000000;   // 4) GPIO clear bit PCTL  
  GPIO_PORTB_DIR_R = 0xFF  ;          // 5) PB7-PB0 output 
  GPIO_PORTB_AFSEL_R = 0x00;        // 6) no alternate function
  GPIO_PORTB_DEN_R |= 0xFF;          // 7) enable digital pins P7-PB0   
}