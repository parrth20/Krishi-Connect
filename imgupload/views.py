import os
import uuid
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
from .forms import ImageUploadForm
from .test01 import identify_plant
from .connection import *
from chatBackend.rag_service import (
    detect_disease,
    disease_answer,
    get_disease_profile,
    get_sample_cases,
    retrieve_documents,
)
from weatherapp.services import build_farm_weather_advice, get_weather_summary
import datetime


def _assistant_url(diagnosis, city=""):
    return "/assistant?%s" % urlencode(
        {
            "disease": diagnosis["slug"],
            "crop": diagnosis["crop"],
            "city": city or "",
        }
    )


def imgupload(request):
    return render(request, 'Plant.html', {"sample_cases": get_sample_cases()})


def result(request):
    return render(request, 'index.html')


def imageprocess(request):

    form = ImageUploadForm(request.POST, request.FILES)

    if form.is_valid():

        uploaded_file = request.FILES['image']
        img_path, img_url = handel_uploaded_file(uploaded_file)
        crop_hint = request.POST.get("crop_name", "")
        symptoms = request.POST.get("symptoms", "")
        city = request.POST.get("city", "")

        x = identify_plant([img_path])

        if x.get("error"):
            plant_name = crop_hint or "Uploaded crop"
            results = []
        else:
            plant_name = x.get("bestMatch", "") or crop_hint or "Uploaded crop"
            results = x.get("results", [])

        # ---------- Extract data from PlantNet response ----------
        if results:
            top = results[0]
            probability = [top.get("score", 0)]
            species = top.get("species", {})
            scientific_name = species.get("scientificName", "Unknown Plant")
            common_names = species.get("commonNames", [])
            family = species.get("family", {}).get("scientificNameWithoutAuthor", "")
            genus = species.get("genus", {}).get("scientificNameWithoutAuthor", "")
        else:
            probability = [0]
            scientific_name = crop_hint or "Unknown Plant"
            common_names = [crop_hint] if crop_hint else []
            family = ""
            genus = ""

        # dummy placeholders (since PlantNet doesn't provide these directly)
        pclass = ""
        kingdom = ""
        order = ""
        phylum = ""
        org_url = ""
        res_orginal = [common_names]
        res_value = probability
        diagnosis = detect_disease(
            crop_hint=crop_hint,
            symptoms=symptoms,
            filename=uploaded_file.name,
            plant_name=plant_name,
        )
        disease_docs = retrieve_documents(disease_answer(diagnosis), limit=3)
        sample_cases = get_sample_cases()
        dis_desc = [case["weather_risk"] for case in sample_cases]
        wiki_url = ["/assistant?disease=%s&crop=%s" % (case["slug"], case["crop"]) for case in sample_cases]
        similar_images = [static(case["sample_image"]) for case in sample_cases]
        name = [case["disease"] for case in sample_cases]

        # ---------- Confidence check ----------

        if results and probability[0] < 0.3:
            messages.error(request, 'Our Database did not find a confident match')
            return redirect(imgupload)

        # ---------- Database insert ----------

        try:
            for i in range(min(3, len(results))):

                species_i = results[i]["species"]

                plant = species_i.get("scientificName", "")
                score = results[i].get("score", 0)

                con = sql_connection()
                mycursor = con.cursor()

                query = "insert into plant values(%s,%s,%s,%s,now())"

                data = [plant_name, plant, score, 'bengluru']

                mycursor.execute(query, data)

                mycursor.close()
                con.commit()

        except:
            pass

        # ---------- Render result page ----------

        weather_summary = get_weather_summary(city) if city else None
        weather_advice = build_farm_weather_advice(weather_summary) if weather_summary else []

        return render(request, 'result.html', {
            'res_orginal': res_orginal,
            'res_value': probability[0],
            'img_url': img_url,
            'uploaded_img_url': img_url,
            'pclass': pclass,
            'family': family,
            'genus': genus,
            'kindom': kingdom,
            'order': order,
            'phylum': phylum,
            'org_url': org_url,
            'plant_name': plant_name,
            'common_names': common_names,
            'dis_desc': dis_desc,
            'wiki_url': wiki_url,
            'similar_images': similar_images,
            'name': name,
            'probability': probability,
            'diagnosis': diagnosis,
            'diagnosis_answer': disease_answer(diagnosis),
            'disease_docs': disease_docs,
            'confidence_percent': round(diagnosis.get("confidence", 0.5) * 100),
            'weather_summary': weather_summary,
            'weather_advice': weather_advice,
            'assistant_url': _assistant_url(diagnosis, city),
        })


def handel_uploaded_file(f):
    upload_dir = os.path.join(settings.BASE_DIR, "static", "Images", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(f.name)[1].lower() or ".jpg"
    file_name = "%s%s" % (uuid.uuid4().hex[:12], ext)
    file_path = os.path.join(upload_dir, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path, "/static/Images/uploads/%s" % file_name


def sample_diagnosis(request, slug):
    diagnosis = get_disease_profile(slug)
    if not diagnosis:
        messages.error(request, "Sample disease was not found")
        return redirect(imgupload)

    sample_cases = get_sample_cases()
    similar_images = [static(case["sample_image"]) for case in sample_cases]
    weather_summary = None
    city = request.GET.get("city", "")
    if city:
        weather_summary = get_weather_summary(city)

    return render(request, 'result.html', {
        'res_orginal': [[diagnosis["crop"]]],
        'res_value': diagnosis.get("confidence", 0.9),
        'img_url': static(diagnosis["sample_image"]),
        'uploaded_img_url': static(diagnosis["sample_image"]),
        'pclass': "",
        'family': diagnosis["crop"],
        'genus': "",
        'kindom': "",
        'order': "",
        'phylum': "",
        'org_url': "",
        'plant_name': diagnosis["crop"],
        'common_names': [diagnosis["crop"]],
        'dis_desc': [case["weather_risk"] for case in sample_cases],
        'wiki_url': ["/assistant?disease=%s&crop=%s" % (case["slug"], case["crop"]) for case in sample_cases],
        'similar_images': similar_images,
        'name': [case["disease"] for case in sample_cases],
        'probability': [diagnosis.get("confidence", 0.9)],
        'diagnosis': diagnosis,
        'diagnosis_answer': disease_answer(diagnosis),
        'disease_docs': retrieve_documents(disease_answer(diagnosis), limit=3),
        'confidence_percent': round(diagnosis.get("confidence", 0.5) * 100),
        'weather_summary': weather_summary,
        'weather_advice': build_farm_weather_advice(weather_summary) if weather_summary else [],
        'assistant_url': _assistant_url(diagnosis, city),
    })


def report(request):

    try:
        con = sql_connection()
        mycursor = con.cursor()

        query = """
        select d1,count(d1),round(avg(percentage)*100,2)
        from plant
        where uploaddate BETWEEN (NOW() - INTERVAL 7 DAY) AND NOW()
        group by d1
        order by 2 desc;
        """

        mycursor.execute(query)

        myresult = mycursor.fetchall()
        mycursor.close()
        con.close()
    except Exception:
        myresult = []
        return render(request, "report.html", {
            'zipped': [],
            'error': "Disease stats need the local MySQL database. The assistant, weather, upload, and sample diagnosis flows still work without it.",
        })

    name = []
    frequency = []
    percentage = []

    for x in myresult:
        name.append(x[0])
        frequency.append(x[1])
        percentage.append(x[2])

    zipped = zip(name, frequency, percentage)

    return render(request, "report.html", {'zipped': zipped})
