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
      ),
      home: const MainNavigationScreen(),
    );
  }
}

// الشاشة الرئيسية مع شريط التنقل السفلي
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
          BottomNavigationBarItem(icon: Icon(Icons.home, size: 28), label: 'الرئيسية'),
          BottomNavigationBarItem(icon: Icon(Icons.medical_services, size: 28), label: 'المخزون'),
          BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet, size: 28), label: 'المبيعات'),
          BottomNavigationBarItem(icon: Icon(Icons.history, size: 28), label: 'الأنشطة'),
        ],
      ),
    );
  }
}

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
              child: ListView(
                children: [
                  _buildNavButton(
                    context,
                    title: 'إدارة المخزون والأدوية',
                    subtitle: 'إضافة ومتابعة أصناف الأدوية',
                    icon: Icons.medical_services,
                    color: Colors.green,
                    destination: const InventoryScreen(),
                  ),
                  const SizedBox(height: 12),
                  _buildNavButton(
                    context,
                    title: 'سجل الحسابات والمبيعات',
                    subtitle: 'تسجيل الفواتير والعمليات المالية',
                    icon: Icons.account_balance_wallet,
                    color: Colors.orange,
                    destination: const SalesScreen(),
                  ),
                  const SizedBox(height: 12),
                  _buildNavButton(
                    context,
                    title: 'تتبع الأنشطة الميدانية',
                    subtitle: 'متابعة زيارات الصيدليات والمناديب',
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

  Widget _buildNavButton(
    BuildContext context, {
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required Widget destination,
  }) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => destination),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              Icon(icon, color: color, size: 32),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                    const SizedBox(height: 4),
                    Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 13)),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 18, color: Colors.grey),
            ],
          ),
        ),
      ),
    );
  }
}

// 1. شاشة إدارة المخزون والأدوية (مع دعم البحث والتصفية)
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

  List> _filteredMedicines = [];
  final _searchController = TextEditingController();
  final _nameController = TextEditingController();
  final _qtyController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _filteredMedicines = _medicines;
    _searchController.addListener(_filterMedicines);
  }

  void _filterMedicines() {
    final query = _searchController.text.toLowerCase();
    setState(() {
      _filteredMedicines = _medicines.where((med) {
        return med['name']!.toLowerCase().contains(query);
      }).toList();
    });
  }

  void _addMedicine() {
    if (_nameController.text.isNotEmpty && _qtyController.text.isNotEmpty) {
      setState(() {
        _medicines.add({
          'name': _nameController.text,
          'quantity': '${_qtyController.text} علبة',
          'price': 'محدد حديثاً',
        });
        _filteredMedicines = _medicines;
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
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'بحث عن دواء...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _filteredMedicines.length,
              itemBuilder: (context, index) {
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  child: ListTile(
                    leading: const Icon(Icons.medication, color: Colors.green),
                    title: Text(_filteredMedicines[index]['name']!),
                    subtitle: Text('الكمية: ${_filteredMedicines[index]['quantity']}'),
                    trailing: Text(_filteredMedicines[index]['price']!),
                  ),
                );
              },
            ),
          ),
        ],
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

// 2. شاشة سجل الحسابات والمبيعات
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

// 3. شاشة تتبع الأنشطة الميدانية
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
