function validateExpenseDate() {
    var dateInput = document.getElementsByName("expense_date")[0];
    var datePattern = /^\d{4}-\d{2}-\d{2}$/;

    if (!datePattern.test(dateInput.value)) {
        alert("Invalid date format. Please use YYYY-MM-DD format.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

document.getElementById("expenseForm").addEventListener("submit", function(event) {
    if (!validateExpenseDate()) {
        event.preventDefault(); // Prevent form submission
    }
});