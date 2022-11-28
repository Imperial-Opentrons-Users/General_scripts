from opentrons.simulate import simulate, format_runlog

# read the file
protocol_file = open("//icnas1.cc.ic.ac.uk/ljh119/GitHub/opentrons_scripts/TC_transformation.py")
# simulate() the protocol, keeping the runlog
runlog, _bundle = simulate(protocol_file, "//icnas1.cc.ic.ac.uk/ljh119/GitHub/opentrons_scripts/TC_transformation.py")
# print the runlog
print('\n', format_runlog(runlog), '\n', sep = '')
