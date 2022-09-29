import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

# detailed in PDRS activity XX

class PDRS_HVAC_1_replace_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC replace meets eligibility requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_replace", "eligibility"]
    }


class PDRS_HVAC_1_replace_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Equipment' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC replace meets equipment requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_replace", "equipment"]
    }

    def formula(buildings, period, parameters):
        is_in_GEM = buildings(
            'Appliance_is_registered_in_GEMS', period)
        exceeds_benchmark = buildings(
            'PDRS_HVAC_1_TCSPF_or_AEER_exceeds_benchmark', period)

        return is_in_GEM * exceeds_benchmark


class PDRS_HVAC_1_replace_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC replace meets implementation requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_replace", "implementation"]
    }

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Equipment_is_installed', period)
        is_removed = buildings("Equipment_is_removed", period)
        performed_by_qualified_person = buildings(
            'Implementation_is_performed_by_qualified_person', period)

        return is_installed * is_removed * performed_by_qualified_person


class PDRS_HVAC_1_replace_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC replace meets all requirements",
    }

    def formula(buildings, period, parameters):
        eligibility = buildings(
            'PDRS_HVAC_1_replace_meets_eligibility_requirements', period)
        equipment = buildings(
            'PDRS_HVAC_1_replace_meets_equipment_requirements', period)
        implementation = buildings(
            'PDRS_HVAC_1_replace_meets_implementation_requirements', period)

        return implementation * eligibility * equipment
