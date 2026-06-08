from .rag_service import answer_farmer_question


def chat(request):
    question = request.POST.get("input", "")
    city = request.POST.get("city", "")
    crop = request.POST.get("crop", "")
    disease_slug = request.POST.get("disease", "")
    return answer_farmer_question(question, city=city, crop=crop, disease_slug=disease_slug)["answer"]
