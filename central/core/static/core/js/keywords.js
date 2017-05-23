/**
 * Created by maksimkislenko on 23.05.17.
 */

$(document).ready(function () {
    $('#id_why').tagsinput({
        typeahead: {
            source: ['Покупки', 'Развлечения', 'Учёба', 'Общение', 'Поиск нужного', 'Быть в курсе', 'Медиа',
                'Хранение', 'Соревнование', 'Обмен']
        },
        tagClass: 'label-primary',
        afterSelect: function() {this.$element[0].value = "";}
    });
    $('#id_who').tagsinput({
        typeahead: {
            source: ['Дети', 'Школьники', 'Девочки', 'Родители', 'Пожилые', 'Молодёжь', 'Семьи', 'Все',
                'Программисты', 'Госслужащие', 'Медики', 'Учёные', 'Математики', 'Пары']
        },
        tagClass: 'label-success',
        afterSelect: function() {this.$element[0].value = "";}
    });
    $('#id_what').tagsinput({
        typeahead: {
            source: ['Вводят', 'Загружают', 'Листают', 'Читают', 'Лайкают', 'Комментируют', 'Играют', 'Решают',
                'Оставляют заявки']
        },
        tagClass: 'label-danger',
        afterSelect: function() {this.$element[0].value = "";}
    });
    $('.js-save').click(function () {
        var parent = $(this).parent();
        var url = parent.attr('data-url');
        $(this).attr('disabled', 'disabled');

        $.post(url, {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'why': $('#id_why').val(),
            'who': $('#id_who').val(),
            'what': $('#id_what').val()
        })
            .done(function (response) {
                if (response.status == 'OK') {
                    $(this).fadeOut(0, function () {
                        parent.find('span').html('Данные сохранены').fadeIn();
                    });
                }
            }.bind(this))
            .always(function () {
                $(this).removeAttr('disabled');
            }.bind(this));
    });
    function fillPreset(domEl, source) {
        if (source.length > 0) {
            for (var I = 0; I < source.length; I++) {
                domEl.tagsinput('add', source[I]);
            }
            domEl.tagsinput('refresh');
        }
    }
    fillPreset($('#id_why'), why_preset);
    fillPreset($('#id_who'), who_preset);
    fillPreset($('#id_what'), what_preset);
});