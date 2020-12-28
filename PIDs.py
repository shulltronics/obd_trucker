def calc_BAR(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return (((A*256) + B) * 0.03625)

def calc_MAP(v):
    return calc_BAR(v)

def calc_EBP(v):
    return calc_BAR(v)

def calc_EOT(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return ((((A*256) + B) / 100) - 40)

def calc_IPW(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return (((A*256) + B) * 0.008)

def calc_ICP(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return (((A*256) + B) * 0.57)

def calc_IPR(v):
    if (len(v) != 1):
        return 0
    else:
        A = int(v[0], 16)
        return (A*0.39063)

def calc_MFD(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return (((A*256)+B)*0.0625)

# v is a list of bytes (raw receipt from PCM)
def calc_TFT(v):
    if (len(v) != 2):
        return 0
    else:
        A = int(v[0], 16)
        B = int(v[1], 16)
        return ((((A*256) + B) * (-0.0036)) + 212.98)

columns =   ("Name"                          , "Abr", "PID"   , "Units", "Max", "Min", "Formula")

PIDs =    [ ("Barometer"                     , "BAR", 0x221442, "PSI"      ,  15   , 10   ,  calc_BAR),
            ("Manifold Absolute Pressure"    , "MAP", 0x221440, "PSI"      ,  45   ,  0   ,  calc_MAP),
            ("Exhaust Back Pressure"         , "EBP", 0x221445, "PSI"      ,  55   ,  0   ,  calc_EBP),
            ("Engine Oil Temperature"        , "EOT", 0x221310, "C"        , 250   ,  0   ,  calc_EOT),
            ("Injector Pulse Width"          , "IPW", 0x221310, "ms"       ,   6   ,  0   ,  calc_IPW),
            ("Injector Control Pressure"     , "ICP", 0x221446, "PSI"      , 3000  ,  0   ,  calc_ICP),
            ("Injector Pressure Regulator"   , "IPR", 0x221434, "%"        ,  100  ,  0   ,  calc_IPR),
            ("Mass Fuel Desired"             , "MFD", 0x221412, "mg/stroke", 100   ,  0   ,  calc_MFD),
            ("Transmission Fluid Temperature", "TFT", 0x2211BD, "F"        , 250   ,  0   ,  calc_TFT)
          ]
