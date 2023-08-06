document.getElementById("expenseForm").addEventListener("submit", function(event) {
    var dateInput = document.getElementsByName("expense_date")[0];
    var datePattern = /^\d{4}-\d{2}-\d{2}$/;

    if (!datePattern.test(dateInput.value)) {
        alert("Invalid date format. Please use YYYY-MM-DD format.");
        event.preventDefault(); // Prevent form submission
    }
});