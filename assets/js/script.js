$(function () {
    // enable navigation toggle
    $('.nav-toggle').on('click', function(e) {
      e.preventDefault();
      var toggle = $(e.target);
      var target = $(toggle.data('target'));

      if (target.length) {
        toggle.toggleClass('active');
        target.toggleClass('active');
      }
    });

    // focus on search input with '/' key.
    $("body").on("keyup", function (e) {
        e.stopPropagation();
        var slashKeys = [47, 111, 191];
        if (slashKeys.some(function (value) { return e.keyCode == value })) {
            $("#search").focus();
        }
    });

    // add `target="_blank"` into all outer links.
    var host = document.location.host;
    $("a[href]").each(function() {
        var re = new RegExp(host, "g");
        if ($(this).attr("href").match(/\/\//) && !$(this).attr("href").match(re)) {
            $(this).attr("target", "_blank");
        }
    });

    // center and linkable all images.
    var $images = $("article img:not(.emoji, .eye-catch)");
    $images.closest("p").css("text-align", "center");
    $images.each(function () {
        var imgUrl = $(this).attr("src");
        var $a = $("<a>").attr("href", imgUrl).attr("target", "_blank", "noopener");
        $(this).wrap($a);
    });

    // stick aside.
    var topSpacing = $(".site-aside").css("padding-top").replace(/px/, "");
    $(".site-aside .sticky").sticky({
        topSpacing: parseInt(topSpacing)
    });
});
