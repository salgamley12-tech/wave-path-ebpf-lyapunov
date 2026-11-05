import 'package:flutter/material.dart';

void main() {
  runApp(const SultanPharmaEliteApp());
}

class SultanPharmaEliteApp extends StatelessWidget {
  const SultanPharmaEliteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'سلطان فارما - العين الساهرة (إصدار النخبة)',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const MainDashboardScreen(),
    );
  }
}

// الشاشة الرئيسية المتكاملة مع شريط التنقل السفلي ومؤشر الإصدار المرئي
class MainDashboardScreen extends StatefulWidget {
  const MainDashboardScreen({super.key});

  @override
  State<MainDashboardScreen> createState() => _MainDashboardScreenState();
}

class _MainDashboardScreenState extends State<MainDashboardScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeTabScreen(),
    const InventoryTabScreen(),
    const SalesTabScreen(),
    const ActivitiesTabScreen(),
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
          BottomNavigationBarItem(icon: Icon(Icons.home, size: 26), label: 'الرئيسية'),
          BottomNavigationBarItem(icon: Icon(Icons.medical_services, size: 26), label: 'المخزون'),
          BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet, size: 26), label: 'المبيعات'),
          BottomNavigationBarItem(icon: Icon(Icons.history, size: 26), label: 'الأنشطة'),
        ],
      ),
    );
  }
}

// تبويب الرئيسية
class HomeTabScreen extends StatelessWidget {
  const HomeTabScreen({super.key});

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
            // مؤشر الإصدار الدلائلي لقطع الشك باليقين
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                border: Border.all(color: Colors.green),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.check_circle, color: Colors.green),
                  SizedBox(width: 8),
                  Text(
                    'الإصدار المحدث: v3.5 (إصدار النخبة المعتمد)',
                    style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 15),
            Card(
              elevation: 3,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: const Padding(
                padding: EdgeInsets.all(14.0),
                child: Row(
                  children: [
                    Icon(Icons.verified_user, color: Colors.blue, size: 32),
                    SizedBox(width: 14),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('المعرف الرئيسي للنظام', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                        SizedBox(height: 2),
                        Text('sal (نشط وموثق من لجنة النخبة)', style: TextStyle(color: Colors.green, fontSize: 13, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 15),
            const Text(
              'أقسام نظام سلطان فارما:',
              style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Colors.blueGrey),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: ListView(
                children: const [
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.medical_services, color: Colors.green, size: 28),
                      title: Text('إدارة المخزون والأدوية', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text('متابعة الأصناف والأرصدة'),
                      trailing: Icon(Icons.arrow_forward_ios, size: 16),
                    ),
                  ),
                  SizedBox(height: 8),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.account_balance_wallet, color: Colors.orange, size: 28),
                      title: Text('سجل الحسابات والمبيعات', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text('العمليات والفواتير المالية'),
                      trailing: Icon(Icons.arrow_forward_ios, size: 16),
                    ),
                  ),
                  SizedBox(height: 8),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.history, color: Colors.purple, size: 28),
                      title: Text('تتبع الأنشطة الميدانية', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text('متابعة زيارات الصيدليات والمناديب'),
                      trailing: Icon(Icons.arrow_forward_ios, size: 16),
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

// تبويب المخزون
class InventoryTabScreen extends StatelessWidget {
  const InventoryTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('إدارة المخزون والأدوية'), backgroundColor: Colors.green, foregroundColor: Colors.white),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: const [
          Card(child: ListTile(leading: Icon(Icons.medication, color: Colors.green), title: Text('باراسيتامول 500ملجم'), subtitle: Text('الكمية: 150 علبة'), trailing: Text('500 ر.ي'))),
          Card(child: ListTile(leading: Icon(Icons.medication, color: Colors.green), title: Text('أموكسيسيلين 250ملجم'), subtitle: Text('الكمية: 80 علبة'), trailing: Text('1200 ر.ي'))),
        ],
      ),
    );
  }
}

// تبويب المبيعات
class SalesTabScreen extends StatelessWidget {
  const SalesTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('سجل الحسابات والمبيعات'), backgroundColor: Colors.orange, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            Card(color: Colors.orangeAccent, child: Padding(padding: const EdgeInsets.all(14), child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: const [Text('مبيعات اليوم:', style: TextStyle(color: Colors.white, fontSize: 16)), Text('45,000 ر.ي', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold))]))),
          ],
        ),
      ),
    );
  }
}

// تبويب الأنشطة
class ActivitiesTabScreen extends StatelessWidget {
  const ActivitiesTabScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('تتبع الأنشطة الميدانية'), backgroundColor: Colors.purple, foregroundColor: Colors.white),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: const [
          Card(child: ListTile(leading: Icon(Icons.location_on, color: Colors.purple), title: Text('زيارة صيدلية الشفاء'), subtitle: Text('تم تسليم الطلبية بنجاح'))),
        ],
      ),
    );
  }
}
