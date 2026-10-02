#!/usr/bin/env bash
set -e

echo "==> [1/5] تحديث المستودع والتحقق من حالته..."
git pull origin main
git status

echo "==> [2/5] فحص إعدادات البناء (Cargo Check)..."
cargo check

echo "==> [3/5] تشغيل اختبارات الإصدار (Release Tests)..."
cargo test --release

echo "==> [4/5] تشغيل النواة السيادية التنفيذية..."
cargo run --release

echo "==> [5/5] اعتماد ورفع التعديلات إلى GitHub..."
git add .

if git diff-index --quiet HEAD --; then
    echo "ℹ️ لا توجد تعديلات جديدة لرفعها، شجرة العمل نظيفة والمستودع محدث تماماً."
else
    git commit -m "auto: sovereign pipeline update and verification $(date +'%Y-%m-%d %H:%M:%S')"
    git push origin main
    echo "🚀 تم رفع التعديلات بنجاح إلى GitHub!"
fi

echo "==> ✨ تم إنجاز الدورة الكاملة بنجاح واستقرار تام!"
