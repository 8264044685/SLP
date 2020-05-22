$(function(){
    $('.btn').click(function(){
        $('.btn.active').removeClass('active');
        $(this).addClass('active');
    });
});

$('.modal').on('click', {
   backdrop: 'static',
    keyboard: false,
});

$(".fa-times-circle").css('font-size', '40px');
$(".fa-times-circle").css('line-height', '60px');
