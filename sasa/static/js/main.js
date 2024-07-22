document.addEventListener('DOMContentLoaded', function() {
  var currentTab = 0; // Current tab is set to be the first tab (0)
  showTab(currentTab); // Display the current tab

  function showTab(n) {
      var steps = document.querySelectorAll(".step");
      var forms = [document.getElementById("symptomFormStep1"), document.getElementById("symptomFormStep2")];

      if (n < 0 || n >= steps.length) {
          console.error("Invalid tab index:", n);
          return;
      }

      steps.forEach(function(step, index) {
          step.style.display = (index === n) ? "block" : "none";
      });

      forms.forEach(function(form, index) {
          form.style.display = (index === n) ? "block" : "none";
      });

      document.getElementById("prevBtnStep2").style.display = (n == 0) ? "none" : "inline";
      document.getElementById("nextBtnStep2").innerHTML = (n == (steps.length - 1)) ? "Submit" : "Next";
      fixStepIndicator(n);
  }

  function nextPrevStep1(n) {
      console.log("nextPrevStep1 called with n:", n);
      var steps = document.querySelectorAll(".step");
      if (n == 1 && !validateFormStep1()) {
          console.log("Form validation failed");
          return false;
      }
      currentTab = currentTab + n;
      if (currentTab >= steps.length) {     
          document.getElementById("symptomFormStep1").submit(); // Final submission for Step 1
          return false;
      }
      showTab(currentTab);
  }

  function nextPrevStep2(n) {
      console.log("nextPrevStep2 called with n:", n);
      var steps = document.querySelectorAll(".step");
      if (n == 1 && !validateFormStep2()) {
          console.log("Form validation failed");
          return false;
      }
      currentTab = currentTab + n;
      if (currentTab >= steps.length) {
          document.getElementById("symptomFormStep2").submit(); // Final submission for Step 2
          return false;
      }
      showTab(currentTab);
  }

  function submitFormStep1() {
      document.getElementById("symptomFormStep1").submit();
  }

  function validateFormStep1() {
      console.log("validateFormStep1 called");
      var valid = true;
      // Add specific validation logic for Step 1 here
      console.log("Form validation result:", valid);
      return valid;
  }

  function validateFormStep2() {
      console.log("validateFormStep2 called");
      var valid = true;
      // Add specific validation logic for Step 2 here
      console.log("Form validation result:", valid);
      return valid;
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

  document.getElementById('nextBtnStep1').addEventListener('click', function() {
      nextPrevStep1(1);
  });
  document.getElementById('prevBtnStep2').addEventListener('click', function() {
      nextPrevStep2(-1);
  });
  document.getElementById('nextBtnStep2').addEventListener('click', function() {
      nextPrevStep2(1);
  });
});