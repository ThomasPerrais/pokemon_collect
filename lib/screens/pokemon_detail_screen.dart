import 'package:flutter/material.dart';

import '../models/pokemon.dart';

class PokemonDetailScreen extends StatefulWidget {
  final Pokemon pokemon;

  const PokemonDetailScreen({
    Key? key,
    required this.pokemon,
  }) : super(key: key);

  @override
  _PokemonDetailScreenState createState() => _PokemonDetailScreenState();
}

class _PokemonDetailScreenState extends State<PokemonDetailScreen> {
  int _resultCount = 0; // This will be updated when results are available

  Pokemon get pokemon => widget.pokemon;

  // Map Pokemon types to colors
  Color _getTypeColor(String typeName) {
    final type = typeName.toLowerCase();
    switch (type) {
      // Fire types
      case 'feu':
        return Colors.red[400]!;
      
      // Water types
      case 'eau':
        return Colors.blue[400]!;
      
      // Electric types
      case 'électrik':
        return Colors.yellow[600]!;
      
      // Grass/Plant types
      case 'plante':
        return Colors.green[500]!;
      
      // Ice types
      case 'glace':
        return Colors.lightBlue[300]!;
      
      // Fighting types
      case 'combat':
        return Colors.orange[700]!;
      
      // Poison types
      case 'poison':
        return Colors.purple[400]!;
      
      // Ground types
      case 'sol':
        return Colors.brown[400]!;
      
      // Flying types
      case 'vol':
        return const Color.fromARGB(255, 96, 191, 234)!;
      
      // Psychic types
      case 'psy':
        return Colors.pink[400]!;
      
      // Bug types
      case 'insecte':
        return Colors.green[600]!;
      
      // Rock types
      case 'roche':
        return Colors.brown[600]!;
      
      // Ghost types
      case 'spectre':
        return Colors.purple[700]!;
      
      // Dragon types
      case 'dragon':
        return const Color.fromARGB(255, 140, 224, 237)!;
      
      // Dark types
      case 'ténèbre':
        return const Color.fromARGB(255, 112, 10, 236)!;
      
      // Steel types
      case 'acier':
        return const Color.fromARGB(255, 200, 199, 199)!;
      
      // Fairy types
      case 'fée':
        return Colors.pink[200]!;
      
      // Normal types
      case 'normal':
        return const Color.fromARGB(255, 164, 163, 163)!;
      
      default:
        return Colors.grey[300]!;
    }
  }

  // Get background color(s) based on Pokemon types
  List<Color> _getBackgroundColors() {
    if (pokemon.types.isEmpty) {
      return [Colors.grey[300]!, Colors.white];
    }
    
    if (pokemon.types.length == 1) {
      final color = _getTypeColor(pokemon.types[0].name);
      return [color.withOpacity(0.3), color.withOpacity(0.1), Colors.white];
    } else {
      // Multiple types: create a gradient
      final color1 = _getTypeColor(pokemon.types[0].name);
      final color2 = _getTypeColor(pokemon.types[1].name);
      return [
        color1.withOpacity(0.3),
        color2.withOpacity(0.3),
        Colors.white,
      ];
    }
  }

  // Remove accents from a string
  String _removeAccents(String input) {
    const Map<String, String> accentMap = {
      'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
      'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
      'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
      'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
      'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
      'ý': 'y', 'ÿ': 'y',
      'ñ': 'n',
      'ç': 'c',
      'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A',
      'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
      'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
      'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
      'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
      'Ý': 'Y',
      'Ñ': 'N',
      'Ç': 'C',
    };
    
    String result = input;
    accentMap.forEach((accent, replacement) {
      result = result.replaceAll(accent, replacement);
    });
    return result;
  }

  Widget _buildPokemonImage() {
    return Image.asset(
      'assets/images/pokemons/${pokemon.nationalDexNumber.toString().padLeft(3, '0')}_${_removeAccents(pokemon.name)}.png',
      fit: BoxFit.contain,
      errorBuilder: (context, error, stackTrace) {
        return Image.asset(
          'assets/images/000_Pokeball.png',
          fit: BoxFit.contain,
          errorBuilder: (context, error, stackTrace) {
            return Icon(Icons.image_not_supported, size: 100, color: Colors.white.withOpacity(0.7));
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final backgroundColors = _getBackgroundColors();
    final primaryTypeColor = pokemon.types.isNotEmpty
        ? _getTypeColor(pokemon.types[0].name)
        : Colors.grey;

    return Scaffold(
      backgroundColor: backgroundColors[0],
      appBar: AppBar(
        title: Text(pokemon.name),
        backgroundColor: primaryTypeColor,
        elevation: 0,
      ),
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: backgroundColors,
              ),
            ),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
            // Header section with National Dex Number
            Container(
              width: double.infinity,
              padding: EdgeInsets.all(24),
              child: Column(
                children: [
                  // National Dex Number badge
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: primaryTypeColor,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      '#${pokemon.nationalDexNumber.toString().padLeft(3, '0')}',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  SizedBox(height: 16),
                  // Pokemon Image
                  Container(
                    width: 200,
                    height: 200,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.3),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(20),
                      child: _buildPokemonImage(),
                    ),
                  ),
                  SizedBox(height: 16),
                  // Pokemon Name
                  Text(
                    pokemon.name,
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            
            // Types section
            Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Types',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: pokemon.types.map((type) {
                      final typeColor = _getTypeColor(type.name);
                      return Chip(
                        label: Text(
                          type.name,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                            color: Colors.white,
                          ),
                        ),
                        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        backgroundColor: typeColor,
                      );
                    }).toList(),
                  ),
                ],
              ),
            ),

            Divider(),

            // Generation section
            Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Generation',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 12),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.calendar_today),
                      title: Text(pokemon.generation.name),
                      subtitle: Text('Released in ${pokemon.generation.releaseYear}'),
                    ),
                  ),
                ],
              ),
            ),

            // Tags section (if any)
            if (pokemon.tags.isNotEmpty) ...[
              Divider(),
              Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Tags',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: pokemon.tags.map((tag) {
                        return Chip(
                          label: Text(
                            tag.name,
                            style: TextStyle(fontSize: 14),
                          ),
                          avatar: Icon(Icons.label, size: 18),
                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ],

            // Additional info section
            Divider(),
            Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Information',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 12),
                  Card(
                    child: Column(
                      children: [
                        ListTile(
                          leading: Icon(Icons.info_outline),
                          title: Text('ID'),
                          trailing: Text(
                            pokemon.id.toString(),
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        Divider(height: 1),
                        ListTile(
                          leading: Icon(Icons.numbers),
                          title: Text('National Dex Number'),
                          trailing: Text(
                            '#${pokemon.nationalDexNumber.toString().padLeft(3, '0')}',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            ],
          ),
        ),
      ),
          // Result count in bottom right corner
          Positioned(
            bottom: 16,
            right: 16,
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: primaryTypeColor.withOpacity(0.9),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                '$_resultCount result${_resultCount != 1 ? 's' : ''}',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

