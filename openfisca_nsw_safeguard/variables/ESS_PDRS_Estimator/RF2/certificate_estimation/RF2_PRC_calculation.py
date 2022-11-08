from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      af = buildings('RF2_af', period)
      baseline_EEI = buildings('RF2_baseline_EEI', period)
      product_EEI = buildings('RF2_product_EEI', period)

      baseline_input_power = (total_energy_consumption * af) * (baseline_EEI / product_EEI) / 24
      return baseline_input_power
  
  
class RF2_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      baseline_peak_asjustment_factor = buildings('RF2_baseline_peak_adjustment_factor', period)
      baseline_input_power = buildings('RF2_baseline_input_power', period)
      input_power = buildings('RF2_input_power', period)
      firmness_factor = 1

      peak_demand_savings_capacity= ((baseline_peak_asjustment_factor * baseline_input_power)
                                        - (input_power * baseline_peak_asjustment_factor )) * firmness_factor
      return peak_demand_savings_capacity
  
  
class RF2_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF2_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = buildings('RF2_lifetime_by_rc_class', period)

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime


class RF2_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Adjustment Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      product_type = buildings('RF2_product_type', period)
      duty_type = buildings('RF2_duty_class', period)
      usage_factor = 1
      
      temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2['temperature_factor'][product_type][duty_type]

      baseline_peak_adjustment_factor = temperature_factor * usage_factor
      return baseline_peak_adjustment_factor
  
  
  
class RF2_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 PRC calculation'
    metadata = {
        'variable-type': 'output'
    }
    
    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('RF2_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF2_network_loss_factor', period) 
        
        result = (peak_demand_reduction_capacity * network_loss_factor * 10)
        
        result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])
        
        return result_to_return
