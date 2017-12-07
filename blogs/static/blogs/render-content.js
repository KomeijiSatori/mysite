// render all content to markdown and emoji etc.
function render_content(text)
{
    // first default markdown render
    var renderer = new marked.Renderer();
    renderer.code = function (code, language) {

        return '<pre class="prettyprint"><code class="hljs">' + hljs.highlightAuto(code).value +
            '</code></pre>';
    };

    var html = marked(text, { renderer: renderer });
    // render the emoji
    html = html.replace(/\[\[([^ \[\]]+?) ([^ \[\]]+?)]]/g, '<img src="/media/emoticon/$1/$2">');
    return html;
}

function update_marked_truncate() {
    $(".marked_truncate").each(function() {
        var content = $(this).text();
        var rendered_html = render_content(content);
        var truncated_html = jQuery.truncate(rendered_html, {length: 120, words: false});
        $(this).html(truncated_html);
    });
    $(".marked_content").each(function() {
        var content = $(this).text();
        var rendered_html = render_content(content);
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
    marked.setOptions({
        gfm: true,
        tables: true,
        breaks: true,
        pedantic: false,
        sanitize: true,
        smartLists: true,
        smartypants: false
    });
    update_marked_truncate();
});