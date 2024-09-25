function toggleDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('hidden'); 
}


window.onclick = function(event) {
    const dropdown = document.getElementById('profileDropdown');
    if (!event.target.matches('.cursor-pointer')) {
        if (!dropdown.classList.contains('hidden')) {
            dropdown.classList.add('hidden');
        }
    }
}