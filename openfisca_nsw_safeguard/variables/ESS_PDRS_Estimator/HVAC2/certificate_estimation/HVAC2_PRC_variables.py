from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


""" Parameters for HVAC2 PRC Calculation
"""

""" Values shared with ESC variables HVAC2_ESC_variables 
    HVAC2_cooling_capacity_input
    HVAC2_baseline_AEER_input
"""

""" These variables use GEMS Registry data
"""
class HVAC2_input_power(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "display_question": "What is the input power of your commercial air conditioner?"
    }


class HVAC2_DNSP_Options(Enum):
    Endeavour = 'Endeavour'
    Essential = 'Essential'
    Ausgrid = 'Ausgrid'


class HVAC2_DNSP(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_DNSP_Options
    default_value = HVAC2_DNSP_Options.Ausgrid
    definition_period = ETERNITY
    label = "What Distribution District does the Implementation take place in?"
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Distribution District",
        "display_question": "Who is your network service provider?"
    }


class HVAC2_network_loss_factor(Variable):
    reference = 'table_A3_network_loss_factors'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        distribution_district = buildings('HVAC2_DNSP', period)
        network_loss_factor = parameters(period).PDRS.table_A3_network_loss_factors['network_loss_factor'][distribution_district]
        return network_loss_factor
    

class HVAC2_New_Equipment(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    label = 'New or Used equipment'
    metadata = {
        "variable-type": "user-input",
        "display_question": "Is the end-user equipment a new air-conditioner?"
        }
