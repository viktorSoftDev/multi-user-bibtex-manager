
function get_form(){
  let v = $('#id_entry_type').val().toString();
  if (v < "------------") {
    document.getElementById('form2div').innerHTML = "";
    $('#submit_button').hide();
  }
  else {
    var formData = $('#record_form').serialize();
    $.ajax({
        type: 'GET',
        url: url_string,
        data: formData
    }).done(function (data) {
      document.getElementById('form2div').innerHTML = data;
    });
    $('#submit_button').show();

  }
};
  $(document).ready(function(){
    $('#id_entry_type').change(function(){
      get_form();
    });
  });
