$(document).ready(function () {
    $('.js-add-form').magnificPopup({
        items: {
            src: '#add-modal',
            type: 'inline'
        }
    });
    $('#js-form-site').submit(function () {
        event.preventDefault();
        $('.error').fadeOut();
        $.post($(this).attr('action'), $(this).serialize())
            .done(function (response) {
                console.log(response);
                if (response.status === 'OK') {
                    $('.no-sites').fadeOut('fast');

                    $('.js-sites').prepend(_.template(
                        $('#site-item-tml').html()
                    )(response.data));
                    $.magnificPopup.close();
                }
                else if (response.status === 'ERROR') {
                    var errors = response.errors;
                    for (var field in errors) {
                        if (errors.hasOwnProperty(field)) {
                            $(this).find('.error-' + field).html(errors[field]).fadeIn();
                        }
                    }
                }
            }.bind(this)).fail(function (xhr, responseText) {});
    });
});
