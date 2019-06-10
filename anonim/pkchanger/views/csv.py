from django.http import HttpResponse


def import_csv(request, path):
    with open(path, 'wb+') as destination:
        for chunk in request.FILES['file'].chunks():
            destination.write(chunk)


def export_csv(dataframe):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    dataframe.to_csv(
        path_or_buf=response,
        sep=';',
        float_format='%.2f',
        index=False,
        decimal=",")
    return response
