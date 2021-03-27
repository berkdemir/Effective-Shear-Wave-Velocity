## Effective Shear Wave Velocity Calculation
### Berk Demir - bdberkdemir [at] gmail.com
This code will calculate effective shear wave velocity using iterative approach to determine the reduction in shear wave velocity based on the modulus reduction ratio curves by Darendeli (2001) and Schnabel (1973).

Iteration is based on the following approach. (Demir, 2021 - submitted to Harding Prize)
 - Calculate seismic shear strain using reduced PGV based on the depth of tunnel and maximum shear wave velocity.
 - Ignoring any static strain, calculate the G/Gmax based on either one of the presented approaches.
 - Calculate shear modulus reduction ratio as square root of the G/Gmax.
 - Using the calculated ratio, calculate effective shear wave velocity.
 - Calculate new seismic shear strain using reduced PGV and new effective shear wave velocity.
 - Continue until reasonable difference is obtained between Vsi+1 and Vsi.

### References
Darendeli, M.B., 2001. Development of a new family of normalized modulus reduction and material damping curves.
Schnabel, P.B., 1973. Effects of local geology and distance from source on earthquake ground motions. University of California, Berkeley.
