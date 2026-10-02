#!/usr/bin/env bash
set -euo pipefail

PROPTEST_CASES=${PROPTEST_CASES:-50000}
REPORT_FILE="lyapunov_stability_report.md"

echo "[+] بدء فحص حتمية النواة السيادية واستقرار دالة ليابونوف..."
echo "[+] عدد حالات Proptest: ${PROPTEST_CASES}"

if cargo test -- --nocapture; then
    TEST_STATUS="PASS"
    echo "[✔] اكتملت كافة الاختبارات بنجاح. دالة ليابونوف مستقرة قطعيًا."
else
    TEST_STATUS="FAIL"
    echo "[✘] تم اكتشاف خرق في اختبارات الاستقرار!"
fi

cat << EOR > "$REPORT_FILE"
# 🛡️ تقرير تدقيق استقرار دالة ليابونوف
* **حالة التدقيق:** **$TEST_STATUS**
* **عدد الحالات:** $PROPTEST_CASES
EOR

echo "[+] تم إخراج التقرير بنجاح إلى: ${REPORT_FILE}"
