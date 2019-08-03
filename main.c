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
#include "SysTick.h"
#include <stdint.h>	
#include "tm4c123gh6pm.h"

//-------------------------------------------------------------------
// LED Status Variable
//#define LED  						 		(*((volatile unsigned long *)0x400253FC))	
//-------------------------------------------------------------------
// COLORS of LED:
#define GPIO_LOCK_KEY           0x4C4F434B  // Unlocks the GPIO_CR register
#define PF0       (*((volatile uint32_t *)0x40025004))
#define PF4       (*((volatile uint32_t *)0x40025040))
#define SWITCHES  (*((volatile uint32_t *)0x40025044))
#define SW1       0x01                      // on the left side of the Launchpad board
#define SW2       0x10                      // on the right side of the Launchpad board
#define SYSCTL_RCGC2_GPIOF      0x00000020  // port F Clock Gating Control
#define SYSCTL_RCGC2_GPIOB			0x00000002	// port B Clock Gating Control
#define SYSCTL_TCGC2_FPIOA			0x00000001	// port A Clock Gating Control
#define RED       0x02
#define BLUE      0x04
#define GREEN     0x08
#define YELLOW    0x0A
#define SKYBLUE   0x0C
#define WHITE     0x0E
#define PINK			0x06
#define DARK			0x00
//-------------------------------------------------------------------

void EnableInterrupts(void);  // Enable interrupts
void PortF_Init(void);
//void Delay(int);


void Delay(void){unsigned long volatile time;
  time = 727240*200/91;  // 0.1sec
  while(time){
    time--;
  }
}
// do not edit this main
// your job is to implement the UART_OutUDec UART_OutDistance functions 
int main(void){ 
	unsigned int KEY;
	int x;
	
  PLL_Init();								// set system clock to 80 MHz
	PortF_Init();							// Setup LEDs
  UART1_Init();              // initialize UART
  EnableInterrupts();       // needed for TExaS
 
  while(1){
		GPIO_PORTF_DATA_R = RED;
		UART1_OutString("AT+NAME=MarkAndTrieuVy");
		for(x=0; x<10; x++){
			Delay();
		}
 		GPIO_PORTF_DATA_R = BLUE;
		UART1_OutString("AT+PSWD=6669");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = YELLOW;
		UART1_OutString("AT+UART=57600,0,1");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = SKYBLUE;
		UART1_OutString("AT+RESET");
		for(x=0; x<10; x++){
			Delay();
		}
		
		/*
		GPIO_PORTF_DATA_R = GREEN;
		UART1_OutString("AT+ROLE0");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = DARK;
		UART1_OutString("AT+PARI2");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = RED;
		UART1_OutString("AT+STOP0");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = PINK;
		UART1_OutString("AT+BAUD3");
		for(x=0; x<10; x++){
			Delay();
		}
		GPIO_PORTF_DATA_R = WHITE;
		*/
		while(1); 																				// all configuration are complete
	}
}
		
			
		/*
		LED ^= BLUE;
		Delay(10);
		UART1_OutString("AT+NAME=MarkAndTrieuVy");
		UART1_OutChar(0x0A);
		UART1_OutChar(0x0D);
		LED ^= GREEN;
		Delay(10);
		UART1_OutString("AT+PSWD=6669");
		UART1_OutChar(0x0A);
		UART1_OutChar(0x0D);
		Delay(10);
		LED = RED;
		UART1_OutString("AT+UART=38400,0,1");
		UART1_OutChar(0x0A);
		UART1_OutChar(0x0D);
		Delay(10);
		LED = 0xE;
		UART1_OutString("AT+RESET");
		UART1_OutChar(0x0A);
		UART1_OutChar(0x0D);
		Delay(10);
		//SysTick_Wait10ms(10);
		
		KEY = UART_InChar();
    if(KEY==0x67){
			LED ^= GREEN;
			if(LED & GREEN) 
				UART_OutString("Green LED is on!");
			else
				UART_OutString("Green LED is off!");
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
		}
		
		else if(KEY==0x72){
			LED ^= RED;
			if(LED & RED) 
				UART_OutString("Red LED is on!");
			else
				UART_OutString("Red LED is off!");
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
		}
		
		else if(KEY==0x62){
			LED ^= BLUE;
			if(LED & BLUE) 
				UART_OutString("Blue LED is on!");
			else
				UART_OutString("Blue LED is off!");
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
		}
		
		else if(KEY==0x65){
			LED = 0x0E;
			UART_OutString("All LEDs have been turned on!");
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
			
		}
		
		else if(KEY==0x71){
			LED = OFF;
			UART_OutString("All LEDs have been turned off!");
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
		}*/
		



//*******************************************************************
// Subroutine to initialize port F pins for input and output
// PF4 is input SW1 
// PF3,PF2,PF1 are outputs to the LEDs
//*******************************************************************
void PortF_Init(void){
	unsigned volatile delay;
	SYSCTL_RCGCGPIO_R |= 0x00000020;  // 1) activate clock for Port F
  delay = SYSCTL_RCGCTIMER_R;
	GPIO_PORTF_LOCK_R = 0x4C4F434B;   // 2) unlock GPIO Port F
  GPIO_PORTF_CR_R = 0x1F;           // allow changes to PF4-0
  // only PF0 needs to be unlocked, other bits can't be locked
  GPIO_PORTF_AMSEL_R = 0x00;        // 3) disable analog on PF
  GPIO_PORTF_PCTL_R = 0x00000000;   // 4) PCTL GPIO on PF4-0
  GPIO_PORTF_DIR_R = 0x0E;          // 5) PF4,PF0 in, PF3-1 out
  GPIO_PORTF_AFSEL_R = 0x00;        // 6) disable alt funct on PF7-0
  GPIO_PORTF_PUR_R = 0x11;          // enable pull-up on PF0 and PF4
  GPIO_PORTF_DEN_R = 0x0E;          // 7) enable digital I/O on PF3-1
}

