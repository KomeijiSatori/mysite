$(document).ready(function() {
    AOS.init({
        duration: 1000,
        easing: 'ease-out-back'
    });
});

function move_to_ele(ele, time) {
    // scroll to ele
    if (ele.size() === 1)
    {
        var elOffset = ele.offset().top;
        var elHeight = ele.height();
        var windowHeight = $(window).height();
        var offset;

        if (elHeight < windowHeight) {
            offset = elOffset - ((windowHeight / 2) - (elHeight / 2));
        }
        else {
            offset = elOffset;
        }
        $('html, body').animate({
            scrollTop: offset
        }, time);
    }
}

// key `h j k l` item selection
// get current kb element
function getCurrentElement()
{
    var ele = $(".blog-div.kb");
    if (ele.size() != 1)
    {
        return null;
    }
    else
    {
        return ele;
    }
}

function movedown(time)
{
    var curEle = getCurrentElement();
    var next;
    // no item selected
    if (curEle === null)
    {
        next = $(".blog-div").first();
    }
    else
    {
        next = curEle.next(".blog-div");
    }
    // if not the last item
    color_to_ele(curEle, next);
    move_to_ele(next, time);
}

function moveup(time)
{
    var curEle = getCurrentElement();
    // no item selected
    if (curEle !== null)
    {
        var next = curEle.prev(".blog-div");
        color_to_ele(curEle, next);
        move_to_ele(next, time);
    }
}

function moveprev()
{
    var btn = $("#prev-btn");
    if (btn.size() === 1)
    {
        btn[0].click();
    }
}

function movenext()
{
    var btn = $("#next-btn");
    if (btn.size() === 1)
    {
        btn[0].click();
    }
}

$(document).ready(function () {
    var time = 100;
    var vim_key_listener = new window.keypress.Listener;
    vim_key_listener.simple_combo("j", function() {
        movedown(time);
    });
    vim_key_listener.simple_combo("k", function() {
        moveup(time);
    });
    vim_key_listener.simple_combo("h", function() {
        moveprev();
    });
    vim_key_listener.simple_combo("l", function() {
        movenext();
    });

    // when user is focus is writing a comment
    $("input[type=text], textarea")
    .bind("focus", function() { vim_key_listener.stop_listening(); })
    .bind("blur", function() { vim_key_listener.listen(); });
});