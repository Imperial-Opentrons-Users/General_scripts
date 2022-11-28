from opentrons import protocol_api, simulate
import opentrons, time, re

metadata = {'apiLevel': '2.10'}

def counter(rows):
    def inner(n):
        """ Takes a number 'n' between 0 and 95, representing the nth tip in the box.
            Returns a well in the form 'A1'."""
        
        row_dict = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        inv_row_dict = {v: k for k, v in row_dict.items()}

        if type(n) == int:
            row = row_dict[n % rows]
            col = 1 + n // rows
            return row + str(col)

        elif type(n) == str:
            row, col = re.findall('\d+|\D+', n)
            col = int(col) - 1

            return col*rows + inv_row_dict[row]

    return inner

tip_counter = counter(8)
print(tip_counter('A11'))

def run(protocol: protocol_api.ProtocolContext):

    ##################
    #### Hardware ####
    ##################

    # Pipettes
    # left = protocol.load_instrument('p300_multi_gen2', 'left')
    
    right = protocol.load_instrument('p20_single_gen2', 'right')

    # Tipracks
    tiprack20_source = protocol.load_labware('opentrons_96_tiprack_20ul', 2)
    tiprack20_1_count = 0
    
    tiprack20_dest = protocol.load_labware('opentrons_96_tiprack_20ul', 3)
    tiprack20_1_count = 0
    
    tiprack300_source = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
    tiprack300_1_count = 0

    tiprack300_dest = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
    tiprack300_1_count = 0

    ###################
    #### Functions ####
    ###################

    def flash():
        ''' Flashes light three times. Intended to prompt user input.'''

        for i in range(4):
            protocol.set_rail_lights(False)
            time.sleep(0.15)
            protocol.set_rail_lights(True)
            time.sleep(0.15)

    def single_restock(pipette, source_rack, dest_rack):
        def single_restock_inner(source_well, dest_well):
            ''' Transfers tips from one tip box to another using a single channel pipette, to refill and consolidate tip boxes. '''
            source_tip_well = tip_counter(source_well)
            avbl_tips = 96 - source_tip_well
            req_tips = tip_counter(dest_well)

            if avbl_tips >= req_tips:
                for i in range(req_tips):
                    pipette.pick_up_tip(source_rack[tip_counter(source_tip_well + i)])
                    pipette.drop_tip(dest_rack[tip_counter(req_tips - 1 - i)])
            else:
                for i in range(avbl_tips):
                    pipette.pick_up_tip(source_rack[tip_counter(source_tip_well + i)])
                    pipette.drop_tip(dest_rack[tip_counter(req_tips - 1 - i)])
    
        return single_restock_inner

    p20_restock = single_restock(right, tiprack20_source, tiprack20_dest)       # single channel p20 restock function
    # p300_restock = single_restock(right, tiprack300_source, tiprack300_dest)  # this would be the function if you had a single channel p300 to use

    # def multi_restock(pipette, source_rack, dest_rack):
    #     def multi_restock_inner(source_well, dest_well, reverse_direction = True):
    #         ''' Transfers tips from one tip box to another using a multi channel pipette, to refill and consolidate tip boxes. 
    #             Assumes tips have been used up by a multichannel in reverse but can also handle tip boxes emptied in the forwards direction. '''
    #         source_tip_well = tip_counter(source_well)
    #         avbl_tips = 96 - source_tip_well
    #         req_tips = tip_counter(dest_well)

    ##################
    #### Protocol ####
    ##################

    protocol.set_rail_lights(True)

    p20_restock('G8', 'A3')

    flash()

    protocol.set_rail_lights(False)
