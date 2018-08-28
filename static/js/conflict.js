
function get_form(){
  let v = $('#id_entry_type').val().toString();
  if (v < "------------") {
    document.getElementById('form2div').innerHTML = "";
  }
  else {
    var formData = $('#current_form').serialize();
    $.ajax({
        type: 'GET',
        url: url_string,
        data: formData
    }).done(function (data) {
      document.getElementById('form2div').innerHTML = data;
    });
  }
};

$(document).ready(function() {
  $("#both").click(function() {
    $('#new_or_both').val('BOTH');
    $('#current_form').submit()
  });
  $('#id_entry_type').change(function(){
    console.log('change');
    get_form();
  });
});
