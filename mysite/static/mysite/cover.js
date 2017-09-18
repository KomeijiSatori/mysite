hljs.initHighlightingOnLoad();

function get_notification_count() {
    var ajax_url = $('#unread-notifications').attr("data-ajax-url");
    $.ajax({
        type: "GET",
        url: ajax_url,
        success: function(result) {
            var count = result['count'];
            if (count > 0)
            {
                $('#unread-notifications').html(count);
            }
            else
            {
                $('#unread-notifications').html("");
            }
        }
    });
}


// key press functions
function toggle_content() {
    $("#main-content").toggle();
    $("#navigation-bar").toggle();
}

function hide_background() {
    $(".hidden-xs").hide();
    $("body").css("background", "url('/static/mysite/images/background.png')");
}

function show_background() {
    $(".hidden-xs").show();
    $("body").css("background", "black");
}

function toggle_background() {
    if ($(".hidden-xs").is(":visible"))
    {
        hide_background();
        Cookies.set("animated_background", false, { expired: 14 });
    }
    else
    {
        show_background();
        Cookies.set("animated_background", true, { expired: 14 });
    }
}

$(document).ready(function () {
    /* for go top */
    jQuery(window).scroll(function(){jQuery(this).scrollTop()>200?jQuery("#zan-gotop").css({bottom:"20px"}):jQuery("#zan-gotop").css({bottom:"-40px"})});
    jQuery("#zan-gotop").click(function(){return jQuery("body,html").animate({scrollTop:0},500),!1});

    // for key_listener
    var key_listener = new window.keypress.Listener;
    key_listener.sequence_combo("up up down down left right left right b a", toggle_content, true);
    key_listener.sequence_combo("left up right down", toggle_background, true);

    var is_animated_background = Cookies.get("animated_background");
    if (is_animated_background === "false")
    {
        hide_background();
    }

    get_notification_count();

});
