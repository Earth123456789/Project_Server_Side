document.addEventListener("DOMContentLoaded", function () {
    const quantitySelect = document.getElementById("ticket-quantity");
    const totalPriceElement = document.getElementById("total-price");
    const ticketPrice = parseFloat(totalPriceElement.dataset.price); // เอา attibute  data-price="{{ event.ticket_price }}"


    function updateTotalPrice() {
        const quantity = parseInt(quantitySelect.value);
        const totalPrice = quantity * ticketPrice;
        totalPriceElement.textContent = `ราคารวม: ${totalPrice.toFixed(2)} บาท`;
    }

    quantitySelect.addEventListener("change", updateTotalPrice);


    updateTotalPrice();
});
