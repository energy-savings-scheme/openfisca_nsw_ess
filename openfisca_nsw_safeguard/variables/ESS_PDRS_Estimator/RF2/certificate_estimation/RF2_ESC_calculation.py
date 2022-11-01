from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      af = buildings('RF2_af', period)

      input_power = (total_energy_consumption * af) / 24
      return input_power



class RF2_lifetime_by_rc_class(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    
    # if rc class is 1 - 6, 9, 10 then lifetime is 8,
    # if rc class is 7, 8, 11 and display area < 3.3 m2 then lifetime is 8
    # if rc class is 7, 8, 11 and display area > or = 3.3 m2 then lifetime is 12
    # if rc class is 12 - 15 then lifetime is 12

    
    def formula(buildings, period, parameters):

      rc_class_by_lifetime = parameters(period).PDRS.refrigerated_cabinets.table_RF2_3['refrigerated_cabinet_class']
      display_area = ____

      lifetime_by_rc_class = np.select(
      [
        rc_class_by_lifetime >= 1 * rc_class_by_lifetime <= 6,
        rc_class_by_lifetime == 8 + rc_class_by_lifetime == 9,
        (rc_class_by_lifetime == 7 + rc_class_by_lifetime == 8 + rc_class_by_lifetime == 11) * display_area < 3.3,
        (rc_class_by_lifetime == 7 + rc_class_by_lifetime == 8 + rc_class_by_lifetime == 11) * display_area >= 3.3,
        rc_class_by_lifetime >= 12 * rc_class_by_lifetime <= 15,
      ],
      [
        8,
        8,
        12,
        12
      ])

      return lifetime_by_rc_class


class RF2_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      baseline_EEI = buildings('RF2_baseline_EEI', period)
      product_EEI = buildings('RF2_product_EEI', period)
      af = buildings('RF2_af', period)
      lifetime = 4

      electricity_savings = total_energy_consumption * (baseline_EEI / product_EEI - 1) * 365 * (lifetime / 1000)
      return electricity_savings
