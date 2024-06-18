openfig("Drifter8_Dive1.fig")

%Internal Volume Error from Target.
%If internal volume is too low platform is ballasted too heavy and needs to remove weight.
%If internal volume is lower than target platform needs additional weight

rho_water = 1023; %[kg/m3] density of a nominal ocean near surface

Nabla_internal_at_hover = 1207.17e-6; %m3 internal scale volume at hover from depth log
Nabla_internal_at_hover_target = 1400e-6; %m3 target internal scale volume at hover

disp("Adjust the platform neutral volume buoyancy by (m^3):")
Nabla_adjust = Nabla_internal_at_hover -  Nabla_internal_at_hover_target


m_lead_remove = 0.453592; %[kg] 1 lb lead weight to remove
rho_lead_remove = 11290; %[kg/m3] density of lead weight to remove
Nabla_lead_remove = m_lead_remove/rho_lead_remove; %Volume of lead weight to remove

%1.  Calculate mass for Pb ballast to add after remove 1 lb lead weight.
rho_ballast = 11290; %[kg/m3] density of lead to add
disp("After Removing 1 lb lead weight add Pb mass (kg):")
m_ballast_Pb = calc_ballast(Nabla_adjust - Nabla_lead_remove, 0 - m_lead_remove, rho_water, rho_ballast)

%2. Calculate mass for Fe ballast to add after removing 1 lb lead weight.
rho_ballast = 8050; %[kg/m3]  density of Fe to add
disp("After Removing 1 lb lead weight add Fe mass (kg):")
m_ballast_Fe = calc_ballast(Nabla_adjust - Nabla_lead_remove, 0 - m_lead_remove, rho_water, rho_ballast)
