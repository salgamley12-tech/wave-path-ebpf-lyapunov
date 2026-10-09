# wave-path-ebpf-lyapunov: AQI Sovereign Kernel Architecture


---

## 1. الهيكل المعماري للمشروع (Project Structure)

```text
wave-path-ebpf-lyapunov/
 Cargo.toml                  # إعدادات وتبيعات مشروع Rust
 Makefile                    # أداة الأتمتة لبناء النظام والتحقق
 build/                      # مجلد مخرجات التجميع الثنائي (eBPF objects)
 proofs/                     # أدوات الإثبات والتحقق الرسمي
   ├── cbmc/                   # إثباتات لغة C وفحص الحدود (CBMC)
   ├── kani/                   # إثباتات خصائص Rust و Fail-Closed (Kani)
   └── scripts/                # سكربتات مساعدة للإثبات
 src/
    ├── ebpf/                   # كود مرشح النواة
    │   └── wave_filter.c       # مرشح XDP لفحص استقرار النظام وحزم الشبكة
    └── user/                   # مسار المستخدم (User-space Engine)
        └── main.rs             # حلقة التحكم ومحمل النواة السيادية
