CMDS = {
    'a': obd.commands.THROTTLE_POS,#
    'b': obd.commands.SPEED, #
    'c': obd.commands.RPM, #
    'd': obd.commands.ENGINE_LOAD,# %
    'e': obd.commands.FUEL_LEVEL,#
    'f': obd.commands.COOLANT_TEMP,#
    'g': obd.commands.AMBIANT_AIR_TEMP,
    'h': obd.commands.INTAKE_PRESSURE,
    'i': obd.commands.INTAKE_TEMP,
    'l': obd.commands.MAF,# gps
    'm': obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
    'n': obd.commands.BAROMETRIC_PRESSURE,
    'o': obd.commands.CONTROL_MODULE_VOLTAGE,
    'p': obd.commands.ACCELERATOR_POS_D,# % throttle
    'q': obd.commands.ACCELERATOR_POS_E,# % throttle
    'r': obd.commands.THROTTLE_ACTUATOR, # %
    's': obd.commands.OIL_TEMP,
    #'v': obd.commands.RELATIVE_THROTTLE_POS,#
    #obd.commands.ACCELERATOR_POS_F,
    #obd.commands.FUEL_RATE,
    #obd.commands.ABSOLUTE_LOAD,
    #obd.commands.COMMANDED_EQUIV_RATIO,
    #obd.commands.THROTTLE_POS_B,
    #obd.commands.THROTTLE_POS_C,
    #obd.commands.COMMANDED_EGR,
    #obd.commands.FUEL_RAIL_PRESSURE_VAC,
    #obd.commands.FUEL_PRESSURE,
    #obd.commands.TIMING_ADVANCE,
}