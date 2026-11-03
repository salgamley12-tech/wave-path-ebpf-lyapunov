#![no_std]
#![no_main]

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

#[repr(C)]
pub struct XdpMd {
    pub data: u32,
    pub data_end: u32,
    pub data_meta: u32,
    pub ingress_ifindex: u32,
    pub rx_queue_index: u32,
}

#[repr(C, packed)]
pub struct EthHeader {
    pub dst_mac: [u8; 6],
    pub src_mac: [u8; 6],
    pub ethertype: u16,
}

#[no_mangle]
pub extern "C" fn aqi_xdp_filter(ctx: *const XdpMd) -> u32 {
    if ctx.is_null() {
        return XDP_PASS;
    }

    unsafe {
        let data = (*ctx).data as usize;
        let data_end = (*ctx).data_end as usize;

        let eth_hdr_size = core::mem::size_of::<EthHeader>();
        if data + eth_hdr_size > data_end {
            return XDP_PASS;
        }

        let eth = &*(data as *const EthHeader);
        let ethertype = u16::from_be(eth.ethertype);

        if ethertype == 0x0800 {
            return XDP_PASS;
        }
    }

    XDP_PASS
}
