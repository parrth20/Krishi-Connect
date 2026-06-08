"""Small farmer knowledge base used by the local RAG assistant."""

DISEASE_PROFILES = {
    "rice-blast": {
        "slug": "rice-blast",
        "crop": "Rice",
        "disease": "Rice blast",
        "confidence": 0.92,
        "sample_image": "Images/disease-samples/rice-blast.png",
        "symptoms": [
            "Spindle-shaped spots with grey centres and brown borders on leaves.",
            "Lesions may join together and dry the leaf in humid weather.",
            "Severe infection can affect nodes and panicles.",
        ],
        "causes": [
            "Long leaf wetness, cloudy weather, and high humidity.",
            "Dense crop canopy and excess nitrogen fertiliser.",
            "Use of infected seed or infected crop residue.",
        ],
        "cure": [
            "Remove badly infected leaves where practical and avoid moving through a wet crop.",
            "Stop excess urea or nitrogen top dressing until the crop recovers.",
            "Keep the field drained enough to reduce long leaf wetness.",
            "If disease is spreading, use a locally approved blast fungicide such as tricyclazole or carbendazim exactly as per label advice.",
        ],
        "prevention": [
            "Use resistant varieties and treated seed.",
            "Keep correct plant spacing for air movement.",
            "Apply balanced NPK and avoid heavy nitrogen in humid weather.",
        ],
        "weather_risk": "High humidity, cloudy days, light rain, and 24-28 C temperature increase rice blast risk.",
        "keywords": ["rice", "paddy", "blast", "spindle", "grey center", "gray center", "brown border"],
    },
    "tomato-early-blight": {
        "slug": "tomato-early-blight",
        "crop": "Tomato",
        "disease": "Early blight",
        "confidence": 0.9,
        "sample_image": "Images/disease-samples/tomato-early-blight.png",
        "symptoms": [
            "Circular brown spots with target-like concentric rings.",
            "Yellowing around old leaf spots, usually starting on lower leaves.",
            "Leaves may dry and drop when infection is heavy.",
        ],
        "causes": [
            "Fungal spores surviving on plant debris and soil.",
            "Splashing rain or overhead irrigation.",
            "Poor air movement and stress from uneven watering.",
        ],
        "cure": [
            "Prune infected lower leaves and remove them from the field.",
            "Mulch around plants to stop soil splash onto leaves.",
            "Water near the root zone, not over the leaves.",
            "If spreading continues, use a locally approved fungicide such as copper, mancozeb, or chlorothalonil as per label and waiting-period rules.",
        ],
        "prevention": [
            "Rotate tomato, potato, chilli, and brinjal crops with non-solanaceous crops.",
            "Stake plants and maintain spacing for air flow.",
            "Do not leave infected crop residue in the plot.",
        ],
        "weather_risk": "Warm humid weather, frequent rain, and wet lower leaves increase early blight risk.",
        "keywords": ["tomato", "early blight", "target spot", "concentric", "yellow halo", "round spot"],
    },
    "potato-late-blight": {
        "slug": "potato-late-blight",
        "crop": "Potato",
        "disease": "Late blight",
        "confidence": 0.91,
        "sample_image": "Images/disease-samples/potato-late-blight.png",
        "symptoms": [
            "Irregular water-soaked brown or black patches on leaves.",
            "Leaf edges may look burnt, especially after cool wet nights.",
            "White fungal growth can appear under leaves in very humid weather.",
        ],
        "causes": [
            "Cool, wet, cloudy conditions with high humidity.",
            "Infected seed tubers or nearby infected potato/tomato plants.",
            "Dense canopy that keeps leaves wet for long periods.",
        ],
        "cure": [
            "Remove and destroy heavily infected leaves or plants away from the field.",
            "Avoid overhead irrigation and improve drainage immediately.",
            "Do not store tubers from badly infected plants.",
            "For active spread, consult the local agriculture office for a registered late-blight fungicide such as mancozeb, cymoxanil, or metalaxyl mixtures and follow the label strictly.",
        ],
        "prevention": [
            "Use disease-free seed tubers.",
            "Maintain field sanitation and destroy volunteer potato plants.",
            "Start protective sprays early when cool wet weather is forecast.",
        ],
        "weather_risk": "Cool temperatures, rain, fog, and humidity above 90 percent create high late blight risk.",
        "keywords": ["potato", "late blight", "water soaked", "black patch", "brown patch", "cool wet"],
    },
    "leaf-stress": {
        "slug": "leaf-stress",
        "crop": "Crop",
        "disease": "Leaf stress or fungal leaf spot",
        "confidence": 0.55,
        "sample_image": "Images/Plant.png",
        "symptoms": [
            "Yellowing, spots, or drying leaves can come from disease, water stress, or nutrient imbalance.",
            "A clear close-up of both sides of the leaf improves diagnosis.",
        ],
        "causes": [
            "Irregular irrigation, low nutrients, poor drainage, or early fungal infection.",
            "Pest injury can also make spots that look like disease.",
        ],
        "cure": [
            "Remove the worst affected leaves and keep the crop area clean.",
            "Check soil moisture before watering; avoid both waterlogging and severe dry stress.",
            "Use balanced nutrition and avoid applying fertiliser on dry soil.",
            "If spots are spreading fast, contact the nearest Krishi Vigyan Kendra or agriculture officer with a fresh sample.",
        ],
        "prevention": [
            "Use clean seed, rotate crops, and maintain spacing.",
            "Inspect the lower leaves twice a week during humid weather.",
        ],
        "weather_risk": "High humidity and repeated rain favour fungal spots; hot dry weather favours water stress.",
        "keywords": ["yellow", "spot", "dry", "leaf", "wilting", "unknown"],
    },
}


