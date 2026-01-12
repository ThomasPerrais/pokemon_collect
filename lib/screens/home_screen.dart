import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

import '../graphql/queries.dart';
import '../models/pokemon.dart';
import '../widget/pokemon_tile.dart';
import 'pokemon_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _nameFilterController = TextEditingController();
  Set<String> _selectedTypes = {};
  List<String> _availableTypes = [];

  @override
  void dispose() {
    _nameFilterController.dispose();
    super.dispose();
  }

  Map<String, dynamic> _buildFilters() {
    final Map<String, dynamic> filterParams = {};
    
    if (_nameFilterController.text.isNotEmpty) {
      // Convert simple text search to regex pattern (case-insensitive)
      filterParams['nameRegex'] = _nameFilterController.text;
    }
    
    if (_selectedTypes.isNotEmpty) {
      filterParams['types'] = _selectedTypes.toList();
    }
    
    // Return empty map if no filters, otherwise wrap in 'filters' key
    return filterParams.isEmpty ? {} : {'filters': filterParams};
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pokemon Research'),
      ),
      body: Column(
        children: [
          // Filter section
          Container(
            padding: EdgeInsets.all(16),
            color: Colors.grey[100],
            child: Column(
              children: [
                // Name filter
                TextField(
                  controller: _nameFilterController,
                  decoration: InputDecoration(
                    labelText: 'Filter by name',
                    hintText: 'Enter pokemon name...',
                    prefixIcon: Icon(Icons.search),
                    suffixIcon: _nameFilterController.text.isNotEmpty
                        ? IconButton(
                            icon: Icon(Icons.clear),
                            onPressed: () {
                              setState(() {
                                _nameFilterController.clear();
                              });
                            },
                          )
                        : null,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  onChanged: (value) {
                    setState(() {});
                  },
                ),
                SizedBox(height: 12),
                // Type filter
                Query(
                  options: QueryOptions(document: gql(getTypesQuery)),
                  builder: (QueryResult result, {refetch, fetchMore}) {
                    if (result.hasException) {
                      return Text('Error loading types');
                    }

                    if (result.isLoading) {
                      return CircularProgressIndicator();
                    }

                    final List types = result.data?['types'] ?? [];
                    if (_availableTypes.isEmpty && types.isNotEmpty) {
                      WidgetsBinding.instance.addPostFrameCallback((_) {
                        setState(() {
                          _availableTypes = types
                              .map((type) => type['name'] as String)
                              .toList();
                        });
                      });
                    }

                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.category, size: 20),
                            SizedBox(width: 8),
                            Text(
                              'Filter by type',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Spacer(),
                            if (_selectedTypes.isNotEmpty)
                              TextButton(
                                onPressed: () {
                                  setState(() {
                                    _selectedTypes.clear();
                                  });
                                },
                                child: Text('Clear all'),
                              ),
                          ],
                        ),
                        SizedBox(height: 8),
                        Container(
                          padding: EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey[300]!),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Wrap(
                            spacing: 8,
                            runSpacing: 8,
                            children: _availableTypes.map((type) {
                              final isSelected = _selectedTypes.contains(type);
                              return FilterChip(
                                label: Text(type),
                                selected: isSelected,
                                onSelected: (selected) {
                                  setState(() {
                                    if (selected) {
                                      _selectedTypes.add(type);
                                    } else {
                                      _selectedTypes.remove(type);
                                    }
                                  });
                                },
                                selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
                                checkmarkColor: Theme.of(context).primaryColor,
                              );
                            }).toList(),
                          ),
                        ),
                        if (_selectedTypes.isNotEmpty) ...[
                          SizedBox(height: 8),
                          Wrap(
                            spacing: 4,
                            runSpacing: 4,
                            children: _selectedTypes.map((type) {
                              return Chip(
                                label: Text(type),
                                onDeleted: () {
                                  setState(() {
                                    _selectedTypes.remove(type);
                                  });
                                },
                                backgroundColor: Theme.of(context).primaryColor,
                                labelStyle: TextStyle(color: Colors.white),
                                deleteIconColor: Colors.white,
                              );
                            }).toList(),
                          ),
                        ],
                      ],
                    );
                  },
                ),
              ],
            ),
          ),
          // Pokemon list
          Expanded(
            child: Query(
              key: ValueKey('pokemons_${_nameFilterController.text}_${_selectedTypes.join(",")}'),
              options: QueryOptions(
                document: gql(getPokemonsQuery),
                variables: _buildFilters(),
                fetchPolicy: FetchPolicy.networkOnly,
              ),
              builder: (QueryResult result, {refetch, fetchMore}) {
                if (result.hasException) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.error_outline, size: 48, color: Colors.red),
                        SizedBox(height: 16),
                        Text(
                          'Error: ${result.exception.toString()}',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: Colors.red),
                        ),
                        SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () => refetch?.call(),
                          child: Text('Retry'),
                        ),
                      ],
                    ),
                  );
                }

                if (result.isLoading) {
                  return Center(child: CircularProgressIndicator());
                }

                final List pokemonsData = result.data?['pokemons'] ?? [];

                if (pokemonsData.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.search_off, size: 64, color: Colors.grey),
                        SizedBox(height: 16),
                        Text(
                          'No pokemons found',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey[600],
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Try adjusting your filters',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[500],
                          ),
                        ),
                      ],
                    ),
                  );
                }

                final List<Pokemon> pokemons = pokemonsData
                    .map((data) => Pokemon.fromJson(data))
                    .toList();

                return RefreshIndicator(
                  onRefresh: () async {
                    await refetch?.call();
                  },
                  child: ListView.builder(
                    itemCount: pokemons.length,
                    itemBuilder: (context, index) {
                      final pokemon = pokemons[index];
                      return PokemonTile(
                        pokemon: pokemon,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => PokemonDetailScreen(
                                pokemon: pokemon,
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
