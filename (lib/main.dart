import 'package:flutter/material.dart';

void main() {
  runApp(const ProofOfCapabilityApp());
}

class ProofOfCapabilityApp extends StatelessWidget {
  const ProofOfCapabilityApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'إثبات القدرة - الماسترو',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.red,
        useMaterial3: true,
      ),
      home: const ProofScreen(),
    );
  }
}

class ProofScreen extends StatefulWidget {
  const ProofScreen({super.key});

  @override
  State<ProofScreen> createState() => _ProofScreenState();
}

class _ProofScreenState extends State<ProofScreen> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('اختبار إثبات القدرة - الماسترو'),
        centerTitle: true,
        backgroundColor: Colors.red,
        foregroundColor: Colors.white,
      ),
      body: Container(
        color: Colors.red.shade50,
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.verified, size: 80, color: Colors.red),
                const SizedBox(height: 20),
                const Text(
                  'تم إثبات نجاح المنصة والبناء بنجاح تام!',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.redAccent),
                ),
                const SizedBox(height: 10),
                const Text(
                  'هذا التطبيق يثبت قدرة الفريق والماسترو على السيطرة الكاملة وتحديث الواجهات.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 14, color: Colors.black54),
                ),
                const SizedBox(height: 30),
                Card(
                  elevation: 6,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      children: [
                        const Text('عدد التفاعلات الناجحة:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 10),
                        Text(
                          '$_counter',
                          style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.red),
                        ),
                        const SizedBox(height: 15),
                        ElevatedButton.styleFrom().let((_) => ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 12),
                          ),
                          onPressed: _incrementCounter,
                          child: const Text('اضغط لاختبار الاستجابة الفورية', style: TextStyle(fontSize: 16)),
                        )),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

extension on ButtonStyle {
  Widget let(Widget Function(ButtonStyle) callback) => callback(this);
}
