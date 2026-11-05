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
        primaryColor: Colors.blueAccent,
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const HomeScreen(),
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
          children: [
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Row(
                  children: const [
                    Icon(Icons.person, color: Colors.blue, size: 30),
                    SizedBox(width: 16),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('المعرف الرئيسي', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        SizedBox(height: 4),
                        Text('sal', style: TextStyle(color: Colors.grey, fontSize: 14)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 15),
            Expanded(
              child: ListView(
                children: [
                  // القسم الأول: إدارة المخزون
                  _buildMenuCard(
                    context,
                    title: 'إدارة المخزون والأدوية',
                    subtitle: 'إضافة واستعراض الأدوية المتاحة',
                    icon: Icons.medical_services,
                    iconColor: Colors.green,
                    destination: const InventoryScreen(),
                  ),
                  const SizedBox(height: 10),
                  // القسم الثاني: الحسابات والمبيعات
                  _buildMenuCard(
                    context,
                    title: 'سجل الحسابات والمبيعات',
                    subtitle: 'تسجيل المبيعات والعمليات المالية',
                    icon: Icons.account_balance_wallet,
                    iconColor: Colors.orange,
                    destination: const SalesScreen(),
                  ),
                  const SizedBox(height: 10),
                  // القسم الثالث: الأنشطة الميدانية
                  _buildMenuCard(
                    context,
                    title: 'تتبع الأنشطة الميدانية',
                    subtitle: 'تسجيل ومتابعة زيارات الزيارات الميدانية',
                    icon: Icons.history,
                    iconColor: Colors.purple,
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

  // بطاقة تفاعلية محسنة هندسياً لاستجابة اللمس بنسبة 100%
  Widget _buildMenuCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required IconData icon,
    required Color iconColor,
    required Widget destination,
  }) {
    return Card(
      elevation: 3,
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
              Icon(icon, color: iconColor, size: 32),
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
              const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
            ],
          ),
        ),
      ),
    );
  }
}

// 1. شاشة إدارة المخزون والأدوية
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
          'price': 'غير محدد',
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
                  const Text('إضافة دواء جديد', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'اسم الدواء')),
                  TextField(controller: _qtyController, decoration: const InputDecoration(labelText: 'الكمية'), keyboardType: TextInputType.number),
                  const SizedBox(height: 15),
                  ElevatedButton(onPressed: _addMedicine, child: const Text('حفظ في المخزون'))
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
            const Card(
              color: Colors.orangeAccent,
              child: Padding(
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
                  ListTile(
                    leading: Icon(Icons.receipt_long, color: Colors.orange),
                    title: Text('فاتورة #102 - صيدلية الأمل'),
                    subtitle: Text('المبلغ: 15,000 ر.ي'),
                    trailing: Text('مكتمـل', style: TextStyle(color: Colors.green)),
                  ),
                  Divider(),
                  ListTile(
                    leading: Icon(Icons.receipt_long, color: Colors.orange),
                    title: Text('فاتورة #103 - صيدلية الشفاء'),
                    subtitle: Text('المبلغ: 30,000 ر.ي'),
                    trailing: Text('مكتمـل', style: TextStyle(color: Colors.green)),
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
