hljs.initHighlightingOnLoad();
$(document).ready(function () {
    /* for go top */
    jQuery(window).scroll(function(){jQuery(this).scrollTop()>200?jQuery("#zan-gotop").css({bottom:"20px"}):jQuery("#zan-gotop").css({bottom:"-40px"})});
    jQuery("#zan-gotop").click(function(){return jQuery("body,html").animate({scrollTop:0},500),!1});
})

