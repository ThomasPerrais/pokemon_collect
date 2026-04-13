from app.db.models import Pokemon, PokemonType, PokemonTag, Set, Card
from sqlalchemy.sql import Select
from sqlalchemy import and_
from app.db.schemas import PokemonFilterParams, SetFilterParams, CardFilterParams


def apply_pokemon_filters(stmt: Select, filters: PokemonFilterParams) -> Select:
    conditions = []
    if filters.name_regex:
        conditions.append(Pokemon.name.like(f"%{filters.name_regex}%"))
    if filters.number:
        conditions.append(Pokemon.national_dex_number == filters.number)
    if filters.types:
        for type_name in filters.types:
            conditions.append(Pokemon.types.any(PokemonType.name == type_name))
    if filters.tags:
        for tag_name in filters.tags:
            conditions.append(Pokemon.tags.any(PokemonTag.name == tag_name))
    if filters.generations:
        conditions.append(Pokemon.generation_id.in_(filters.generations))

    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.distinct()
    return stmt


def apply_set_filters(stmt: Select, filters: SetFilterParams) -> Select:
    conditions = []
    if filters.name_regex:
        conditions.append(Set.name.like(f"%{filters.name_regex}%"))
    if filters.era_id:
        conditions.append(Set.era_id == filters.era_id)
    if filters.abbreviation:
        conditions.append(Set.abbreviation == filters.abbreviation)
    if filters.year:
        conditions.append(Set.release_date.year == filters.year)

    if conditions:
        stmt = stmt.where(and_(*conditions))
    return stmt.distinct()


def apply_card_filters(stmt: Select, filters: CardFilterParams) -> Select:
    conditions = []
    if filters.name_regex:
        conditions.append(Card.name.like(f"%{filters.name_regex}%"))
    if filters.rarity:
        conditions.append(Card.rarity.in_(filters.rarity))
    if filters.set_id:
        conditions.append(Card.set_id == filters.set_id)
    if filters.pokemon_id:
        conditions.append(Card.pokemon_id == filters.pokemon_id)

    if conditions:
        stmt = stmt.where(and_(*conditions))
    return stmt.distinct()
