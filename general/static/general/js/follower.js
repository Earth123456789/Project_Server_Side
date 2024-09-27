let isFollowing = false; 

function follow(userId, eventId, csrf_token, button) {
    const action = isFollowing ? 'DELETE' : 'PUT';

    fetch(`/event/${eventId}/followers/${userId}/`, {
        method: action,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token, 
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        if (action === 'PUT') {
            isFollowing = true; 
            button.querySelector('p').innerText = 'กำลังติดตาม'; 
        } else {
            isFollowing = false; 
            button.querySelector('p').innerText = 'ติดตาม'; 
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}