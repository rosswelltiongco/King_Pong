#include "tm4c123gh6pm.h"
#include "UART.h"
#include "PWM.h"
#include "PLL.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void LED_Init(void);
void Switch_Init(void);
void DisableInterrupts(void); // Disable interrupts
void EnableInterrupts(void);  // Enable interrupts
void WaitForInterrupt(void);  // low power mode

unsigned int COUNT, PULSE_COUNT;
unsigned int RPM = 1;
// COLORS of LED:
#define LED  (*((volatile unsigned long *)0x400253FC))	
#define RED 	      0x02
#define BLUE 	      0x04
#define GREEN       0x08
#define OFF 	      0x00

#define PB2					0x04
#define ACTIVE					0x04
uint8_t PULSE;

int main(void){    
	//unsigned long potentiometer, sensor1, sensor2;
	unsigned char KEY = 'n';
	DisableInterrupts();  // disable interrupts while initializing 
	PLL_Init();           // 80 MHz
	LED_Init();
	UART_Init();
	PWM0A_Init();
  EnableInterrupts();  // The grader uses interrupts
	LED = BLUE;
	//PWM0A_Duty(500);
  while(1)
	{
		KEY = UART_InChar();
	
		if(KEY=='1'){				
			PWM0A_Duty(1600);
			LED = GREEN;
		}
		else if(KEY=='2'){	
			PWM0A_Duty(2400);
			LED = RED;
		}
		else if(KEY=='3'){	
			PWM0A_Duty(2560);
			LED = BLUE;
		}
		else if(KEY=='4'){	
			PWM0A_Duty(2880);
			LED = OFF;
		}
		UART_OutString("You Suck");
		
		//ADC_In298(&potentiometer, &sensor1, &sensor2); // sample AIN2(PE1), AIN9 (PE4), AIN8 (PE5)
		//ReadADCMedianFilter(&potentiometer, &sensor1, &sensor2);
  }
}

char *my_itoa(int num, char *str)
{
        if(str == NULL)
        {
                return NULL;
        }
        sprintf(str, "%d", num);
        return str;
}
/*
int main()
{
        int num = 2016;
        char str[20];
        if(my_itoa(num, str) != NULL)
        {
                printf("%s\n", str);
        }
}
*/
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

// L range: 8000,16000,24000,32000,40000,48000,56000,64000,72000
// power:   10%    20%   30%   40%   50%   60%   70%   80%   90%


void SysTick_Handler(void){
		COUNT++;
}


void GPIOPortB_Handler(void){
	PULSE = GPIO_PORTD_RIS_R&PB2;	// Check Obstacle Sensor PB2
	// Logic in MAIN Function:
	if(PULSE==ACTIVE){
		if(COUNT!=0){ 	
			PULSE_COUNT = COUNT;
			COUNT = 0;
		}
	}
	RPM = (PULSE_COUNT/2)*60;
	GPIO_PORTD_ICR_R = PB2; 				// acknowledge flag2
}
