#![no_std]
#![no_main]

use core::ffi::c_void;
use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

pub static LICENSE: [u8; 4] = [b'G', b'P', b'L', 0];

#[no_mangle]
pub extern "C" fn aqi_xdp_filter(ctx: *mut c_void) -> u32 {
    let _ = ctx;
    0
}
