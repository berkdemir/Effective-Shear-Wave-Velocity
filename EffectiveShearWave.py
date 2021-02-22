#  Effective Shear Wave Velocity Using Darendeli (2001) and Schnabel (1973) by Berk Demir

# INPUTS
Ground_Type = "Soil"  # Either "Soil" or "Rock"
PGV = 80  # cm/sec
PGV_Red = 0.8  # PGV reduction ratio with depth
VS = 300  # Maximum shear wave velocity, m/s
PI = 20  # Plasticity index in percent. (For Soil only.)
OCR = 1  # Overconsolidation Ratio. (For Soil only.)
Eff_Pressure = 200  # Effective pressure in kPa. (For Soil only)


def EFS(Ground_Type, PGV, PGV_Red, VS, PI, OCR, Eff_Pressure):
    # CALCULATIONS
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
