import 'package:flutter/material.dart';

import '../models/pokemon.dart';

class PokemonTile extends StatelessWidget {
  final Pokemon pokemon;
  final VoidCallback? onTap;

  const PokemonTile({
    Key? key,
    required this.pokemon,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        leading: CircleAvatar(
          child: Text(
            '#${pokemon.nationalDexNumber}',
            style: TextStyle(fontSize: 12),
          ),
        ),
        title: Text(
          pokemon.name,
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 4),
            Text('Generation: ${pokemon.generation.name}'),
            SizedBox(height: 4),
            Wrap(
              spacing: 4,
              children: pokemon.types.map((type) {
                return Chip(
                  label: Text(
                    type.name,
                    style: TextStyle(fontSize: 11),
                  ),
                  padding: EdgeInsets.all(0),
                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                );
              }).toList(),
            ),
          ],
        ),
        trailing: Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}

