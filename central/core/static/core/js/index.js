$(document).ready(function () {
    $('#fullpage').fullpage({
        sectionsColor: ['#1bbc9b', '#4BBFC3', '#7BAABE', '#ccddff'],
        anchors: ['main', 'adviser', 'site-owner', 'use-it'],
        menu: '#left-navbar',
        scrollBar: true
    });
    $('.js-adviser-reg').magnificPopup({
        items: { src: '#adviser-modal', type: 'inline' }
    });
    $('.js-site-owner-reg').magnificPopup({
        items: { src: '#site-owner-modal', type: 'inline' }
    });
    $('#js-more').click(function () {
        $.fn.fullpage.moveSectionDown();
    });
    $('.js-login-form').submit(function (event) {
        event.preventDefault();
        $.post($(this).attr('action'), $(this).serialize())
            .done(function (response) {
                console.log(response);
                if (response.status === 'OK') {
                    location.replace(response.success_url);
                } else {
                    $('.error-email').html(response.errors).fadeIn().delay(2000).fadeOut();
                }
            }.bind(this))
            .fail(function (xhr, responseText) {});
    });
    $('.js-register').submit(function (event) {
        event.preventDefault();
        $('.error').fadeOut();
        $.post($(this).attr('action'), $(this).serialize())
            .done(function (response) {
                console.log(response);
                if (response.status === 'OK') {
                    location.replace(response.success_url);
                } else {
                    var errors = response.errors;
                    for (var field in errors) {
                        if (errors.hasOwnProperty(field)) {
                            $(this).find('.error-' + field).html(errors[field]).fadeIn();
                        }
                    }
                }
            }.bind(this))
            .fail(function (xhr, responseText) {});
    });
});