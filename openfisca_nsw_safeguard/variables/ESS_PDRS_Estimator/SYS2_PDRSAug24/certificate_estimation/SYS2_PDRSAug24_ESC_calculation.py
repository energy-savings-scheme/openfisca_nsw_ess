from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS2_PDRSAug24_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        "variable-type": "inter-interesting",
        "alias":"PDRS Regional Network Factor",
        "display_question": "PDRS regional network factor"
    }

    def formula(buildings, period, parameters):
        postcode = buildings('SYS2_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class SYS2_PDRSAug24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, paremeters):
        PAEC = buildings('SYS2_PDRSAug24_projected_annual_energy_consumption', period)
        PAEC_baseline = buildings('SYS2_PDRSAug24_PAEC_baseline', period)
        lifetime = 10

        deemed_electricity_savings = (PAEC_baseline - PAEC) * (lifetime / 1000)
        return deemed_electricity_savings


class SYS2_PDRSAug24_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #Nameplate input power
        nameplate_input_power = buildings('SYS2_PDRSAug24_nameplate_input_power', period)

        #PAEC
        PAEC = buildings('SYS2_PDRSAug24_projected_annual_energy_consumption', period)

        #PAEC baseline
        nameplate_input_power_to_check = np.select(
            [
                (nameplate_input_power <= 1000),
                (nameplate_input_power > 1000) * (nameplate_input_power <= 1500),
                (nameplate_input_power > 1500) * (nameplate_input_power <= 2000),
                (nameplate_input_power > 2000),
            ],
            [
                'less_than_or_equal_to_1000w',
                '1001_to_1500w',
                '1501_to_2000w',
                'greater_than_2000w'
            ])

        PAEC_baseline = parameters(period).ESS.HEER.table_D5_1_PDRSAug24.baseline_PAEC[nameplate_input_power_to_check]

        #deemed activity electricity savings
        lifetime = 10

        deemed_electricity_savings = (PAEC_baseline - PAEC) * (lifetime / 1000)

        #regional network factor
        postcode = buildings('SYS2_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        regional_network_factor = rnf.calc(postcode)

        #annual energy savings
        annual_energy_savings = deemed_electricity_savings * regional_network_factor
        
        annual_savings_return = np.select([
            annual_energy_savings <= 0, 
            annual_energy_savings > 0
        ],
        [
            0, 
            annual_energy_savings
        ])
        
        return annual_savings_return


class SYS2_PDRSAug24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('SYS2_PDRSAug24_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('SYS2_PDRSAug24_PDRS__regional_network_factor', period)

        electricity_savings = deemed_electricity_savings * regional_network_factor
        return electricity_savings


class SYS2_PDRSAug24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for SYS2'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('SYS2_PDRSAug24_electricity_savings', period) #15
        electricity_certificate_conversion_factor = 1.06

        result = (electricity_savings * electricity_certificate_conversion_factor)
               
        result_to_return = np.select([
            result <= 0,
            result > 0
        ],
        [
            0,
            result
        ])
        
        return result_to_return