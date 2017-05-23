$(function () {
    var path = "{% url 'core:adv' %}?site={{ site.id }}";
    var imgTag = '<img src="' + path + '" alt="Targeto block"/>';
    $('.targeto').html(imgTag);
});