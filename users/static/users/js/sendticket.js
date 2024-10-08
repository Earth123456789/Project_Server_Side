function sendTicket(ticketId, userId, csrf_token) {
    Swal.fire({
        title: 'กรุณากรอกอีเมล',
        html: `
            <input type="email" id="email" class="kanit-regular bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="อีเมลของผู้รับ" required />
        `,
        showCancelButton: true,
        confirmButtonText: 'ส่ง',
        cancelButtonText: 'ยกเลิก',
        customClass: {
            confirmButton: 'kanit-regular bg-green-600 text-white hover:bg-green-700', 
            cancelButton: 'kanit-regular bg-red-600 text-white hover:bg-red-700' 
        },
        preConfirm: () => {
            const Email = document.getElementById('email').value;
            if (!Email) {
                Swal.showValidationMessage('กรุณากรอกอีเมล');
                return;
            }

            const url = `/user/ticket/${userId}/send/${ticketId}/`;

            return fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token,
                },
                // ส่ง request body เป็น JSON ex. { email: 65070@email.com }
                body: JSON.stringify({ email: Email })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(data => {
                Swal.fire({
                    title: 'สำเร็จ!',
                    text: 'ส่งตั๋วสำเร็จ! อย่าลืมบอกเพื่อนคุณล่ะ',
                    icon: 'success',
                    customClass: {
                        text: 'kanit-regular',
                        confirmButton: 'kanit-regular bg-green-600 text-white hover:bg-green-700', 
                    }
                });
            })
            .catch(error => {
                Swal.fire({
                    title: 'ผิดพลาด!',
                    text: 'โปรดตรวจสอบข้อมูลของคุณก่อนส่งอีกครั้ง',
                    icon: 'error',
                    customClass: {
                        text: 'kanit-regular',
                        confirmButton: 'kanit-regular bg-green-600 text-white hover:bg-green-700', 
                    }
                });
            });
        }
    });
}
