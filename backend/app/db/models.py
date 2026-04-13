from app.db.database import Base
import enum

from sqlalchemy import String, ForeignKey, UniqueConstraint

from sqlalchemy import Date, Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship


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

    # add unique key constraint on name
    __table_args__ = (
        UniqueConstraint("name", name="uq_pokemon_name"),
    )


class Era(Base):
    """
    ORM model for the 'era' table.
    Represents a bloc of Pokemon cards sets.
    """

    __tablename__ = "era"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    sets: Mapped[list["Set"]] = relationship(
        back_populates="era", cascade="all, delete-orphan"
    )

    # add unique key constraint on name
    __table_args__ = (
        UniqueConstraint("name", name="uq_era_name"),
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

    era_id: Mapped[int] = mapped_column(ForeignKey("era.id"))
    era: Mapped["Era"] = relationship(back_populates="sets")

    cards: Mapped[list["Card"]] = relationship(
        back_populates="set", cascade="all, delete-orphan"
    )
    star_pokemons: Mapped[list["Pokemon"]] = relationship(
        secondary="set_star_pokemon", back_populates="star_in_sets"
    )

    # add unique key constraint on name
    __table_args__ = (
        UniqueConstraint("name", name="uq_set_name"),
        UniqueConstraint("abbreviation", name="uq_set_abbreviation"),
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
        # trainer = "trainer"
        stadium = "stadium"
        energy = "energy"
        tool = "tool"

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
        rainbow_rare = "rainbow_rare"
        gold_rare = "gold_rare"
        double_shiny = "double_shiny"
        promo = "promo"
        tech = "tech"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    number: Mapped[int]
    rarity: Mapped[CardRarity]
    type: Mapped[CardType]

    image_path: Mapped[str] = mapped_column(String(255))

    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    set: Mapped["Set"] = relationship(back_populates="cards")

    pokemon_id: Mapped[int | None] = mapped_column(
        ForeignKey("pokemon.id"), nullable=True
    )
    pokemon: Mapped["Pokemon"] = relationship(back_populates="cards")

    __table_args__ = (
        UniqueConstraint("set_id", "number", name="uq_card_set_number"),
    )


class AbstractBooster(Base):
    """
    ORM model for the 'abstract_booster' table
    Represents an abstract booster related to a pokemon set
    """

    __tablename__ = "abstract_booster"

    id: Mapped[int] = mapped_column(primary_key=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    card_count: Mapped[int]

    __table_args__ = (
        UniqueConstraint("set_id", "card_count", name="uq_card_number_booster"),
    )


class Booster(Base):
    """
    ORM model for the 'booster' table.
    Represent one of the booster illustration of a pokemon set
    """

    __tablename__ = "booster"

    id: Mapped[int] = mapped_column(primary_key=True)
    abstract_booster_id: Mapped[int] = mapped_column(ForeignKey("abstract_booster.id"))
    name: Mapped[str] = mapped_column(String(255))


class BoosterPokemon(Base):
    """
    ORM model for the "booster_pokemon" association table.
    This table stores the pokemons illustrated on each booster
    """

    __tablename__ = "booster_pokemon"

    id: Mapped[int] = mapped_column(primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"))
    booster_id: Mapped[int] = mapped_column(ForeignKey("booster.id"))


class Item(Base):
    """
    ORM model for the 'item' table.
    Represents an abstract pokemon item commercialized
    """

    __tablename__ = "item"

    class ItemType(enum.Enum):
        blister = "blister"
        booster = "booster"
        duopack = "duopack"
        tripack = "tripack"
        pokebox = "pokebox"
        coffret = "coffret"
        half_display = "half_display"
        display = "display"
        ETB = "ETB"
        bundle = "bundle"
        mini_tin = "mini_tin"
        art_set = "art_set"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[ItemType]
    retail_price: Mapped[float] = mapped_column(Numeric(7, 2))
    release_date: Mapped[Date] = mapped_column(Date)


class ItemPokemon(Base):
    """
    ORM model for the "item_pokemon" association table.
    This table stores the pokemons illustrated on each item
    """

    __tablename__ = "item_pokemon"

    id: Mapped[int] = mapped_column(primary_key=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemon.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))


class ItemAbstractContent(Base):
    """
    ORM model for the 'item_abstract_content' table.
    This table stores the content of every pokemon item in terms of abstract boosters
    """

    __tablename__ = "item_abstract_content"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    abstract_booster_id: Mapped[int] = mapped_column(ForeignKey("abstract_booster.id"))
    quantity: Mapped[int]


class ItemExactContent(Base):
    """
    ORM model for the 'item_exact_content' table.
    This table stores the content of every pokemon item in terms of exact boosters illustrations
    """

    __tablename__ = "item_exact_content"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    booster_id: Mapped[int] = mapped_column(ForeignKey("booster.id"))
    quantity: Mapped[int]


class ItemExactCardContent(Base):
    """
    ORM model for the 'item_exact_card_content' table.
    This table stores the promo cards contained in every pokemon item
    """
    
    __tablename__ = "item_exact_card_content"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))
    quantity: Mapped[int]


class User(Base):
    """
    ORM model for the 'user' table.
    This table stores user information
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[Date] = mapped_column(Date)

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

# TODO: remaining tables!!
# Table user {
#   id serial pk
#   username varchar [unique, not null]
#   email varchar [unique, not null]
#   created_at timestamp [default: `now()`]
# }

# Table user_item {
#   id serial pk
#   user_id int [ref: > user.id, not null]
#   item_id int [ref: > item.id ,not null]
#   name varchar
# }

# Table user_card {
#   id serial pk
#   user_id int [ref: > user.id, not null]
#   card_id int [ref: > card.id, not null]
#   booster_opening_id int [ref: > user_booster_opening.id]
# }

# Table user_item_condition {
#   id serial pk
#   user_item_id int [ref: > user_item.id, not null]
#   date timestamp [default: "now()"]
#   condition sealed_item_condition
# }

# Table user_card_condition {
#   id serial pk
#   user_card_id int [ref: > user_card.id, not null]
#   date timestamp [default: "now()"]
#   condition card_condition
# }

# Enum transaction {
#   buy
#   sell
# }

# Table user_item_transaction {
#   id serial pk
#   user_item_id int [ref: > user_item.id, not null]
#   type transaction
#   counterparty varchar
# }

# Table user_card_transaction {
#   id serial pk
#   user_card_id int [ref: > user_card.id, not null]
#   type transaction
#   counterparty varchar
# }

# Table user_booster_opening {
#   id serial pk
#   date date
#   serie int [ref: > serie.id, not null]
#   item int [ref: > user_item.id, not null]
# }


# Table gradation_service {
#   id serial pk
#   name varchar
#   country varchar
# }

# Table gradation {
#   id serial pk
#   card_id int [ref: > user_card.id, not null]
#   service gradation_service

# }