from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class BESS1_V5Nov24_demand_shifting_component(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Demand shifting component kW'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        usable_battery_capacity = buildings('BESS1_V5Nov24_usable_battery_capacity', period)
        demand_reduction_factor = 0.0853

        demand_shifting_component = usable_battery_capacity * demand_reduction_factor
        return demand_shifting_component
    

class BESS1_V5Nov24_peak_demand_shifting_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand shifting capacity kW'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        demand_shifting_component = buildings('BESS1_V5Nov24_demand_shifting_component', period)
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['BESS1']

        peak_demand_shifting_capacity = demand_shifting_component * firmness_factor
        return peak_demand_shifting_capacity


class BESS1_V5Nov24_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):    
        #usable battery capacity
        usable_battery_capacity = buildings('BESS1_V5Nov24_usable_battery_capacity', period)

        #demand shifting component
        demand_reduction_factor = 0.0853

        demand_shifting_component = usable_battery_capacity * demand_reduction_factor
        
        #peak demand shifting capacity
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['BESS1']

        peak_demand_shifting_capacity = demand_shifting_component * firmness_factor
        
        #peak demand annual savings
        summer_peak_demand_duration = 6

        #lifetime
        lifetime = 15

        peak_demand_annual_savings = peak_demand_shifting_capacity * summer_peak_demand_duration * lifetime

        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ],
            [
                0, peak_demand_annual_savings
            ])
        
        
        return peak_demand_annual_savings_return


class BESS1_V5Nov24_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity kW'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
       peak_demand_shifting_capacity = buildings('BESS1_V5Nov24_peak_demand_shifting_capacity', period)
       summer_peak_demand_reduction_duration = 6
       lifetime = 15

       peak_demand_reduction_capacity = peak_demand_shifting_capacity * summer_peak_demand_reduction_duration * lifetime
       return peak_demand_reduction_capacity


class BESS1_V5Nov24_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'BESS1 PRC calculation'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('BESS1_V5Nov24_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('BESS1_V5Nov24_get_network_loss_factor_by_postcode', period)
        installation_eligibility = buildings('BESS1_V5Nov24_installation_activity', period)

        BESS1_eligible_PRCs = np.select(
            [
                installation_eligibility,
                np.logical_not(installation_eligibility)
            ],
            [
                (peak_demand_reduction_capacity * network_loss_factor * 10),
                0
            ])

        result_to_return = np.select(
            [
                BESS1_eligible_PRCs <= 0, 
                BESS1_eligible_PRCs > 0
            ],
            [
                0, 
                BESS1_eligible_PRCs
            ])
        return result_to_return

