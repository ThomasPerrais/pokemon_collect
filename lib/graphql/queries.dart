const String getPokemonsQuery = r'''
  query GetPokemons($filters: PokemonFilter) {
    pokemons(filters: $filters) {
      id
      name
      nationalDexNumber
      generation {
        id
        name
        releaseYear
      }
      types {
        id
        name
      }
      tags {
        id
        name
      }
    }
  }
''';

const String getTypesQuery = r'''
  query {
    types {
      id
      name
    }
  }
''';
