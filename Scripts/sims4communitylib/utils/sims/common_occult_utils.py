"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.common_trait_utils import CommonTraitUtils


class CommonOccultUtils:
    """ Utilities for handling sim occults. """

    @staticmethod
    def get_sim_info_of_all_occults_gen(sim_info: Union[SimInfo, SimInfoBaseWrapper], *exclude_occult_types: OccultType) -> Iterator[Union[SimInfo, SimInfoBaseWrapper]]:
        """
            Retrieve a generator of SimInfo objects for all Occults of a sim.

            Note: Results include the sim_info specified.
        """
        if sim_info is None:
            return tuple()
        yield sim_info
        occults = (OccultType.HUMAN, OccultType.ALIEN, OccultType.VAMPIRE, OccultType.MERMAID, OccultType.WITCH)
        for occult in occults:
            if occult in exclude_occult_types:
                continue
            if occult == sim_info.current_occult_types:
                continue
            if not sim_info.occult_tracker.has_occult_type(occult):
                continue
            occult_sim_info: SimInfo = sim_info.occult_tracker.get_occult_sim_info(occult)
            if occult_sim_info is None:
                continue
            yield occult_sim_info

    @staticmethod
    def is_vampire(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Vampire.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE)

    @staticmethod
    def is_alien(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is an Alien.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN)

    @staticmethod
    def is_plant_sim(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Plant Sim.
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM)

    @staticmethod
    def is_ghost(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Ghost.
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            is_ghost_trait = getattr(trait, 'is_ghost_trait', None)
            if is_ghost_trait:
                return True
        return False

    @staticmethod
    def is_mermaid(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Mermaid
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID)

    @staticmethod
    def is_in_mermaid_form(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is in Mermaid Form (Their Tail is visible).
        """
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID_MERMAID_FORM)

    @staticmethod
    def is_mermaid_in_mermaid_form(sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """
            Determine if a sim is a Mermaid and is in Mermaid Form (Their Tail is visible).
        """
        return CommonOccultUtils.is_mermaid(sim_info) and CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def _has_occult_trait(sim_info: Union[SimInfo, SimInfoBaseWrapper], trait: int) -> bool:
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for sim_trait in equipped_sim_traits:
            sim_trait_id = getattr(sim_trait, 'guid64', None)
            if sim_trait_id == trait:
                return True
        return False