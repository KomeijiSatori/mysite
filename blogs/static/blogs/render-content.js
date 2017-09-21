function update_marked_truncate() {
    marked.setOptions({
           gfm: true,
           tables: true,
           breaks: true,
           pedantic: false,
           sanitize: true,
           smartLists: true,
           smartypants: false
       });
    $(".marked_truncate").each(function() {
        var content = $(this).text();
        var rendered_html = marked(content);
        var truncated_html = jQuery.truncate(rendered_html, {length: 120, words: false});
        $(this).html(truncated_html);
    });
    $(".blog_content").each(function() {
        var content = $(this).text();
        var rendered_html = marked(content);
        $(this).html(rendered_html);
    });
    $(".marked_truncate p:not(:has(img))").css("text-indent", "2em");
    $(".blog_content p:not(:has(img))").css("text-indent", "2em");
}

function color_to_ele(curEle, next)
{
    if (next.size() === 1)
    {
        if (curEle !== null)
        {
            curEle.removeClass("kb");
        }
        next.addClass("kb");
    }
}

$(document).ready(function () {
    update_marked_truncate();
});