
$('.custom-control-input').on("change",function(){
    var $checkbox = $(this).find(':checkbox');
    var status = $(this).attr('data-merchant-status')
    var statusURL = $(this).attr('data-status-url')
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    var merchant_id = $(this).attr('data-merchant-id')

    if (status == 'Unblock'){
        $.ajax({
                url: statusURL,
                type:'post',
                data: {
                    'status': status,
                    'id':merchant_id,
                    'csrfmiddlewaretoken':csrf,
                },
                success: function (data) {
                    $(this).attr('data-merchant-status',data)
                }
            });
    }else{
        $.ajax({
                url: statusURL,
                type:'post',
                data: {
                    'status': status,
                    'id':merchant_id,
                    'csrfmiddlewaretoken':csrf,
                },
                success: function (data) {
                    $(this).attr('data-merchant-status',data)
                }
            });
    }

});



var clickHandler = function(e){
    var url = $('#forgot_password_form').attr('data-url');
    var email = $('.email_password_forget').val();
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    console.log("csrf",csrf)
    console.log("url",url)
    console.log("email",email)
    $('.email_password_forget').val('')

  $.ajax({
          url: url,
          type:"POST",
          data:{
            'email':email,
            'csrfmiddlewaretoken':csrf,
          },
          success: function(data){
            $('.forget_email_error').html(data)

          }
      });
    }
$(document).ready(function(){
  $('#loader').hide();
  $('.forgot_password_btn').on('click', clickHandler);
})