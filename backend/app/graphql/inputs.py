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