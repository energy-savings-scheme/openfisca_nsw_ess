from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class PDRS__is_eligible_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is An Eligible Activity",
    }

    def formula(buildings, period, parameters):
        provides_capacity_to_reduce_demand = buildings('PDRS__provides_capacity_to_reduce_demand', period)
        is_eligible_for_PDRS_creation = buildings('PDRS__is_eligible_for_PDRS_creation', period)
        is_in_PDRS_jurisdiction = buildings('PDRS__is_in_PDRS_jurisdiction', period)
        is_unlawful_activity = buildings('PDRS__is_unlawful_activity', period)
        greenhouse_emissions_increase = buildings('PDRS__greenhouse_emissions_increase', period)
        activity_meets_mandatory_requirement = buildings('PDRS__meets_mandatory_requirement', period)
        is_standard_control_service = buildings('PDRS__is_standard_control_service', period)
        is_prescribed_transmission_service = buildings('PDRS__is_prescribed_transmission_service', period)
        is_non_network_option = buildings('PDRS__is_non_network_option', period)
        reduces_safety_levels = buildings('PDRS__reduces_safety_levels', period)
        is_eligible_for_RET = buildings('PDRS__is_eligible_for_RET', period)
        tradeable_certificates = buildings('PDRS__tradeable_certificates', period)


        is_eligible_peak_demand_reduction_activity = (
        provides_capacity_to_reduce_demand * 
        is_eligible_for_PDRS_creation *
        is_in_PDRS_jurisdiction *
        (np.logical_not(is_unlawful_activity))        
        )

        is_not_eligible_peak_demand_reduction_activity = (
        (greenhouse_emissions_increase) +
        (activity_meets_mandatory_requirement)
        +
        (is_standard_control_service
        + is_prescribed_transmission_service
        * (np.logical_not(is_non_network_option))
        )
        + reduces_safety_levels
        + is_eligible_for_RET
        + tradeable_certificates
        )

        is_eligible = (
          is_eligible_peak_demand_reduction_activity *
          (np.logical_not(is_not_eligible_peak_demand_reduction_activity))
        )
        return is_eligible


class PDRS__provides_capacity_to_reduce_demand(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity provide the capacity to reduce demand?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity Reduces Demand",
        'display_question': "Does your activity provide capacity to reduce demand during the Peak Demand Reduction period?"
    }


class PDRS__is_eligible_for_PDRS_creation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible for creation?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible for PDRS Creation",
    }


class PDRS__is_in_PDRS_jurisdiction(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity occur within the PDRS jurisdiction?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity is in Jurisdiction",
    }


class PDRS__is_unlawful_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity unlawful to conduct?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Unlawful Activity",
        'display_question': "Was your activity lawful in NSW on the implementation date?"
    }


class PDRS__greenhouse_emissions_increase(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in an increase in emissions?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity Increases Emissions",
        'display_question': "Will your activity lead to a net increase in greenhouse emissions?"
    }


class PDRS__meets_mandatory_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity conducted to meet mandatory requirements of...?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity Meets Mandatory Requirements",
        'display_question': "Is your activity being undertaken to comply with any mandatory legal requirements?"
    }


class PDRS__is_standard_control_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a Standard Control Service?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity is Standard Control Service",
    }


class PDRS__is_prescribed_transmission_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a Prescribed Transmission Service?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Activity is Prescribed Transmission Service",
        'display_question': "Is your activity a Standard Control Service or Prescribed Transmission service undertaken by a Network Service Provider?"
    }


class PDRS__is_non_network_option(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a Non-Network Option?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Non-Network Option",
    }


class PDRS__reduces_safety_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction in safety levels?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Reduces Safety Levels",
        'display_question' : "Will your activity reduce safety levels or permanently reduce production or service levels?"
    }


class PDRS__is_eligible_for_RET(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible to generate activities within the RET?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Eligible for RET",
    }

class PDRS__tradeable_certificates(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have you created tradeable certificates'
    metadata = {
        'display_question' : 'Have you created tradeable certificates under the Renewable Energy Act?'
    }


class PDRS__residential_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have you created tradeable certificates'
    metadata = {
        'display_question' : 'Has the new End-User equipment been installed in a residential building?'
    }