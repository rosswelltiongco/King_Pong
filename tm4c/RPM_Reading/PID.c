//PID Example, this is the bare minimum to implement PID safely and correctly
//  It's also not a bad idea to scale all values to be a float bound within 0 to 1
//  example: 8-bit sensor input and 8-bit PWM output
//	Feedback from Sensor = 0 to 255, Output to PWM = 0 to 255, and Setpoint = 128 (50% of max) 
//  Everytime a new Sensor Value is Received:
//		PWMvalue = PID(float(128/255),NewSensorValue()/255) * 255;
//			To Operate Correctly, The Arguments Must Never Be Below 0 or Above 1

//These Coefficients need to be tuned/adjusted for the desired response of the system
#define Kp 0.50 /* Coefficient of Proportional (Values 0 to 1)*/
#define Ki 0.15 /* Coefficient of Integral (Values 0 to 1)*/
//#define Kd 0.01 /* Coefficient of Derivative (Values 0 to 1)*/

//SP = SetPoint, the desired operating point, i.e. Position/Velocity/etc...
//PV = ProcessVariable, the feedback from the Plant/System, i.e. DistanceSensor/RPMs/etc...
//MV = ManipulatedVariable, the new value to drive the Plant/System, i.e. PWM value for motor/etc...

float PID(float set_point, float PV)
{
	float Error, MV;
	static float Integral, prevIntegral;
	
	//SP = 0;								//Get Setpoint
	//PV = feedBack(void);	//Get Process Variable
	
	//Calculate Error
	Error = set_point - PV;
	
	//prevError = Error; //Save a copy for Derivative Calculation
	
	//Calculate Integral Term, we also need to make sure the Integral does not overflow
	//	and if it does overflow we need to disregard that result and use the old value
	prevIntegral = Integral;	//Save a copy of the Integral before we calculate a new one
	//Calculate the new Integral Term, Apply Ki here so we can accumulate more times without overflowing
	Integral = Integral + (Error * Ki);
	//Check if the Integral Calculation Resulted in an Overflow
	if((prevIntegral > 0) && (Error > 0) && (Integral < 0)) //Check if the result had a sign change
		Integral = prevIntegral;	//Overflow Occurred, restore previously calculated integral
	if((prevIntegral < 0) && (Error < 0) && (Integral > 0)) //Check if the result had a sign change
		Integral = prevIntegral;	//Overflow Occurred, restore previously calculated integral
	//Since this PID loop is designed to operate between 0 and 1, we can also keep I from windup problems
	//  by checking it and clamping it -1 or 1
	if(Integral > 1) Integral = 1;
	if(Integral < -1) Integral = -1;
	
	//Calculate Derivative Term
	//Derivative = Error - prevError;
	
	//Calculate Manipulated Variable, only one of these should be used
	//P Controller - P only: Rarely Used
	MV = Error * Kp;
	//PI Controller - PI Only: Most Common
	MV = (Error * Kp) + Integral;
	//PID Controller - PID: Common, but be careful as D can add a lot of noise/jitter - Kd should be kept small
	//MV = (Error * Kp) + Integral + (Derivative * Kd);
	
	/*
	//Add a Bias
	MV = MV + 0.5;
	
	//Lets also make sure MV never falls outside 0 and 1
	if(MV > 1) MV = 1;
	if(MV < 0) MV = 0;
	*/
	
	return MV;
}
