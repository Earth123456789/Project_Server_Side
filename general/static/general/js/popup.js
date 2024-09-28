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
            <div class="space-y-6">
                <div class="flex flex-col">
                    <h1 class="kanit-black underline text-left text-xl">ชื่อบริษัท:</h1>
                    <p class="kanit-regular mt-1 text-left text-gray-700">${company.name}</p>
                </div>
                <div class="flex flex-col">
                    <h1 class="kanit-black underline text-left text-xl">อีเมล:</h1>
                    <p class="kanit-regular mt-1 text-left text-gray-700">${company.email}</p>
                </div>
                <div class="flex flex-col">
                    <h1 class="kanit-black underline text-left text-xl">ช่องทางติดต่ออื่นๆ:</h1>
                    <p class="kanit-regular mt-1 text-left text-gray-700">${company.contact}</p>
                </div>
                <div class="flex flex-col">
                    <h1 class="kanit-black underline text-left text-xl">เบอร์โทรศัพท์:</h1>
                    <p class="kanit-regular mt-1 text-left text-gray-700">${company.phone}</p>
                </div>
            </div>
        `,
        icon: 'info',
        confirmButtonText: 'ปิด',
        confirmButtonColor: "#d33"
    });
}
