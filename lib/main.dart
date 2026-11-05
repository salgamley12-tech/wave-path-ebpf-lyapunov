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
            const Card(
              child: ListTile(
                leading: Icon(Icons.person, color: Colors.blue),
                title: Text('المعرف الرئيسي'),
                subtitle: Text('sal'),
              ),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: ListView(
                children: const [
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.medical_services, color: Colors.green),
                      title: Text('إدارة المخزون والأدوية'),
                      trailing: Icon(Icons.arrow_forward_ios),
                    ),
                  ),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.account_balance_wallet, color: Colors.orange),
                      title: Text('سجل الحسابات والمبيعات'),
                      trailing: Icon(Icons.arrow_forward_ios),
                    ),
                  ),
                  Card(
                    child: ListTile(
                      leading: Icon(Icons.history, color: Colors.purple),
                      title: Text('تتبع الأنشطة الميدانية'),
                      trailing: Icon(Icons.arrow_forward_ios),
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
