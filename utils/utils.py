from django.template.loader import render_to_string


def get_date_with_template_format(date_to_show):
    return render_to_string('utils/show_date.html', {'date_to_show': date_to_show})
