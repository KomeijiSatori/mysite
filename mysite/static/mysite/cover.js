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

$(document).ready(function () {
    /* for go top */
    jQuery(window).scroll(function(){jQuery(this).scrollTop()>200?jQuery("#zan-gotop").css({bottom:"20px"}):jQuery("#zan-gotop").css({bottom:"-40px"})});
    jQuery("#zan-gotop").click(function(){return jQuery("body,html").animate({scrollTop:0},500),!1});

    get_notification_count();

});

