document.addEventListener('DOMContentLoaded', function() {
  var currentTab = 0; // Current tab is set to be the first tab (0)
  showTab(currentTab); // Display the current tab

  function showTab(n) {
    var x = document.getElementsByClassName("step");
    if (n < 0 || n >= x.length) {
      console.error("Invalid tab index:", n);
      return;
    }
    for (var i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    x[n].style.display = "block";
    document.getElementById("prevBtn").style.display = (n == 0) ? "none" : "inline";
    document.getElementById("nextBtn").innerHTML = (n == (x.length - 1)) ? "Submit" : "Next";
    fixStepIndicator(n);
  }

  function nextPrev(n) {
    console.log("nextPrev called with n:", n);
    var x = document.getElementsByClassName("step");
    console.log("Current tab index:", currentTab);
    console.log("Total steps:", x.length);
    if (n == 1 && !validateForm()) {
        console.log("Form validation failed");
        return false;
    }
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    console.log("New current tab index:", currentTab);
    if (currentTab >= x.length) {
        document.getElementById("symptomForms").submit(); // Final submission
        return false;
    }
    showTab(currentTab);
    
    // Auto-submit for non-final steps
    if (n == 1 && currentTab < x.length - 1) {
        document.getElementById("symptomForms").submit(); // Auto-submit on next
    }
}

  function validateForm() {
    console.log("validateForm called");
    var x, y, i, valid = true;
    x = document.getElementsByClassName("step");
    y = x[currentTab].getElementsByTagName("input");
    for (i = 0; i < y.length; i++) {
        if (y[i].value == "") {
            y[i].className += " invalid";
            valid = false;
        }
    }
    if (valid) {
        document.getElementsByClassName("stepIndicator")[currentTab].className += " finish";
    }
    console.log("Form validation result:", valid);
    return true;
  }

  function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("stepIndicator");
    for (i = 0; i < x.length; i++) {
      x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
  }
  

  // Common configuration for select2
  const select2Config = {
    tags: true,
    closeOnSelect: false,
    placeholder: 'Select Symptoms',
  };

  $(document).ready(function() {
      $('.body-system-select').select2(select2Config);
  });

  // Initialize multiselect
  $('#multiple-checkboxes').multiselect({
    includeSelectAllOption: true
  });
  
  document.getElementById('prevBtn').addEventListener('click', function() {
    nextPrev(-1);
  });
  document.getElementById('nextBtn').addEventListener('click', function() {
    nextPrev(1);
  });
});