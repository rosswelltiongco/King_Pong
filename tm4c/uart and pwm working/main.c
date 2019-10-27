#include "tm4c123gh6pm.h"
#include "UART.h"
#include "ADCSWTrigger.h"
#include "PLL.h"

void LED_Init(void);
void PWM_Init(void);
void Switch_Init(void);
void DisableInterrupts(void); // Disable interrupts
void EnableInterrupts(void);  // Enable interrupts
void WaitForInterrupt(void);  // low power mode

unsigned long H,L;

// COLORS of LED:
#define LED  (*((volatile unsigned long *)0x400253FC))	
#define RED 	      0x02
#define BLUE 	      0x04
#define GREEN       0x08
#define OFF 	      0x00

int main(void){    
	//unsigned long potentiometer, sensor1, sensor2;
	unsigned char KEY = 'n';
	DisableInterrupts();  // disable interrupts while initializing 
	ADC_Init298();
	PLL_Init();           // 80 MHz
	LED_Init();
	UART_Init();
	PWM_Init();
  EnableInterrupts();  // The grader uses interrupts
	LED = BLUE;
	L = 10;
  while(1)
	{
		KEY = UART_InChar();
	
		if(KEY=='1'){			
			L = 5000;
			LED = GREEN;
		}
		else if(KEY=='2'){	
			L = 6000;
			LED = RED;
		}
		else if(KEY=='3'){	
			L = 7000;
			LED = BLUE;
		}
		else if(KEY=='4'){	
			L = 10;
			LED = OFF;
		}
		H = 10000-L; // constant period of 1ms, variable duty cycle
		UART_OutChar('1');
		
		//ADC_In298(&potentiometer, &sensor1, &sensor2); // sample AIN2(PE1), AIN9 (PE4), AIN8 (PE5)
		//ReadADCMedianFilter(&potentiometer, &sensor1, &sensor2);
  }
}
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

void PWM_Init(void){
  SYSCTL_RCGC2_R |= 0x00000002; // activate clock for port F
  H = L = 5000;                // 50%
  GPIO_PORTB_AMSEL_R &= ~0x04;      // disable analog functionality on leds (PF1,2,3)
  GPIO_PORTB_PCTL_R &= ~0x00F00000; // configure PF0 as GPIO
  GPIO_PORTB_DIR_R |= 0x04;     // make leds (PF1,2,3) output
  GPIO_PORTB_AFSEL_R &= ~0x04;  // disable alt funct on leds (PF1,2,3)
  GPIO_PORTB_DEN_R |= 0x04;     // enable digital I/O on leds (PF1,2,3)
  GPIO_PORTB_DATA_R &= ~0x04;   // make leds (PF1,2,3) low
  NVIC_ST_CTRL_R = 0;           // disable SysTick during setup
  NVIC_ST_RELOAD_R = L-1;       // reload value for 500us
  NVIC_ST_CURRENT_R = 0;        // any write to current clears it
  NVIC_SYS_PRI3_R = (NVIC_SYS_PRI3_R&0x00FFFFFF)|0x40000000; // priority 2
  NVIC_ST_CTRL_R = 0x00000007;  // enable with core clock and interrupts
}

void SysTick_Handler(void){
  if(GPIO_PORTB_DATA_R&0x04){   // toggle leds (PF1,2,3)
    GPIO_PORTB_DATA_R &= ~0x04; // make leds (PF1,2,3) low
    NVIC_ST_RELOAD_R = L-1;     // reload value for low phase
  } else{
    GPIO_PORTB_DATA_R |= 0x04;  // make leds (PF1,2,3) high
    NVIC_ST_RELOAD_R = H-1;     // reload value for high phase
  }
}

// L range: 8000,16000,24000,32000,40000,48000,56000,64000,72000
// power:   10%    20%   30%   40%   50%   60%   70%   80%   90%


