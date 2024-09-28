let isFollowing = false;

function updateButtonText(button) {
    const buttonText = button.querySelector('p'); // เลือก <p>
    buttonText.innerText = isFollowing ? 'กำลังติดตาม' : 'ติดตาม'; 
}

function follow(userId, eventId, csrf_token, button) {
    const action = isFollowing ? 'DELETE' : 'PUT';

    // ดึง api มาใช้งานในฝั่ง front-end 
    fetch(`/event/${eventId}/followers/${userId}/`, {
        method: action,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
    })
    .then(response => {
        if (response.ok) {
            // ส่ง response เป็น  json
            return response.json();
        }
        throw new Error('Network not ok.');
    })
    .then(data => {
        isFollowing = !isFollowing;
        // ใช้ localStorage ในการเก็บข้อมูลเพื่อเวลา refresh หน้าข้อมูลยังคงไว้
        localStorage.setItem(`following-${eventId}`, isFollowing);
        updateButtonText(button);
        // เห็นข้อมูลได้ทันที
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('#follow-button'); // <id>
    const eventId = button.getAttribute('data-event-id'); // <เลือก data-event-id = ...>
    const storedFollowingStatus = localStorage.getItem(`following-${eventId}`); // ดึง localStorage ที่ set ไว้
    isFollowing = storedFollowingStatus === 'true';
    updateButtonText(button);
});
