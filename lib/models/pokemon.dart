class Pokemon {
  final int id;
  final String name;
  final int nationalDexNumber;
  final PokemonGeneration generation;
  final List<PokemonType> types;
  final List<PokemonTag> tags;

  Pokemon({
    required this.id,
    required this.name,
    required this.nationalDexNumber,
    required this.generation,
    required this.types,
    required this.tags,
  });

  factory Pokemon.fromJson(Map<String, dynamic> json) {
    return Pokemon(
      id: json['id'] as int,
      name: json['name'] as String,
      nationalDexNumber: json['nationalDexNumber'] as int? ?? 
                          (json['national_dex_number'] as int? ?? 0),
      generation: PokemonGeneration.fromJson(
        json['generation'] as Map<String, dynamic>,
      ),
      types: (json['types'] as List<dynamic>?)
              ?.map((type) => PokemonType.fromJson(type as Map<String, dynamic>))
              .toList() ??
          [],
      tags: (json['tags'] as List<dynamic>?)
              ?.map((tag) => PokemonTag.fromJson(tag as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

class PokemonGeneration {
  final int id;
  final String name;
  final int releaseYear;

  PokemonGeneration({
    required this.id,
    required this.name,
    required this.releaseYear,
  });

  factory PokemonGeneration.fromJson(Map<String, dynamic> json) {
    return PokemonGeneration(
      id: json['id'] as int,
      name: json['name'] as String,
      releaseYear: json['releaseYear'] as int? ?? 
                    (json['release_year'] as int? ?? 0),
    );
  }
}

class PokemonType {
  final int id;
  final String name;

  PokemonType({
    required this.id,
    required this.name,
  });

  factory PokemonType.fromJson(Map<String, dynamic> json) {
    return PokemonType(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}

class PokemonTag {
  final int id;
  final String name;

  PokemonTag({
    required this.id,
    required this.name,
  });

  factory PokemonTag.fromJson(Map<String, dynamic> json) {
    return PokemonTag(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}

