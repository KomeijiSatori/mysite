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
    $(".simple-image-div").css('display', '');
}

function show_background() {
    $(".hidden-xs").show();
    $(".simple-image-div").css('display', 'none');
}

function toggle_background() {
    if (!window.matchMedia('(max-width: 768px)').matches)
    {
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
}

var instrument_active = false;
var instrument_listener = null;
var octave_base = 4;
var note_span = 2;
var instrument = 0;

var keymap = {
    'q': 'C -1',
    'w': 'D -1',
    'e': 'E -1',
    'r': 'F -1',
    't': 'G -1',
    'y': 'A -1',
    'u': 'B -1',
    'i': 'C 0',
    'o': 'D 0',
    'p': 'E 0',
    '[': 'F 0',
    ']': 'G 0',
    'z': 'A 0',
    'x': 'B 0',
    'c': 'C 1',
    'v': 'D 1',
    'b': 'E 1',
    'n': 'F 1',
    'm': 'G 1',
    ',': 'A 1',
    '.': 'B 1',
    '2': 'C# -1',
    '3': 'D# -1',
    '5': 'F# -1',
    '6': 'G# -1',
    '7': 'A# -1',
    '9': 'C# 0',
    '0': 'D# 0',
    '=': 'F# 0',
    'a': 'G# 0',
    's': 'A# 0',
    'f': 'C# 1',
    'g': 'D# 1',
    'j': 'F# 1',
    'k': 'G# 1',
    'l': 'A# 1'
};

var key_state = {};

$(document).ready(function () {
    instrument_listener = new window.keypress.Listener;
    Synth.setVolume(0.4);
    var key_func_map = [];

    for (var key in keymap)
    {
        key_state[key] = false;

        key_func_map.push({
            "keys": key,
            "on_keydown": function(event)
            {
                var key = event.key.toLowerCase();
                if (key_state[key] === false)
                {
                    var cur_str = keymap[key];
                    var note = cur_str.split(" ")[0];
                    var oct = parseInt(cur_str.split(" ")[1]);
                    Synth.play(instrument, note, oct + octave_base, note_span);
                    key_state[key] = true;
                }
            },
            "on_keyup": function(event)
            {
                var key = event.key.toLowerCase();
                key_state[key] = false;
            }
        });
    }
    key_func_map.push({
        "keys": 'up',
        "on_keydown": function()
        {
            if (octave_base <= 6)
            {
                octave_base++;
            }
        }
    });
    key_func_map.push({
        "keys": 'down',
        "on_keydown": function()
        {
            if (octave_base >= 2)
            {
                octave_base--;
            }
        }
    });
    key_func_map.push({
        "keys": 'left',
        "on_keydown": function()
        {
            if (instrument >= 1)
            {
                instrument--;
            }
        }
    });
    key_func_map.push({
        "keys": 'right',
        "on_keydown": function()
        {
            if (instrument <= 2)
            {
                instrument++;
            }
        }
    });

    instrument_listener.register_many(key_func_map);
    instrument_listener.stop_listening();
});


function toggle_keyboard()
{
    if (instrument_active === false)
    {
        instrument_active = true;
        instrument_listener.listen();
    }
    else if (instrument_active === true)
    {
        instrument_active = false;
        instrument_listener.stop_listening();
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
    key_listener.sequence_combo("! @ #", toggle_keyboard, true);

    $("input[type=text], textarea")
    .bind("focus", function() { key_listener.stop_listening(); })
    .bind("blur", function() { key_listener.listen(); });

    var is_animated_background = Cookies.get("animated_background");
    if (is_animated_background === "true")
    {
        show_background();
    }
    else
    {
        hide_background();
    }

    get_notification_count();

    // for textarea and input effect
    POWERMODE.colorful = true; // make power mode colorful
    POWERMODE.shake = false; // turn off shake
    document.body.addEventListener('input', POWERMODE);
    document.body.addEventListener('textarea', POWERMODE);
});
