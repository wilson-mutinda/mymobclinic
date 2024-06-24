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
    if (n == 0) {
      document.getElementById("prevBtn").style.display = "none";
    } else {
      document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
      document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
      document.getElementById("nextBtn").innerHTML = "Next";
    }
    fixStepIndicator(n);
  }

  function nextPrev(n) {
    var x = document.getElementsByClassName("step");
    if (n == 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {
      document.getElementById("signUpForm").submit();
      return false;
    }
    showTab(currentTab);
  }

  function validateForm() {
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
    return valid;
  }

  function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("stepIndicator");
    for (i = 0; i < x.length; i++) {
      x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
  }

  // Initialize select2
  $('#cardiovascularSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#respiratorySelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#gastrointestinalSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#neurologicalSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#musculoskeletalSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#dermatologicalSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  $('#psychiatricSelect').select2({
    placeholder: 'Select Symptoms',
    tags: true,
    closeOnSelect: false,
    tokenSeparators: [',', ' ']
  });

  // Initialize multiselect
  $('#multiple-checkboxes').multiselect({
    includeSelectAllOption: true
  });

  // Attach event listeners to buttons
  document.getElementById('prevBtn').addEventListener('click', function() {
    nextPrev(-1);
  });
  document.getElementById('nextBtn').addEventListener('click', function() {
    nextPrev(1);
  });
});
