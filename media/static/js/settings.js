$(document).ready(function(){
    $("#reset_btn").click(function(){
        $('#profile_form input[type="text"]').val('');
        $('#profile_form #bio').val('');
    });
});