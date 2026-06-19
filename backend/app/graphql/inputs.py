import strawberry
from typing import List, Optional

@strawberry.input
class PokemonCreationInput:
    name: str
    national_dex_number: int
    generation_name: str
    types: List[str]
    tags: List[str]


@strawberry.input
class CardCreationInput:
    name: str
    number: int
    rarity: str
    type: str
    set_id: int
    image_path: str = ""
    pokemon_ids: List[int] = strawberry.field(default_factory=list)


@strawberry.input
class AbstractBoosterCreationInput:
    set: str
    set_card_count: int
    energy_card_count: int = 0
    special_card_count: int = 0


@strawberry.input
class BoosterCreationInput:
    abstract_booster_id: int
    pokemon_names: List[str] = strawberry.field(default_factory=list)
    name: Optional[str] = None


@strawberry.input
class PokemonFilter:
    name_regex: Optional[str] = None
    number: Optional[int] = None
    types: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    generations: Optional[List[int]] = None


@strawberry.input
class SetFilter:
    name_regex: Optional[str] = None
    era_id: Optional[int] = None
    abbreviation: Optional[str] = None
    year: Optional[int] = None


@strawberry.input
class CardFilter:
    name_regex: Optional[str] = None
    rarity: Optional[List[str]] = None
    set_id: Optional[int] = None
    pokemon_id: Optional[int] = None
