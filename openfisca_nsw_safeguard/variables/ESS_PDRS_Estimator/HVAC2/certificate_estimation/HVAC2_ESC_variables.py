from importlib.metadata import metadata
import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for HVAC2 ESC Calculation
    These variables use GEMS Registry data
"""
class HVAC2_heating_capacity_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY


class HVAC2_rated_ACOP_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY


class HVAC2_cooling_capacity_input(Variable):
    reference = 'unit in kw'
    value_type = float
    entity = Building
    definition_period = ETERNITY


class HVAC2_rated_AEER_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY


""" These variables use Rule tables
"""
class HVAC2_equivalent_heating_hours_input(Variable):
    reference = 'table_F4.1'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    
    metadata = {
        "variable-type": "inter-interesting"
    }


class HVAC2_equivalent_cooling_hours_input(Variable):
    reference = 'table_F4.1'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        "variable-type": "inter-interesting"
    }



class HVAC2_baseline_ACOP_input(Variable):
    reference = 'table_F4.3'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        "variable-type": "inter-interesting"
    }



class HVAC2_baseline_AEER_input(Variable):
    reference = 'table_F4.3'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        "variable-type": "inter-interesting"
    }


class HVAC2_lifetime_value(Variable):
    # description = 'ESS_D16_lifetime'
    reference = 'unit in years'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }
