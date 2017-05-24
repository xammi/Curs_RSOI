{% load core_tags %}

$(function () {
    var p = "{{ site_url }}{% url 'core:adv' %}?site={{ site|key:'id' }}";
    $.get(p).done(function (r) {
        var inEl = $('.targeto');
        if (inEl.length === 0) {
            inEl = $('<div class="targeto"></div>');
            $('body').prepend(inEl);
        }
        inEl.html(r.html);
    });
});