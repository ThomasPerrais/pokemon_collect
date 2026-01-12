import 'package:flutter/material.dart';

import 'card_research_screen.dart';
import 'home_screen.dart';

class PokeballPainter extends CustomPainter {
  final Color borderColor;
  final Color topColor;
  final Color centerColor;

  PokeballPainter({
    required this.borderColor,
    required this.topColor,
    required this.centerColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    final strokePaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2
      ..color = borderColor;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2 - 1;

    // Draw outer circle border
    canvas.drawCircle(center, radius, strokePaint);

    // Draw top half (red)
    paint.color = topColor;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -3.14159, // -π (top)
      3.14159,  // π (half circle)
      false,
      paint,
    );

    // Draw bottom half (white)
    paint.color = Colors.white;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      0,        // 0 (right)
      3.14159,  // π (half circle)
      false,
      paint,
    );

    // Draw horizontal line
    strokePaint.strokeWidth = 1.5;
    canvas.drawLine(
      Offset(1, size.height / 2),
      Offset(size.width - 1, size.height / 2),
      strokePaint,
    );

    // Draw center circle
    paint.color = centerColor;
    canvas.drawCircle(center, radius * 0.3, paint);
    paint.color = Colors.white;
    canvas.drawCircle(center, radius * 0.25, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}

class MainNavigationScreen extends StatefulWidget {
  @override
  _MainNavigationScreenState createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    HomeScreen(),
    CardResearchScreen(),
  ];

  Widget _buildPokeballIcon({required bool isSelected}) {
    final color = isSelected 
        ? Theme.of(context).primaryColor 
        : Colors.grey;
    final redColor = isSelected ? Colors.red[600]! : Colors.grey[400]!;
    
    return SizedBox(
      width: 24,
      height: 24,
      child: CustomPaint(
        painter: PokeballPainter(
          borderColor: color,
          topColor: redColor,
          centerColor: color,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(
            icon: _buildPokeballIcon(isSelected: _currentIndex == 0),
            activeIcon: _buildPokeballIcon(isSelected: true),
            label: 'Pokemon',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.credit_card),
            label: 'Cards',
          ),
        ],
      ),
    );
  }
}

