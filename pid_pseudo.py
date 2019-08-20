#pseudo code for PID controller

import numpy as np
import matplotlab.pyplot as plt 
import scipy.integrate as S


def Derivative(z, t):
		x = z[0] ;
		xdot = z[1];
		eint = z[2];
		
		
		#our input 
		#proportional control 
		xc = 10;
		e	 = xc - x;
		kp = 50;
		
		#derivative control 
		xcdot = 0;
		edot  = xcdot - xdot;
		kd = 25;
		
		
		#integral gain 
		eintdot = e;
		f = (kp * e) + (ki * eint) + (kd *edot);
		
		#f is the input forcing function
		sdldot = f - 2*xdot - 3*x;
		
		zdot = np.asarray([xdot, xdbldot, eintdot]);
		return zdot 
		
plt.close("all")

zinitial = np.asarray([-2, -5, 0]);
tspan = np.arange(0, 10, 0.01);

zout = S.odeint(Derivative, zinitial, tspan);

xout = zout[:, 0];

plt.plot(tspan, xout)
plt.show()
