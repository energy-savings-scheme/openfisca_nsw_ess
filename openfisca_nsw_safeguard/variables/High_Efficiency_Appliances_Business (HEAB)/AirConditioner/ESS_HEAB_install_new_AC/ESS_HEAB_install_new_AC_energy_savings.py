from openfisca_core.entities import entity
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

import numpy as np


class ESS_HEAB_install_or_replace_AC_energy_savings(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings created by Activity Definition F4?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings(
            'ESS_HEAB_install_or_replace_AC_electricity_savings', period)
        meets_all_requirements = buildings(
            'ESS_HEAB_residential_AC_install_meets_all_requirements', period)
        return electricity_savings * meets_all_requirements


class ESS_HEAB_install_or_replace_AC_electricity_savings(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings created by Activity Definition F4?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        reference_cooling_annual_energy_use = buildings(
            'ESS_HEAB_install_or_replace_AC_reference_cooling_annual_energy_use', period)
        cooling_annual_energy_use = buildings(
            'ESS_HEAB_install_or_replace_AC_cooling_annual_energy_use', period)
        reference_heating_annual_energy_use = buildings(
            'ESS_HEAB_install_or_replace_AC_reference_heating_annual_energy_use', period)
        heating_annual_energy_use = buildings(
            'ESS_HEAB_install_or_replace_AC_heating_annual_energy_use', period)

        lifetime = parameters(period).ESS.HEAB.table_F4_6.lifetime

        electricity_savings = (
            (
                reference_cooling_annual_energy_use -
                cooling_annual_energy_use
            ) +
            (
                reference_heating_annual_energy_use -
                heating_annual_energy_use
            ) *
            lifetime / 
            1000
        )

        return electricity_savings


class ESS_HEAB_install_or_replace_AC_reference_cooling_annual_energy_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Reference Annual Cooling Use?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        AC_climate_zone = buildings('AC_climate_zone', period)
        activity_type = buildings('PDRS_activity_type', period)
        ActivityType = activity_type.possible_values
        equivalent_cooling_hours = parameters(period).ESS.HEAB.table_F4_1.cooling_hours[AC_climate_zone]
        baseline_rated_AEER = np.where([
            activity_type == ActivityType.install_AC,
            activity_type == ActivityType.replace_AC,
            (
                np.logical_not(activity_type == ActivityType.install_AC) +
                np.logical_not(activity_type == ActivityType.replace_AC)
            )
            ],
            [
                parameters(period).ESS.HEAB.table_F4_2.AEER,
                parameters(period).ESS.HEAB.table_F4_3.AEER,
                0
            ]
            )

        return(
            cooling_capacity *
            equivalent_cooling_hours / 
            baseline_rated_AEER
        )


class ESS_HEAB_install_or_replace_AC_reference_heating_annual_energy_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Reference Annual Cooling Use?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        heating_capacity = buildings('new_AC_heating_capacity', period)
        AC_climate_zone = buildings('AC_climate_zone', period)
        activity_type = buildings('PDRS_activity_type', period)
        ActivityType = activity_type.possible_values
        equivalent_heating_hours = parameters(period).ESS.HEAB.table_F4_1.heating_hours[AC_climate_zone]
        baseline_rated_ACOP = np.where([
            activity_type == ActivityType.install_AC,
            activity_type == ActivityType.replace_AC,
            (
                np.logical_not(activity_type == ActivityType.install_AC) +
                np.logical_not(activity_type == ActivityType.replace_AC)
            )
            ],
            [
                parameters(period).ESS.HEAB.table_F4_2.ACOP,
                parameters(period).ESS.HEAB.table_F4_3.ACOP,
                0
            ]
            )

        return(
            heating_capacity *
            equivalent_heating_hours / 
            baseline_rated_ACOP
        )


class ESS_HEAB_install_or_replace_AC_cooling_annual_energy_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Reference Annual Cooling Use?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        AC_climate_zone = buildings('AC_climate_zone', period)
        equivalent_cooling_hours = parameters(period).ESS.HEAB.table_F4_1.cooling_hours[AC_climate_zone]
        new_rated_AEER = buildings('AC_AEER', period)
        return(
            cooling_capacity *
            equivalent_cooling_hours / 
            new_rated_AEER
        )

class ESS_HEAB_install_or_replace_AC_heating_annual_energy_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Reference Annual Cooling Use?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        heating_capacity = buildings('new_AC_heating_capacity', period)
        AC_climate_zone = buildings('AC_climate_zone', period)
        equivalent_heating_hours = parameters(period).ESS.HEAB.table_F4_1.heating_hours[AC_climate_zone]
        new_rated_ACOP = buildings('AC_ACOP', period)
        return(
            heating_capacity *
            equivalent_heating_hours / 
            new_rated_ACOP
        )

