$(function() {

  $("#executeFormDiv").hide();

  $("#commandSelect").on('change', function(){
    if(this.value != 0){
        $("#executeFormDiv").show();
    }else{
        $("#executeFormDiv").hide();
    }
  });

  $('#commandSelect').append('<option value="0">Select Command</option>');

  $.ajax({
    url: "././commands",
    type: "GET",
    cache: false,
    success: function(result) {
        for(var i=0; i < result["commands"].length; i++){
            var name = result["commands"][i]["name"];
            var id = i + 1;
            $('#commandSelect').append('<option value="' + id + '">' + name + '</option>');
        };
    },
    error: function() {
        
    },
    complete: function() {
      setTimeout(function() {
        $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
      }, 1000);
    }
  });

  $("#contactForm input,#contactForm select").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      var command = $("#commandSelect").val();
      var args = $("#args").val();
      $this = $("#sendMessageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "././execute/" + command,
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
          args: args
        }),
        cache: false,
        success: function(result) {
          var message = result["message"];
          var status = result["status"];
          if(status == "success"){
              $('#success').html("<div class='alert alert-success'>");
              $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                .append("</button>");
              $('#success > .alert-success')
                .append("<strong>The command is executed successfully. Message: </strong> " + message);
              $('#success > .alert-success')
                .append('</div>');
              //clear all fields
              $('#contactForm').trigger("reset");
          }else{
              $('#success').html("<div class='alert alert-danger'>");
              $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                .append("</button>");
              $('#success > .alert-danger').append($("<strong>").text("Something went wrong, Message: " + message));
              $('#success > .alert-danger').append('</div>');
              //clear all fields
              $('#contactForm').trigger("reset");
          }
        },
        error: function() {
          // Fail message
          $('#success').html("<div class='alert alert-danger'>");
          $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-danger').append($("<strong>").text("Sorry it seems that the backend server is not responding. Please try again later!"));
          $('#success > .alert-danger').append('</div>');
          //clear all fields
          $('#contactForm').trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});
