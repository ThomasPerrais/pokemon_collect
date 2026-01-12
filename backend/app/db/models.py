from app.db.database import Base
import enum

from sqlalchemy import String, ForeignKey, and_
from sqlalchemy_enum34 import EnumType

from sqlalchemy import Date, Integer, Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, foreign


class PokemonGeneration(Base):
    """
    ORM model for the 'pokemon_generation' table.
    Represents a generation of Pokemon.
    """

    __tablename__ = "pokemon_generation"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    release_year: Mapped[int]

    pokemons: Mapped[list["Pokemon"]] = relationship(
        back_populates="generation", cascade="all, delete-orphan"
    )


class PokemonType(Base):
    """
    ORM model for the 'type' table.
    Represents a Pokemon type (e.g., Fire, Water).
    """

    __tablename__ = "pokemon_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    pokemons: Mapped[list["Pokemon"]] = relationship(
        secondary="pokemon_type_association", back_populates="types"
    )


class PokemonTypeAssociation(Base):
    """
    Association table for many-to-many relationship between Pokemon and PokemonType.
    """

    __tablename__ = "pokemon_type_association"
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    type_id: Mapped[int] = mapped_column(
        ForeignKey("pokemon_type.id"), primary_key=True
    )


class PokemonTag(Base):
    """
    ORM model for the 'tag' table.
    Represents a tag that can be associated with Pokemon (e.g., Legendary, Starter).
    """

    __tablename__ = "pokemon_tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    pokemons: Mapped[list["Pokemon"]] = relationship(
        secondary="pokemon_tag_association", back_populates="tags"
    )


class PokemonTagAssociation(Base):
    """
    Association table for many-to-many relationship between Pokemon and PokemonTag.
    """

    __tablename__ = "pokemon_tag_association"
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("pokemon_tag.id"), primary_key=True)


class PokemonEvolution(Base):
    """
    ORM model for the 'pokemon_evolution' table.
    Represents an evolution relationship between two Pokemon.
    """

    __tablename__ = "pokemon_evolution"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"))
    to_pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"))
    evolution_method: Mapped[str] = mapped_column(String(255))

    from_pokemon: Mapped["Pokemon"] = relationship(
        "Pokemon", foreign_keys=[from_pokemon_id], back_populates="evolutions_from"
    )
    to_pokemon: Mapped["Pokemon"] = relationship(
        "Pokemon", foreign_keys=[to_pokemon_id], back_populates="evolutions_to"
    )


class Pokemon(Base):
    """
    ORM model for the 'pokemon' table.
    Represents a Pokemon species.
    """

    __tablename__ = "pokemon"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    national_dex_number: Mapped[int]

    generation_id: Mapped[int] = mapped_column(ForeignKey("pokemon_generation.id"))
    generation: Mapped["PokemonGeneration"] = relationship(back_populates="pokemons")

    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    cards: Mapped[list["Card"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )

    types: Mapped[list["PokemonType"]] = relationship(
        secondary="pokemon_type_association", back_populates="pokemons"
    )

    tags: Mapped[list["PokemonTag"]] = relationship(
        secondary="pokemon_tag_association", back_populates="pokemons"
    )

    # Self-referential relationships via PokemonEvolution
    evolutions_from: Mapped[list["PokemonEvolution"]] = relationship(
        "PokemonEvolution",
        foreign_keys="[PokemonEvolution.from_pokemon_id]",
        back_populates="from_pokemon",
        cascade="all, delete-orphan",
    )

    evolutions_to: Mapped[list["PokemonEvolution"]] = relationship(
        "PokemonEvolution",
        foreign_keys="[PokemonEvolution.to_pokemon_id]",
        back_populates="to_pokemon",
        cascade="all, delete-orphan",
    )

    star_in_sets: Mapped[list["Set"]] = relationship(
        secondary="set_star_pokemon", back_populates="star_pokemons"
    )

    # Optional convenience properties
    @property
    def evolutions(self) -> list["Pokemon"]:
        """Pokemon this one evolves into."""
        return [evo.to_pokemon for evo in self.evolutions_from]

    @property
    def pre_evolutions(self) -> list["Pokemon"]:
        """Pokemon this one evolves from."""
        return [evo.from_pokemon for evo in self.evolutions_to]


class Era(Base):
    """
    ORM model for the 'era' table.
    Represents a bloc of Pokemon cards sets.
    """

    __tablename__ = "era"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    start_year: Mapped[int]
    end_year: Mapped[int]
    publisher: Mapped[str] = mapped_column(String(255))

    sets: Mapped[list["Set"]] = relationship(
        back_populates="era", cascade="all, delete-orphan"
    )


class Set(Base):
    """
    ORM model for the 'set' table.
    Represents a Pokemon card set belonging to an era.
    """

    __tablename__ = "set"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    era_index: Mapped[float] = mapped_column(Numeric(3, 1))

    release_date: Mapped[Date] = mapped_column(Date)
    abbreviation: Mapped[str] = mapped_column(String(10))
    total_cards: Mapped[int]
    secret_cards: Mapped[int]

    era_id: Mapped[int] = mapped_column(ForeignKey("era.id"))
    era: Mapped["Era"] = relationship(back_populates="sets")

    cards: Mapped[list["Card"]] = relationship(
        back_populates="set", cascade="all, delete-orphan"
    )
    star_pokemons: Mapped[list["Pokemon"]] = relationship(
        secondary="set_star_pokemon", back_populates="star_in_sets"
    )


class SetStarPokemon(Base):
    """
    ORM model for the 'set_star_pokemon' table.
    Represents a star Pokemon of a set.
    """

    __tablename__ = "set_star_pokemon"
    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"))


class Card(Base):
    """
    ORM model for the 'card' table.
    Represents a Pokemon card belonging to a set.
    """

    __tablename__ = "card"

    class CardType(enum.Enum):
        pokemon = "pokemon"
        object = "object"
        supporter = "supporter"

    class CardRarity(enum.Enum):
        common = "common"
        uncommon = "uncommon"
        rare = "rare"  # <EV: rare cards.
        holographic = "holographic"
        double_rare = "double_rare"  # >EV = Ex cards.
        alternative = "alternative"  # >EV: illustrated alternative art cards.
        ultra_rare = "ultra_rare"  # >EV: alternative art double-rare cards & trainers.
        secret = "secret"  # <EV: secret rare cards.
        alt_special_rare = "alt_special_rare"  # >EV: illustrated double-rare cards & trainers.
        hyper_rare = "hyper_rare"  # >EV: 3 stars gold cards.
        mega_hyper_rare = "mega_hyper_rare"  # <ME: méga-evolutions gold cards.
        special_rare = "special_rare"  # other categories of rare cards (e.g. black/white rare in BLK and WHT).
        shiny = "shiny"
        double_shiny = "double_shiny"
        promo = "promo"
        tech = "tech"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    number: Mapped[int]
    rarity: Mapped[CardRarity] = mapped_column(EnumType(CardRarity))
    type: Mapped[CardType] = mapped_column(EnumType(CardType))

    image_path: Mapped[str] = mapped_column(String(255))

    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    set: Mapped["Set"] = relationship(back_populates="cards")

    pokemon_id: Mapped[int | None] = mapped_column(
        ForeignKey("pokemon.id"), nullable=True
    )
    pokemon: Mapped["Pokemon"] = relationship(back_populates="cards")


# TODO: remaining tables!!