KNOWLEDGE_DOCUMENTS = [
    {
        "id": "rice-blast-cure",
        "title": "Rice blast cure and prevention",
        "topic": "crop disease cure rice blast paddy",
        "body": (
            "Rice blast shows spindle-shaped lesions with grey centres and brown borders. "
            "Reduce leaf wetness, avoid excess nitrogen, remove infected leaves where practical, "
            "and use a locally approved blast fungicide only as per label. Resistant varieties, "
            "seed treatment, spacing, and balanced fertiliser reduce future risk."
        ),
        "profile_slug": "rice-blast",
    },
    {
        "id": "tomato-early-blight-cure",
        "title": "Tomato early blight cure",
        "topic": "tomato early blight target spot yellow leaves cure",
        "body": (
            "Tomato early blight starts on lower leaves as brown target-like rings with yellowing. "
            "Prune infected lower leaves, mulch soil, water at the root, improve air flow, and rotate crops. "
            "Copper, mancozeb, or chlorothalonil may be used only if locally registered and label directions are followed."
        ),
        "profile_slug": "tomato-early-blight",
    },
    {
        "id": "potato-late-blight-cure",
        "title": "Potato late blight cure",
        "topic": "potato late blight water soaked brown patch cure",
        "body": (
            "Potato late blight causes irregular water-soaked brown patches and spreads quickly in cool wet weather. "
            "Remove badly infected plants, avoid overhead irrigation, improve drainage, and protect nearby plants. "
            "Use disease-free seed tubers and consult local extension staff for registered fungicide timing."
        ),
        "profile_slug": "potato-late-blight",
    },
    {
        "id": "weather-spray",
        "title": "Weather-aware spraying advice",
        "topic": "weather rain humidity wind spray pesticide fungicide",
        "body": (
            "Do not spray pesticide or fungicide before rain, during strong wind, or when leaves are already wet. "
            "A calm dry window of 6-8 hours is best. High humidity and leaf wetness raise fungal disease risk, "
            "so inspect crops after rain and remove infected leaves early."
        ),
    },
    {
        "id": "irrigation-heat",
        "title": "Irrigation during heat",
        "topic": "irrigation heat temperature dry crop water stress",
        "body": (
            "During hot dry weather, irrigate early morning or evening and avoid wetting leaves when disease pressure is high. "
            "Mulch reduces evaporation. Check soil moisture before watering because waterlogging can damage roots and increase fungal disease."
        ),
    },
    {
        "id": "yellow-leaves",
        "title": "Yellow leaves first checks",
        "topic": "yellow leaves nutrient deficiency water stress",
        "body": (
            "Yellow leaves may mean nitrogen deficiency, root stress, waterlogging, drought, or disease. "
            "Check whether yellowing starts from old leaves, whether soil is too wet or dry, and whether spots are spreading. "
            "Balanced fertiliser and corrected irrigation solve many non-disease cases."
        ),
        "profile_slug": "leaf-stress",
    },
    {
        "id": "rag-project-scope",
        "title": "Krishi Connect assistant scope",
        "topic": "chatbot farmer assistant plant disease weather government scheme",
        "body": (
            "Krishi Connect helps farmers ask crop questions, check local weather, upload plant images, "
            "review disease samples, and get cure guidance from a small agriculture knowledge base. "
            "The assistant gives practical next steps and recommends local expert confirmation for chemical use."
        ),
    },
]


SAMPLE_CASES = [
    {
        "slug": "rice-blast",
        "title": "Rice leaf sample",
        "button": "Analyze rice blast",
        "description": "Spindle lesions on rice leaf.",
    },
    {
        "slug": "tomato-early-blight",
        "title": "Tomato leaf sample",
        "button": "Analyze tomato blight",
        "description": "Target-like rings and yellowing.",
    },
    {
        "slug": "potato-late-blight",
        "title": "Potato leaf sample",
        "button": "Analyze potato blight",
        "description": "Irregular dark water-soaked patches.",
    },
]
