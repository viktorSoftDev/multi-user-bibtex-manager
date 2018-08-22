$(document).ready(function() {
  $("#both").click(function() {
    var formData = $("#current_form").serialize();
    console.log(formData);
    $.ajax({
      type: "POST",
      url: url_string,
      data: formData
    }).done(function() {
      window.location.replace(redirect);
    });
  });
});
