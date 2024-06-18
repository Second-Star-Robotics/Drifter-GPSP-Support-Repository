openfig("Drifter8_Dive1.fig")

%Internal Volume Error from Target.
%If internal volume is too low platform is ballasted too heavy and needs to remove weight.
%If internal volume is lower than target platform needs additional weight

Nabla_internal_at_hover = 1207.17e-6; %m3 internal scale volume at hover from depth log
Nabla_internal_at_hover_target = 1400e-6; %m3 target internal scale volume at hover

Nabla_internal_error = Nabla_internal_at_hover - Nabla_internal_at_hover_target;

%1. CALCULATE INITIAL CONDITIONS
%Constants
a_g = 9.80655; %[m/s] Acceleration due to gravity
rho_water = 1023; %[kg/m3] Density of seawater at hover

B_corrected_volume =  -rho_water*Nabla_internal_error*a_g; %[N] Buoyancy due to corrected volume displaced by engine

%Force on platform due to corrected volume
Z_corrected_volume = B_corrected_volume; %[N]

%1. CALCULATE REMOVED BALLAST (if needed)
%Ballast to be removed (1 lb lead dive weight.
rho_Ballast_removed = 11290; %kg/m3
m_Ballast_removed = 0.454; %kg Mass of ballast to be removed
Nabla_Ballast_removed = m_Ballast_removed/rho_Ballast_removed;

B_Ballast_removed = -rho_water*Nabla_Ballast_removed
W_Ballast_removed = m_Ballast_removed*a_g
Z_ballast_removed = B_Ballast_removed+W_Ballast_removed

%2.  Calculate Z_ballast_added
%Add steel ballast to adjust
rho_Ballast_added = 
