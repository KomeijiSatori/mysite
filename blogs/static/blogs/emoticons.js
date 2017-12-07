function make_text(textarea, text) {
    var s = textarea.get(0).selectionStart;
    var e = textarea.get(0).selectionEnd;
    var val = textarea.get(0).value;
    textarea.get(0).value = val.substring(0, s) + text + val.substring(e);
    textarea.get(0).selectionStart = e + text.length;
    textarea.get(0).selectionEnd = e + text.length;
    textarea.focus();
}


$(document).ready(function () {
    $(".emoticon-img").hide();
    $(".emoticon-set").hide();

    $(".emoticon-div a").click(function() {
        function on_click(item)
        {
            // the first button to be clicked
            if (item.attr('data-selected') === undefined)
            {
                item.parent().next(".emoticon-img").show();
                cur_set.slideDown(500);
                item.parent().find("a").attr('data-selected', '0');
                item.attr("data-selected", '1');
            }
            // click from other button to the current button
            else if (item.attr('data-selected') === '0')
            {
                cur_set.slideDown(500);
                item.parent().next(".emoticon-img").show();
                item.parent().find("a").attr('data-selected', '0');
                item.attr("data-selected", '1');
            }
            // toggle the button
            else
            {
                cur_set.slideUp(500, function() {item.parent().next(".emoticon-img").hide()});
                item.parent().find("a").removeAttr('data-selected');
            }

            item.parent().find("a").attr('class', 'btn btn-default');
            item.parent().find("a[data-selected='1']").attr('class', 'btn btn-primary');
        }

        var emoticon_sets = $(this).parent().next(".emoticon-img").find(".emoticon-set");
        var cur_ind = parseInt($(this).attr("data-ind"));
        var cur_set = emoticon_sets.eq(cur_ind);
        var selected_btn = $(this).parent().find("a[data-selected='1']");

        if (selected_btn.length > 0)
        {
            var selected_set = emoticon_sets.eq(parseInt(selected_btn.attr("data-ind")));
            selected_set.slideUp(500, on_click($(this)));
        }
        else
        {
            on_click($(this));
        }
    });

    $(".emoticon-set img").click(function(){
        var set_name = $(this).parent().attr("data-emoticon_set_name");
        var file_name = $(this).attr("data-filename");
        var string = "[" + set_name + " " + file_name + "]";

        // find the nearest ``textarea`` above the current bar
        var textarea = $(this).closest("form").find("textarea")
        make_text(textarea, string);
    });
});