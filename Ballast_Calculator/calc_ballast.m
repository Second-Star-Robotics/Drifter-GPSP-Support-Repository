function m_ballast = calc_ballast(V_vehicle, m_vehicle, rho_water, rho_ballast)
%CALC_BALLAST Calculate the amount of ballast based on water density
%function m_ballast = calc_ballast(V_vehicle, m_vehicle, rho_water, rho_ballast)
%inputs:
%   V_vehicle = Volume of vehicle in m3 (eg. 0.0523994 m3)
%   m_vehicle = mass of vehicle in kg (eg. 52.3994 kg)
%   rho_water = density of seawater (eg. 1023.6 kg/m3)
%   rho_ballast = density of ballast (eg. diveweight = 11290 kg/m3, steel = 8050 kg/m3)
%outputs:
%   m_ballast = ballast mass in kilograms (negative means remove ballast)

%Constants
a_g = 9.80655; %[m/s] Acceleration due to gravity

%Calculate Vehicle forces
Fb_vehicle = rho_water*V_vehicle*a_g;
Fg_vehicle = m_vehicle*a_g;

%Calculate ballast mass to trim
m_ballast = (Fb_vehicle-Fg_vehicle)/(a_g-(rho_water*a_g)/(rho_ballast));

