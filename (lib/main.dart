import 'package:flutter/material.dart';

void main() {
  runApp(const SultanPharmaApp());
}

class SultanPharmaApp extends StatelessWidget {
  const SultanPharmaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'العين الساهرة سلطان',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const MainNavigationScreen(),
    );
  }
}

// الشاشة الرئيسية مع شريط أزرار تحكم سفلي وتصميم تفاعلي مضمون
class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeScreen(),
    const InventoryScreen(),
    const SalesScreen(),
    const FieldActivitiesScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.blueAccent,
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'الرئيسية'),
          BottomNavigationBarItem(icon: Icon(Icons.medical_services), label: 'المخزون'),
          BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet), label: 'المبيعات'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'الأنشطة'),
        ],
      ),
    );
  }
}

// 1. شاشة لوحة التحكم الرئيسية مع أزرار تحكم بارزة
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('شركة الأدوية - العين الساهرة'),
        centerTitle: true,
        backgroundColor: Colors.blueAccent,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              elevation: 3,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.verified_user, color: Colors.blue, size: 36),
                    SizedBox(width: 16),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('المعرف الرئيسي للنظام', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        SizedBox(height: 4),
                        Text('sal (نشط وموثق)', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'أزرار التحكم السريع بالأقسام:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueGrey),
            ),
            const SizedBox(height: 15),
            Expanded(
              child: GridView.count(
                crossAxisCount: 1,
                childAspectRatio: 3.5,
                crossAxisSpacing: 10,
                mainAxisSpacing: 12,
                children: [
                  _buildActionButton(
                    context,
                    title: 'إدارة المخزون والأدوية',
                    icon: Icons.medical_services,
                    color: Colors.green,
                    destination: const InventoryScreen(),
                  ),
                  _buildActionButton(
                    context,
                    title: 'سجل الحسابات والمبيعات',
                    icon: Icons.account_balance_wallet,
                    color: Colors.orange,
                    destination: const SalesScreen(),
                  ),
                  _buildActionButton(
                    context,
                    title: 'تتبع الأنشطة الميدانية',
                    icon: Icons.history,
                    color: Colors.purple,
                    destination: const FieldActivitiesScreen(),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton(
    BuildContext context, {
    required String title,
    required IconData icon,
    required Color color,
    required Widget destination,
  }) {
    return ElevatedButton.styleFrom(
      // استخدام زر بارز ومضمون الاستجابة
    ).let((_) => ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        elevation: 4,
      ),
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => destination),
        );
      },
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 28),
          const SizedBox(width: 12),
          Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ],
      ),
    ));
  }
}

// امتداد مساعدة صغير لضمان بناء الزر بسلاسة
extension on ButtonStyle {
  Widget let(Widget Function(ButtonStyle) callback) => callback(this);
}

// 2. شاشة إدارة المخزون والأدوية
class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  State<InventoryScreen> createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final List> _medicines = [
    {'name': 'باراسيتامول 500ملجم', 'quantity': '150 علبة', 'price': '500 ر.ي'},
    {'name': 'أموكسيسيلين 250ملجم', 'quantity': '80 علبة', 'price': '1200 ر.ي'},
  ];

  final _nameController = TextEditingController();
  final _qtyController = TextEditingController();

  void _addMedicine() {
    if (_nameController.text.isNotEmpty && _qtyController.text.isNotEmpty) {
      setState(() {
        _medicines.add({
          'name': _nameController.text,
          'quantity': '${_qtyController.text} علبة',
          'price': 'محدد حديثاً',
        });
      });
      _nameController.clear();
      _qtyController.clear();
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('إدارة المخزون والأدوية'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        itemCount: _medicines.length,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            child: ListTile(
              leading: const Icon(Icons.medication, color: Colors.green),
              title: Text(_medicines[index]['name']!),
              subtitle: Text('الكمية: ${_medicines[index]['quantity']}'),
              trailing: Text(_medicines[index]['price']!),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.green,
        onPressed: () {
          showModalBottomSheet(
            context: context,
            builder: (_) => Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('إضافة دواء جديد للمخزون', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'اسم الدواء')),
                  TextField(controller: _qtyController, decoration: const InputDecoration(labelText: 'الكمية'), keyboardType: TextInputType.number),
                  const SizedBox(height: 15),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.green, foregroundColor: Colors.white),
                    onPressed: _addMedicine,
                    child: const Text('حفظ وإضافة'),
                  ),
                ],
              ),
            ),
          );
        },
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }
}

// 3. شاشة سجل الحسابات والمبيعات
class SalesScreen extends StatelessWidget {
  const SalesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('سجل الحسابات والمبيعات'),
        backgroundColor: Colors.orange,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Card(
              color: Colors.orangeAccent,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('إجمالي مبيعات اليوم:', style: TextStyle(color: Colors.white, fontSize: 16)),
                    Text('45,000 ر.ي', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 15),
            Expanded(
              child: ListView(
                children: const [
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.receipt_long, color: Colors.orange),
                      title: Text('فاتورة #102 - صيدلية الأمل'),
                      subtitle: Text('المبلغ: 15,000 ر.ي'),
                      trailing: Text('مكتمل', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                    ),
                  ),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.receipt_long, color: Colors.orange),
                      title: Text('فاتورة #103 - صيدلية الشفاء'),
                      subtitle: Text('المبلغ: 30,000 ر.ي'),
                      trailing: Text('مكتمل', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// 4. شاشة تتبع الأنشطة الميدانية
class FieldActivitiesScreen extends StatelessWidget {
  const FieldActivitiesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('تتبع الأنشطة الميدانية'),
        backgroundColor: Colors.purple,
        foregroundColor: Colors.white,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: const [
          Card(
            child: ListTile(
              leading: Icon(Icons.location_on, color: Colors.purple),
              title: Text('زيارة صيدلية الشفاء'),
              subtitle: Text('الحالة: تم تسليم الطلبية - الساعة 10:30 صباحاً'),
            ),
          ),
          Card(
            child: ListTile(
              leading: Icon(Icons.location_on, color: Colors.purple),
              title: Text('زيارة مركز السعادة الطبي'),
              subtitle: Text('الحالة: قيد الانتظار / الموعد 02:00 ظهراً'),
            ),
          ),
        ],
      ),
    );
  }
}
