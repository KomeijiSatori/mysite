$(document).ready(function () {
    $("#author").on('click', function() {
        $("#profile-modal").show();
    });

    $(".close").on('click', function() {
        $("#profile-modal").hide();
    });

    $("#profile-close").on('click', function() {
        $("#profile-modal").hide();
    });
});

