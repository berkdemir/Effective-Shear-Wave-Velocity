"""
Seismic Deformations for Plaxis by Berk Demir / https://github.com/berkdemir
Locate this file in <PLAXIS installation folder>\pytools\input and call it from Plaxis - Expert - Run Python tool
"""


import easygui
from plxscripting.easy import *
# If script is used OUTSIDE of Plaxis.
"""
localhostport_i = 10000
password = "262314bd"
s_i, g_i = new_server("localhost", localhostport_i, password=password)
"""
# If we use the script as a Plaxis tool.

s_i, g_i = new_server()


def get_borehole_layers(borehole):
    """ reads the borehole information to collect soillayer thickness
        information and returns a dictionary per layer top-down """
    borehole_layers = []
    for soillayer in g_i.Soillayers:
        for zone in soillayer.Zones:
            if (zone.Borehole.value) == borehole:
                borehole_layers.append({"name": soillayer.Name.value,
                                        "top": zone.Top.value,
                                        "bottom": zone.Bottom.value,
                                        "thickness": zone.Thickness.value
                                        }
                                       )
    return borehole_layers

def get_xmin_xmax():
    """ gets the xmax and xmin of the model."""
    point_list = []
    
    for i in g_i.SoilContour:
        point_list.append(i)
    
    xmin = point_list[0].x.value
    xmax = point_list[1].x.value
    return xmin, xmax


bh = g_i.Boreholes[0]

borehole_layers = get_borehole_layers(bh)

top = borehole_layers[0]["top"]
bottom = borehole_layers[-1]["bottom"]
depth = top-bottom


title = "Seismic Deformation Application by Berk Demir"
msg = "Please enter seismic parameters."
fieldNames = [
    "Peak Ground Velocity (cm/sec)",
    "Reduction in PGV due to depth",
    "Maximum Shear Wave Velocity (m/s)",
    "Ratio of Effective to Maximum Shear Wave Velocity"
    ]

fieldValues = easygui.multenterbox(msg, title, fieldNames)

def_choice = ["Triangular","Z-Shape"]

select_def_type = easygui.buttonbox("Select deformation type", "Seismic Deformation Type", def_choice)


PGV, PGV_Red, VS, VS_Red = [float(item) for item in fieldValues]

xmin, xmax = get_xmin_xmax()

strain = PGV * PGV_Red * 0.01 / (VS*VS_Red)

if select_def_type == "Triangular":
    deformation = strain * depth
    LD_Left = g_i.linedispl((xmin,top),(xmin,bottom))[-1]
    LD_Right = g_i.linedispl((xmax,top),(xmax,bottom))[-1]
    LD_Top = g_i.linedispl((xmin,top),(xmax,top))[-1]
    LD_Left.setproperties("Displacement_x","Prescribed","Displacement_y","Free","Distribution","Linear","ux_start",deformation,"ux_end",0)
    LD_Right.setproperties("Displacement_x","Prescribed","Displacement_y","Free","Distribution","Linear","ux_start",deformation,"ux_end",0)
    LD_Top.setproperties("Displacement_x","Prescribed","Displacement_y","Fixed","Distribution","Uniform","ux_start",deformation)
    
elif select_def_type == "Z-Shape":
    deformation = strain * depth * 0.5
    LD_Left = g_i.linedispl((xmin,top),(xmin,bottom))[-1]
    LD_Right = g_i.linedispl((xmax,top),(xmax,bottom))[-1]
    LD_Top = g_i.linedispl((xmin,top),(xmax,top))[-1]
    LD_Bottom = g_i.linedispl((xmin,bottom),(xmax,bottom))[-1]
    LD_Left.setproperties("Displacement_x","Prescribed","Displacement_y","Free","Distribution","Linear","ux_start",deformation,"ux_end",-deformation)
    LD_Right.setproperties("Displacement_x","Prescribed","Displacement_y","Free","Distribution","Linear","ux_start",deformation,"ux_end",-deformation)
    LD_Top.setproperties("Displacement_x","Prescribed","Displacement_y","Fixed","Distribution","Uniform","ux_start",deformation)
    LD_Bottom.setproperties("Displacement_x","Prescribed","Displacement_y","Fixed","Distribution","Uniform","ux_start",-deformation)
    




