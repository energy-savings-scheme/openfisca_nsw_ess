from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class ESS__PDRS__ACP_base_scheme_eligibility(Variable):
    """
        Formula to calculate the ESS PDRS Base Scheme eligibility for an ACP
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the base scheme requirements of the ESS and PDRS Schemes?'
    metadata = {
        "alias": "ESS PDRS Base Scheme Requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        energy_consumption = buildings('ESS__reduces_energy_consumption', period)
        reduce_demand = buildings('PDRS__provides_capacity_to_reduce_demand', period)
        activity_implemented = buildings('PDRS__have_implemented_PDR_activity', period)
        implementation_date = buildings('PDRS__implementation_after_1_July_2022', period)
        lawful = buildings('PDRS__is_lawful_activity', period)
        registered_ACP = buildings('ESS_registered_ACP', period)
        engaged_an_ACP = buildings('ESS_engaged_ACP', period)
        removing_or_replacing = buildings('PDRS__removing_or_replacing', period)
        not_resold_reused_refurbished = buildings('ESS__equipment_is_not_resold_reused_or_refurbished', period)
        appropriate_disposal = buildings('ESS__appropriate_disposal_of_equipment_after_15_April_2016', period)
        no_reduction_safety_levels = buildings('PDRS__reduces_safety_levels', period)
        no_increase_emissions = buildings('PDRS__greenhouse_emissions_increase', period)
        no_mandatory_requirement = buildings('PDRS__meets_mandatory_requirement', period)
        basix_affected = buildings('PDRS__basix_affected_development', period)
        not_prescribed_service = buildings('PDRS__is_prescribed_transmission_service', period)
        not_tradeable_certificates = buildings('PDRS__tradeable_certificates', period)
        replacement_hw = buildings('PDRS__replacement_water_heater_certificates', period)
        replacement_solar_hw = buildings('PDRS__replacement_solar_water_heater_certificates', period)
        
        # removing or replacing is YES and equipment is not resold, reused or refurbished and is disposed of appropriately
        removing_replacing_intermediary = removing_or_replacing + (not_resold_reused_refurbished * appropriate_disposal)

        # mandatory requirement is YES and basix affected is YES
        mandatory_allowance = np.logical_not(no_mandatory_requirement) * basix_affected
        
        # are you a registered ACP or engaged an ACP
        acp_status = registered_ACP + (np.logical_not(registered_ACP) * engaged_an_ACP)

        # tradeable certificates is YES and replacement heat pump water heater is YES and solar water heater is no
        tradeable_certificates_allowed = np.logical_not(not_tradeable_certificates) * replacement_hw * np.logical_not(replacement_solar_hw)

        end_formula =  ( energy_consumption * reduce_demand * activity_implemented * implementation_date * lawful * acp_status *
                         removing_replacing_intermediary * no_reduction_safety_levels * no_increase_emissions * mandatory_allowance *
                         not_prescribed_service * tradeable_certificates_allowed
                       )
        
        return end_formula
