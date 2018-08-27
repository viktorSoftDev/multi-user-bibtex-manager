$(document).ready(function() {
  $("#both").click(function() {
    $('#new_or_both').val('BOTH');
    console.log($('#new_or_both').val());
    $('#current_form').submit()
  });
});
