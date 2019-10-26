#include "tm4c123gh6pm.h"

#include "ADCSWTrigger.h"
#include "PLL.h"


void Led_Init();
void B_Init();
void Switch_Init();
void set_L(int new_L);
void DisableInterrupts(void); // Disable interrupts
void EnableInterrupts(void);  // Enable interrupts
void WaitForInterrupt(void);  // low power mode

int main(void){    
	unsigned long potentiometer, sensor1, sensor2;
	DisableInterrupts();  // disable interrupts while initializing 
	ADC_Init298();
	PLL_Init();                           // 80 MHz
	//Led_Init();         // output from PA5, SysTick interrupts
	B_Init();
	Switch_Init();        // arm PF4, PF0 for falling edge interrupts	
  EnableInterrupts();  // The grader uses interrupts
  while(1){
		WaitForInterrupt(); // low power mode
		//ADC_In298(&potentiometer, &sensor1, &sensor2); // sample AIN2(PE1), AIN9 (PE4), AIN8 (PE5)
		ReadADCMedianFilter(&potentiometer, &sensor1, &sensor2);
  }
}


unsigned long H,L;
/*
void Led_Init(void){
  SYSCTL_RCGC2_R |= 0x00000020; // activate clock for port F
  H = L = 40000;                // 50%
  GPIO_PORTF_AMSEL_R &= ~0x0E;      // disable analog functionality on leds (PF1,2,3)
  GPIO_PORTF_PCTL_R &= ~0x00F00000; // configure PF0 as GPIO
  GPIO_PORTF_DIR_R |= 0x0E;     // make leds (PF1,2,3) output
  GPIO_PORTF_AFSEL_R &= ~0x0E;  // disable alt funct on leds (PF1,2,3)
  GPIO_PORTF_DEN_R |= 0x0E;     // enable digital I/O on leds (PF1,2,3)
  GPIO_PORTF_DATA_R &= ~0x0E;   // make leds (PF1,2,3) low
  NVIC_ST_CTRL_R = 0;           // disable SysTick during setup
  NVIC_ST_RELOAD_R = L-1;       // reload value for 500us
  NVIC_ST_CURRENT_R = 0;        // any write to current clears it
  NVIC_SYS_PRI3_R = (NVIC_SYS_PRI3_R&0x00FFFFFF)|0x40000000; // priority 2
  NVIC_ST_CTRL_R = 0x00000007;  // enable with core clock and interrupts
	GPIO_PORTF_DATA_R = 0x0A;  		// Initialize led to red
}
*/

void B_Init(void){
  SYSCTL_RCGC2_R |= 0x00000002; // activate clock for port F
  H = L = 40000;                // 50%
  GPIO_PORTB_AMSEL_R &= ~0x01;      // disable analog functionality on leds (PF1,2,3)
  GPIO_PORTB_PCTL_R &= ~0x00F00000; // configure PF0 as GPIO
  GPIO_PORTB_DIR_R |= 0x01;     // make leds (PF1,2,3) output
  GPIO_PORTB_AFSEL_R &= ~0x01;  // disable alt funct on leds (PF1,2,3)
  GPIO_PORTB_DEN_R |= 0x01;     // enable digital I/O on leds (PF1,2,3)
  GPIO_PORTB_DATA_R &= ~0x01;   // make leds (PF1,2,3) low
  NVIC_ST_CTRL_R = 0;           // disable SysTick during setup
  NVIC_ST_RELOAD_R = L-1;       // reload value for 500us
  NVIC_ST_CURRENT_R = 0;        // any write to current clears it
  NVIC_SYS_PRI3_R = (NVIC_SYS_PRI3_R&0x00FFFFFF)|0x40000000; // priority 2
  NVIC_ST_CTRL_R = 0x00000007;  // enable with core clock and interrupts
	//GPIO_PORTB_DATA_R = 0x0A;  		// Initialize led to red
}

void SysTick_Handler(void){
  if(GPIO_PORTB_DATA_R&0x01){   // toggle leds (PF1,2,3)
    GPIO_PORTB_DATA_R &= ~0x01; // make leds (PF1,2,3) low
    NVIC_ST_RELOAD_R = L-1;     // reload value for low phase
  } else{
    GPIO_PORTB_DATA_R |= 0x01;  // make leds (PF1,2,3) high
    NVIC_ST_RELOAD_R = H-1;     // reload value for high phase
  }
}


void Switch_Init(void){
	unsigned long volatile delay;
  SYSCTL_RCGC2_R |= 0x00000020; // (a) activate clock for port F
  delay = SYSCTL_RCGC2_R;
  GPIO_PORTF_LOCK_R = 0x4C4F434B; // unlock GPIO Port F
  GPIO_PORTF_CR_R = 0x11;         // allow changes to PF4,0
  GPIO_PORTF_DIR_R &= ~0x11;    // (c) make PF4,0 in (built-in button)
  GPIO_PORTF_AFSEL_R &= ~0x11;  //     disable alt funct on PF4,0
  GPIO_PORTF_DEN_R |= 0x11;     //     enable digital I/O on PF4,0
  GPIO_PORTF_PCTL_R &= ~0x000F000F; //  configure PF4,0 as GPIO
  GPIO_PORTF_AMSEL_R &= ~0x11;  //     disable analog functionality on PF4,0
  GPIO_PORTF_PUR_R |= 0x11;     //     enable weak pull-up on PF4,0
  GPIO_PORTF_IS_R &= ~0x11;     // (d) PF4,PF0 is edge-sensitive
  GPIO_PORTF_IBE_R &= ~0x11;    //     PF4,PF0 is not both edges
  GPIO_PORTF_IEV_R &= ~0x11;    //     PF4,PF0 falling edge event
  GPIO_PORTF_ICR_R = 0x11;      // (e) clear flags 4,0
  GPIO_PORTF_IM_R |= 0x11;      // (f) arm interrupt on PF4,PF0
  NVIC_PRI7_R = (NVIC_PRI7_R&0xFF00FFFF)|0x00400000; // (g) priority 2
  NVIC_EN0_R = 0x40000000;      // (h) enable interrupt 30 in NVIC
}
// L range: 8000,16000,24000,32000,40000,48000,56000,64000,72000
// power:   10%    20%   30%   40%   50%   60%   70%   80%   90%
void GPIOPortF_Handler(void){ // called on touch of either SW1 or SW2
  if(GPIO_PORTF_RIS_R&0x01){  // SW2 touch
    GPIO_PORTF_ICR_R = 0x01;  // acknowledge flag0
    if(L>8000) L = L-8000;    // slow down
  }
  if(GPIO_PORTF_RIS_R&0x10){  // SW1 touch
    GPIO_PORTF_ICR_R = 0x10;  // acknowledge flag4
    if(L<72000) L = L+8000;   // speed up
  }
	L = 8000; // hard code
  H = 80000-L; // constant period of 1ms, variable duty cycle
}

void set_L(int new_L){
	L = new_L;
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


// PF4 