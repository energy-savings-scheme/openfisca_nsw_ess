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
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated cooling input power (kW)'
    metadata = {
        'display_question': 'Rated cooling input power at 35C as recorded in the GEMS registry',
        'sorting' : 9,
        'label': 'Rated cooling input power (kW)'
    }


class HVAC2_DNSP_Options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


class HVAC2_DNSP(Variable):
     # this variable is used as the second input on all estimator certificate calculation pages
    value_type = Enum
    entity = Building
    possible_values = HVAC2_DNSP_Options
    default_value = HVAC2_DNSP_Options.Ausgrid
    definition_period = ETERNITY
    label = "Distribution Network Service Provider"
    metadata = {
        'variable-type': 'user-input',
        'display_question': 'Who is your Distribution Network Service Provider?',
        'sorting' : 2,
        'label': "Distribution Network Service Provider"
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
        'variable-type': 'user-input',
        'display_question': 'Is the End-User equipment a new air-conditioner?',
        'sorting' : 3,
        'label': 'New or Used equipment'
        }