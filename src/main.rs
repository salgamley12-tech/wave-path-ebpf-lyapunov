#![no_std]
#![no_main]

use core::ffi::c_void;
use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

pub static LICENSE: [u8; 4] = [b'G', b'P', b'L', 0];



pub const XDP_ABORTED: u32 = 0;
pub const XDP_DROP: u32 = 1;
pub const XDP_PASS: u32 = 2;
pub const XDP_TX: u32 = 3;
pub const XDP_REDIRECT: u32 = 4;

/// هيكل سياق حزمة الشبكة (XDP Context)
#[repr(C)]
pub struct XdpMd {
    pub data: u32,
    pub data_end: u32,
    pub data_meta: u32,
    pub ingress_ifindex: u32,
    pub rx_queue_index: u32,
}

/// هيكل ترويسة الإيثرنت (Ethernet Header - 14 Bytes)
#[repr(C, packed)]
pub struct EthHeader {
    pub dst_mac: [u8; 6],
    pub src_mac: [u8; 6],
    pub ethertype: u16,
}

#[no_mangle]
pub extern "C" fn aqi_xdp_filter(ctx: *mut XdpMd) -> u32 {
    if ctx.is_null() {
        return XDP_PASS;
    }

    unsafe {
        let data = (*ctx).data as usize;
        let data_end = (*ctx).data_end as usize;

        // التحقق من حدود ترويسة الإيثرنت لمنع قراءة الذاكرة العشوائية
        let eth_hdr_size = core::mem::size_of::<EthHeader>();
        if data + eth_hdr_size > data_end {
            return XDP_PASS; // تمرير الحزم الأصغر من حجم الترويسة بأمان
        }

        // تحويل مؤشر البيانات إلى هيكل ترويسة الإيثرنت
        let eth = &*(data as *const EthHeader);
        
        // قراءة نوع البروتوكول وتحويله من ترتيب بايتات الشبكة (Network Byte Order)
        let ethertype = u16::from_be(eth.ethertype);

        // مثال على التصفية السيادية:
        // EtherType 0x0800 يمثل بروتوكول IPv4
        // يمكننا تطبيق قواعد الفلترة هنا (مثلاً السماح أو فحص الحزم بدقة)
        if ethertype == 0x0800 {
            // الحزمة من نوع IPv4 - مسموح لها بالعبور للمستوى التالي
            return XDP_PASS;
        }
    }

    // افتراضياً نسمح بباقي الحزم أو نطبق سياسة حظر مخصصة
    XDP_PASS
}
