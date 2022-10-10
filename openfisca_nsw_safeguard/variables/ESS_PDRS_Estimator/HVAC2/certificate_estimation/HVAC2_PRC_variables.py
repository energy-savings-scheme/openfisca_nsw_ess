import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for HVAC2 PRC Calculation
"""

""" Values shared with ESC variables HVAC2_ESC_variables 
    HVAC2_cooling_capacity_input
    HVAC2_baseline_AEER_input
    HVAC2_lifetime_value
"""

""" These variables use GEMS Registry data
"""
class HVAC2_input_power(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY


""" These variables use Rule tables
"""
class HVAC2_firmness_factor(Variable):
    reference = 'PDRS_table_A6'
    value_type = float
    entity = Building
    definition_period = ETERNITY


class HVAC2_network_loss_factor(Variable):
    reference = 'PDRS_table_A3'
    value_type = float
    entity = Building
    definition_period = ETERNITY