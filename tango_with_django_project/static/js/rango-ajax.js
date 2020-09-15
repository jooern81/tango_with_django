$(document).ready( function() {

$("#about-btn").click( function(event) {
    alert("Don't click buttons randomly!");
    });


$(".img-circle").click( function(event) {
    alert("You clicked me! ouch!");
    });

$("p").hover( function() {
    $(this).css('color', 'red');
    },
    function() {
    $(this).css('color', 'blue');
    });

$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like', {category_id: catid}, function(data){
    $('#like_count').html(data);
    $('#likes').hide();
    });
    });
});