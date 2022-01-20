from django.db.models import Sum, Avg
from django.shortcuts import render
from django.views import View

from kpiapp.models import Request, Update


class MainView(View):

    def get(self, request, *args, **kwargs):
        source_dates = Request.objects.values('date_time')
        years = {}
        months_source = {
            '12': 'Декабрь',
            '11': 'Ноябрь',
            '10': 'Октябрь',
            '9': 'Сентябрь',
            '8': 'Август',
            '7': 'Июль',
            '6': 'Июнь',
            '5': 'Май',
            '4': 'Апрель',
            '3': 'Март',
            '2': 'Февраль',
            '1': 'Январь'
        }
        for date in source_dates:
            if not str(date['date_time'].year) in years:
                years[str(date['date_time'].year)] = [str(date['date_time'].month)]
            else:
                if not str(date['date_time'].month) in years[str(date['date_time'].year)]:
                    years[str(date['date_time'].year)].append(str(date['date_time'].month))

        context = {
            'kpis_by_year': []
        }

        for year in years:
            months = {}
            for number in years[year]:
                months[number] = months_source[number]

            kpis_by_month = {
                'year': year,
                'year_id': f'year{year}',
                'kpis_by_month': []
            }
            reqs_by_year = Request.objects.filter(date_time__year=year)

            for key, value in months.items():
                reqs_by_month = reqs_by_year.filter(date_time__month=key)

                companies = reqs_by_month.values('company', 'url_uid', 'date_time').order_by('date_time')

                new_dict = {
                        'month': value,
                        'month_id': f'month{key}{year}',
                        'kpis': [],
                        'general_info': {
                            'reqs_count': reqs_by_month.count(),
                            'clients_count': reqs_by_month.values('company').distinct().count(),
                        },
                        'general_info_id': f'general_month{key}{year}',
                        'companies': companies,
                        'companies_pool_id': f'companies_month{key}{year}'
                    }
                specs = Request.objects.values('specialist').distinct()
                for spec in specs:
                    reqs = reqs_by_month.filter(specialist=spec['specialist'])
                    if spec['specialist'] and reqs:
                        kpis_of_spec = {
                            'reqs_count': reqs.count(),
                            'dec_in_time': reqs.aggregate(sum=Sum('dec_in_time'))['sum'],
                            'react_count': reqs.aggregate(sum=Sum('reactions_count'))['sum'],
                            'react_in_time_count': reqs.aggregate(sum=Sum('reactions_in_time_count'))['sum'],
                            'dec_time_avg': round(reqs.aggregate(avg=Avg('decision_time'))['avg'], 2),
                            'react_time_avg': round(reqs.aggregate(avg=Avg('reactions_average'))['avg'], 2),
                            'dec_time_perc': round(reqs.aggregate(sum=Sum('dec_in_time'))['sum'] / reqs.count() * 100, 2),
                            'react_speed_perc': round(reqs.aggregate(sum=Sum('reactions_in_time_count'))['sum'] / reqs.aggregate(sum=Sum('reactions_count'))['sum'] * 100, 2),
                        }
                        new_dict['kpis'].append({
                            'spec_name': spec['specialist'],
                            'kpis_of_spec': kpis_of_spec,
                        })
                kpis_by_month['kpis_by_month'].append(new_dict)
            context['kpis_by_year'].append(kpis_by_month)
            context['update_date_time'] = Update.objects.values('date_time').last()
        return render(request, "index.html", context=context)
