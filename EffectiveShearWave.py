def EFS(Ground_Type, PGV, PGV_Red, VS, PI=20, OCR=1, Eff_Pressure=300):
    """
    Effective Shear Wave Velocity Using Darendeli (2001) and Schnabel (1973) by Berk Demir / https://github.com/berkdemir
    
    Inputs:
        Ground_Type: Either "Soil" or "Rock"
        PGV: Peak Ground Velocity (cm/sec) 
        PGV_Red: PGV reduction ratio with depth
        VS: Maximum shear wave velocity (m/s)
        PI: Plasticity index in percent. (For Soil only.)
        OCR: Overconsolidation Ratio. (For Soil only.)
        Eff_Pressure: Effective pressure (kPa) (For Soil only)
        
    Returns:
        VS_Red: Reduction ratio for maximum shear wave velocity.
    
    Notes:
        Also prints a sentence with reduction ratio and effective shear wave velocity.
        
    Example:
        For Soils: Vs_Red = EFS(Ground_Type = "Soil", PGV = 70, PGV_Red = 0.8, VS = 300, PI=20, OCR=1, Eff_Pressure=300)
        For Rocks: Vs_Red = EFS(Ground_Type = "Rock", PGV = 70, PGV_Red = 0.8, VS = 800)
    """
    
    PGV_eff = PGV * PGV_Red * 0.01  # m/s
    Shear_Modulus_Reaction = 0.7  # initial value
    VS_Red = pow(Shear_Modulus_Reaction, 0.5)

    if Ground_Type == "Soil":
        Strain_Ref = (0.0352 + 0.001 * PI * pow(OCR, 0.3246)) * \
            pow(Eff_Pressure / 100, 0.3483) / 100
        VS_Red = pow(Shear_Modulus_Reaction, 0.5)
        for i in range(0, 20):
            seismic_shear_strain = PGV_eff / (VS_Red * VS)
            Shear_Modulus_Reaction = 1 / \
                (1 + pow(seismic_shear_strain / Strain_Ref, 0.919))
            VS_Red = pow(Shear_Modulus_Reaction, 0.5)
        print("Reduction ratio of shear wave velocity is", round(VS_Red, 2), "and effective shear wave velocity is", round(
            VS*VS_Red, 0), "m/s using Darandeli (2001) G/Gmax curves for soils.")

    elif Ground_Type == "Rock":
        for i in range(0, 20):
            seismic_shear_strain = PGV_eff / (VS_Red * VS)
            Shear_Modulus_Reaction = -3.642 * \
                pow(seismic_shear_strain, 0.02553) + 3.784
            VS_Red = pow(Shear_Modulus_Reaction, 0.5)
        print("Reduction ratio of shear wave velocity is", round(VS_Red, 2), "and effective shear wave velocity is", round(
            VS*VS_Red, 0), "m/s using Schnabel (1973) G/Gmax curve for rocks.")

    return VS_Red

if __name__ == "__main__":
    VS_Red = EFS(Ground_Type, PGV, PGV_Red, VS, PI, OCR, Eff_Pressure)
    VS_eff = VS * VS_Red
