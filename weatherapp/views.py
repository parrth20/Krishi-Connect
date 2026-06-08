from django.shortcuts import render

from .services import build_farm_weather_advice, get_weather_summary


def input(request):
    return render(request, 'weather.html')


def result(request):
    city = request.POST.get('Cityname') or request.GET.get('Cityname') or ""
    summary = get_weather_summary(city)
    advice = build_farm_weather_advice(summary)

    return render(
        request,
        'wresult.html',
        {
            'city': city,
            'summary': summary,
            'advice': advice,
            'location': summary.get("location", {}) if summary else {},
            'current': summary.get("current", {}) if summary and not summary.get("error") else {},
            'daily': summary.get("daily", []) if summary and not summary.get("error") else [],
            'error': summary.get("error") if summary else None,
        },
    )
