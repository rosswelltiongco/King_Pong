#include "tm4c123gh6pm.h"
#include "UART.h"
#include "PWM.h"
#include "PLL.h"
#include "SysTick.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void LED_Init(void);
void DisableInterrupts(void); // Disable interrupts
void EnableInterrupts(void);  // Enable interrupts
void WaitForInterrupt(void);  // low power mode
void SysTick_Handler(void);
unsigned long systick;
// COLORS of LED:
#define LED  (*((volatile unsigned long *)0x400253FC))	
#define RED 	      0x02
#define BLUE 	      0x04
#define GREEN       0x08
#define OFF 	      0x00
//#define PB2					0x04
#define PD6					0x40
#define ACTIVE			0x40
uint8_t TACH;
uint8_t toggle;
uint16_t COUNT_RPM, RPM;
bool RESET;

uint16_t current_RPM, desired_RPM, current_PWM;
signed int sum;
float error;
float kp = 0.001;

int main(void){    
	unsigned char KEY;
	unsigned int key;
	DisableInterrupts();  // Disable interrupts while initializing 
	PLL_Init();           // 50 MHz
	SysTick_Init(16000000);
	LED_Init(); 
	UART_Init(); 
	Tach_Init();
	PWM0A_Init(25000,15000);
  EnableInterrupts();  
	RESET=false;
	COUNT_RPM=0; RPM=0; KEY = 0; key = 0;
	
	desired_RPM = 10000;
  while(1)
	{
		if(systick > 5) //check for 1sec to have passed
		{
			if(toggle)
			{
				toggle = 0;
				LED = GREEN;
			}
			else
			{
				toggle = 1;
				LED = BLUE;
			}
			systick = 0;
			UART_OutUDec((60*(unsigned long)COUNT_RPM)/2);
			UART_OutChar(0x0A);
			UART_OutChar(0x0D);
			COUNT_RPM = 0;
		}
			
  } // while(1)
} // main

void LED_Init(void){ volatile unsigned long delay;
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
	NVIC_PRI7_R = (NVIC_PRI7_R&0xFF1FFFFF)|0x00A00000; // (g) priority 5
	NVIC_EN0_R = 0x40000000; 					// (h) enable interrupt 30 in NVIC
}

void GPIOPortD_Handler(void){
	unsigned char TACH_pin;
	TACH_pin = GPIO_PORTD_RIS_R&PD6;// Check Tach(PD6)
	if(TACH_pin)
		COUNT_RPM++;
	GPIO_PORTD_ICR_R = PD6; 		// acknowledge flag6
}

void SysTick_Handler(void){
	systick++;
	
}
