// DOM (Document Object Model) รอจน DOMContentLoaded เกิดขึ้นจึงเรียกใช้ฟังก์ชันภายในที่กำหนด
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // ป้องกันการส่งฟอร์มตามปกติ

        Swal.fire({
            icon: 'success',
            title: 'สำเร็จ!',
            text: 'กรุณาตรวจสอบอีเมลของคุณเพื่อรีเซ็ตรหัสผ่าน',
            timer: 1500,
            showConfirmButton: false 
        }).then(() => {
            form.submit(); // ส่งฟอร์ม
        });
    });
});
