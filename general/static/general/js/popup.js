function showLoginAlert() {
    Swal.fire({
        title: 'โปรดเข้าสู่ระบบ',
        text: 'คุณต้องเข้าสู่ระบบเพื่อดำเนินการต่อ',
        icon: 'warning',
        timer: 1000,
        showConfirmButton: false,
        showCancelButton: false,
    })
}


function showData(company) {
    Swal.fire({
        title: 'ข้อมูลบริษัท',
        html: `
            <div class="space-y-4"> 
                <div class="flex flex-col"> 
                    <h1 class='kanit-black underline text-left'>ชื่อบริษัท:</h1>
                    <p class='kanit-regular mt-2 text-left'>${company.name}</p>
                </div>
                <div class="flex flex-col"> 
                    <h1 class='kanit-black underline text-left'>อีเมล:</h1>
                    <p class='kanit-regular mt-2 text-left'>${company.email}</p>
                </div>
                <div class="flex flex-col"> 
                    <h1 lass='kanit-black underline text-left'>ช่องทางติดต่ออื่นๆ:</h1>
                    <p class='kanit-regular mt-2 text-left'>${company.contact}</p>
                </div>
                <div class="flex flex-col"> 
                    <h1 class='kanit-black underline text-left'>เบอร์โทรศัพท์:</h1>
                    <p class='kanit-regular mt-2 text-left'>${company.phone}</p>
                </div>
            </div>
        `,
        icon: 'info',
        confirmButtonText: 'ปิด',
        confirmButtonColor: "#d33"
    });
}
