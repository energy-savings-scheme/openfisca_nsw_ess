from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

import numpy as np

class ESS_HEAB_install_sensor_based_blowdown_on_gas_boiler_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F13?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        operating_pressure = buildings('ESS_HEAB_steam_boiler_new_equipment_operating_pressure', period)
        bars_of_pressure = np.select(
                                [
                                        operating_pressure < 8,
                                        (operating_pressure >= 8) * (operating_pressure < 10),
                                        (operating_pressure >= 10) * (operating_pressure < 12),
                                        (operating_pressure >= 12) * (operating_pressure < 15),
                                        operating_pressure > 15
                                   ],
                                  [
                                        'under_eight_bars',
                                        'eight_bars',
                                        'ten_bars',
                                        'twelve_bars',
                                        'fifteen_bars'
                                   ]
                                   )
        # note that if less than 8 bars, use 8 bars. if between a tier of bars \
        # (i.e. 9.5 bars) use the lower bar.
        default_efficiency_improvement = parameters(period).ESS.HEAB.table_F13_1.default_efficiency_improvement[bars_of_pressure]
        load_utilisation_factor = parameters(period).ESS.HEAB.table_F13_2.load_utilisation_factor
        lifetime = parameters(period).ESS.HEAB.table_F13_3.lifetime
        hours_in_year = parameters(period).ESS.ESS_related_constants.hours_in_year
        return (
                current_capacity * 
                default_efficiency_improvement * 
                load_utilisation_factor * 
                lifetime * 
                hours_in_year / 
                1000
                )
        # need to make the burner replacement age calc more efficient