#include "tm4c123gh6pm.h"
#include "UART.h"
#include "UART_Pi.h"
#include "PWM.h"
#include "PLL.h"
#include "PID.h"
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
unsigned long systick, UART;
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

uint16_t current_RPM, desired_RPM=10000, current_PWM, PWM;



signed int sum;
float error;
float kp = 0.001;

float PV;
unsigned char cup;

int main(void){    
	//unsigned char KEY;
	DisableInterrupts();  // Disable interrupts while initializing 
	PLL_Init();           // 50 MHz
	SysTick_Init(16000000);
	LED_Init(); 
	UART0_Init();  // Realterm
	UART1_Init();  // Raspberry Pi
	Tach_Init();
	PWM = 15000;
	PWM0A_Init(25000,PWM);
  EnableInterrupts();  
	RESET=false;
	COUNT_RPM=0; RPM=0;
	
	desired_RPM = 10000;
  while(1)
	{
		
		if(UART > 80)
		{
			cup = UART0_InChar();
			switch(cup)
			{
				case '1': 
					desired_RPM=10000;
					break;
				case '2': 
					desired_RPM=12000;
					break;
				case '3': 
					desired_RPM=15000;
					break;
				case '4': 
					desired_RPM=16000;
					break;
				case '5': 
					desired_RPM=14000;
					break;
				case '6': 
					desired_RPM=9000;
					break;
				case '7': 
					desired_RPM=4000;
					break;
				case '8': 
					desired_RPM=5000;
					break;
				case '9': 
					desired_RPM=18000;
					break;
				default:
					desired_RPM=20000;
					break;
			}
			UART = 0;
		}
			
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
			
			current_RPM = (60*(unsigned long)COUNT_RPM)/2;
			
			PWM += (PID((float)desired_RPM,(float)current_RPM));
			PWM0A_Duty(PWM);

			UART1_OutUDec(current_RPM);
			UART1_OutChar(0x0A);
			UART1_OutChar(0x0D);
			
			UART0_OutUDec(current_RPM);
			UART0_OutChar(0x0A);
			UART0_OutChar(0x0D);
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
	UART++;
}