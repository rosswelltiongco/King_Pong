// main.c
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
void Flag_Init(void);
void Flag_Set(void);
void Flag_Clear(void);
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
#define MAX_DURATION 	0xFFFF

uint8_t 	TACH, toggle;
uint16_t 	COUNT_RPM, current_RPM, desired_RPM, PWM, PID_COUNT;

unsigned char cup;
bool execute_PID, ACTIVATE;

int main(void){	
	DisableInterrupts();  	// Disable interrupts while initializing 
	PLL_Init();           	// 50 MHz Clock
	SysTick_Init(16000000); // 100 ms
	LED_Init(); 
	UART0_Init();  // Realterm
	UART1_Init();  // Raspberry Pi
	
	Tach_Init();
	Flag_Init();
	PWM = 5000;
	PWM0A_Init(25000,PWM);
  EnableInterrupts();  
	COUNT_RPM = 0;
	PID_COUNT=0;
	
	//Initial RPM
	desired_RPM = 10000;
	execute_PID = true;
	GPIO_PORTF_DATA_R |= 0x04;
	
  while(1)
	{				
		
		if(execute_PID==false)
		{
		
		cup = UART1_InChar();
		
		if(cup=='1')
			desired_RPM=14000;
		else if(cup=='2')
			desired_RPM=14750;
		else if(cup=='3')
			desired_RPM=17000;
		else if(cup=='4')
			desired_RPM=17500;   
		else
			desired_RPM = desired_RPM;
		Flag_Clear();
		UART=0; 
		execute_PID = true;
		}
		
		if(PID_COUNT>3 && execute_PID==true){
			PWM += (PID((float)desired_RPM,(float)current_RPM));
			PWM0A_Duty(PWM);
			
			if(current_RPM<(50+desired_RPM) && current_RPM>(desired_RPM-50))
			{
				PID_COUNT=0;
				Flag_Set();
				execute_PID = false;
			}
			
			PID_COUNT=0;
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
			COUNT_RPM = 0;
			
			UART0_OutUDec(current_RPM);
			UART0_OutChar(0x0A);
			UART0_OutChar(0x0D);
		}
	}
	
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

void Flag_Init(void)
{
	volatile unsigned long Delay;
	SYSCTL_RCGC2_R |= 0x01;           // 1) activate clock for Port A
	Delay = SYSCTL_RCGC2_R;           // allow time for clock to start
									  // 2) no need to unlock PA2
	GPIO_PORTA_PCTL_R &= ~0x00000F00; // 3) regular GPIO
	GPIO_PORTA_AMSEL_R &= ~0x04;      // 4) disable analog function on PA2
	GPIO_PORTA_DIR_R |= 0x04;         // 5) set direction to output
	GPIO_PORTA_AFSEL_R &= ~0x04;      // 6) regular port function
	GPIO_PORTA_DEN_R |= 0x04;         // 7) enable digital port
}
	
void Flag_Set(void)
{
		// Set A2
		GPIO_PORTA_DATA_R |= 0x04;
}

void Flag_Clear(void)
{
		// Clear A2
		GPIO_PORTA_DATA_R &= ~0x04;
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
	PID_COUNT++;
}                             