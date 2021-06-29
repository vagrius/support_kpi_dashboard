from django.db.models import Sum, Avg
from django.shortcuts import render
from django.views import View

from kpiapp.models import Request, Company


class MainView(View):

    def get(self, request, *args, **kwargs):
        months = {
            '5': 'Май',
            '4': 'Апрель'
        }
        count = 0
        context = {
            'kpis_by_month': []
        }
        for key, value in months.items():
            reqs_by_month = Request.objects.filter(date_time__month=key)

            companies = reqs_by_month.values('company', 'url_uid').distinct()

            new_dict = {
                    'month': value,
                    'month_id': f'month{key}',
                    'kpis': [],
                    'general_info': {
                        'reqs_count': reqs_by_month.count(),
                        'clients_count': reqs_by_month.values('company').distinct().count(),
                        'unanswered_reqs_count': reqs_by_month.filter(specialist='').count(),
                    },
                    'general_info_id': f'general_month{key}',
                    'companies': companies,
                    'companies_pool_id': f'companies_month{key}'
                }
            specs = Request.objects.values('specialist').distinct()
            for spec in specs:
                reqs = reqs_by_month.filter(specialist=spec['specialist'])
                if spec['specialist']:
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
            context['kpis_by_month'].append(new_dict)
            count += 1
        return render(request, "index.html", context=context)
