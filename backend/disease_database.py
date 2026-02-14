"""
V14.0 Disease Treatment Database
Comprehensive disease information with chemical recommendations and treatment protocols
"""

DISEASE_TREATMENTS = {
    "Powdery Mildew": {
        "severity": "Moderate to High",
        "symptoms": [
            "White powdery spots on leaves and stems",
            "Yellowing and curling of leaves",
            "Stunted plant growth",
            "Reduced yield and fruit quality"
        ],
        "causes": [
            "Fungal infection (Erysiphe, Oidium, Sphaerotheca species)",
            "High humidity with moderate temperatures (20-30°C)",
            "Poor air circulation",
            "Dense plant spacing"
        ],
        "fungicides": [
            {
                "name": "Sulfur 80% WP (Wettable Powder)",
                "active_ingredient": "Elemental Sulfur",
                "dosage": "2-3 g/L water",
                "application": "Foliar spray every 7-10 days",
                "brands": ["Sulphex", "Sulfex", "Kumulus"]
            },
            {
                "name": "Azoxystrobin 23% SC",
                "active_ingredient": "Azoxystrobin",
                "dosage": "1 ml/L water",
                "application": "Spray at disease onset, repeat after 15 days",
                "brands": ["Amistar", "Heritage"]
            },
            {
                "name": "Hexaconazole 5% SC",
                "active_ingredient": "Hexaconazole",
                "dosage": "2 ml/L water",
                "application": "Spray at first sign of disease",
                "brands": ["Contaf", "Hexazole"]
            }
        ],
        "preventive_measures": [
            "Improve air circulation by proper plant spacing",
            "Avoid overhead irrigation",
            "Remove infected plant debris",
            "Apply neem oil (5 ml/L) as preventive spray"
        ],
        "treatment_schedule": {
            "Day 1": "Initial fungicide application (Sulfur or Azoxystrobin)",
            "Day 7": "Second application if symptoms persist",
            "Day 14": "Third application for severe infections",
            "Day 21": "Final application and monitoring"
        },
        "safety_precautions": [
            "Wear protective gloves and mask during application",
            "Avoid spraying during windy conditions",
            "Do not spray during flowering to protect pollinators",
            "Maintain 7-day pre-harvest interval"
        ],
        "recovery_timeline": "14-21 days for complete recovery with proper treatment"
    },
    
    "Downy Mildew": {
        "severity": "High",
        "symptoms": [
            "Yellow patches on upper leaf surface",
            "Gray or purple fuzzy growth on lower leaf surface",
            "Leaf distortion and premature drop",
            "Reduced photosynthesis"
        ],
        "causes": [
            "Oomycete pathogens (Peronospora, Plasmopara species)",
            "Cool, wet conditions (15-20°C)",
            "High humidity and leaf wetness",
            "Splashing water spreading spores"
        ],
        "fungicides": [
            {
                "name": "Metalaxyl 8% + Mancozeb 64% WP",
                "active_ingredient": "Metalaxyl + Mancozeb",
                "dosage": "2.5 g/L water",
                "application": "Foliar spray every 10-12 days",
                "brands": ["Ridomil Gold", "Matco"]
            },
            {
                "name": "Copper Oxychloride 50% WP",
                "active_ingredient": "Copper Oxychloride",
                "dosage": "3 g/L water",
                "application": "Spray at 10-day intervals",
                "brands": ["Blitox", "Fytolan"]
            },
            {
                "name": "Cymoxanil 8% + Mancozeb 64% WP",
                "active_ingredient": "Cymoxanil + Mancozeb",
                "dosage": "2 g/L water",
                "application": "Spray at disease appearance",
                "brands": ["Curzate", "Cymox"]
            }
        ],
        "preventive_measures": [
            "Use resistant varieties",
            "Ensure proper drainage",
            "Avoid evening irrigation",
            "Remove and destroy infected leaves"
        ],
        "treatment_schedule": {
            "Day 1": "Initial application of Metalaxyl + Mancozeb",
            "Day 10": "Second application",
            "Day 20": "Third application if needed",
            "Day 30": "Final monitoring and assessment"
        },
        "safety_precautions": [
            "Wear full protective equipment (PPE)",
            "Avoid contact with skin and eyes",
            "Do not apply before rain",
            "Maintain 14-day pre-harvest interval for Metalaxyl"
        ],
        "recovery_timeline": "21-28 days with consistent treatment"
    },
    
    "Leaf Spot": {
        "severity": "Moderate",
        "symptoms": [
            "Circular or irregular brown spots on leaves",
            "Yellow halos around spots",
            "Leaf yellowing and defoliation",
            "Reduced plant vigor"
        ],
        "causes": [
            "Bacterial or fungal pathogens (Cercospora, Alternaria, Xanthomonas)",
            "Warm, humid conditions",
            "Overhead irrigation",
            "Nutrient deficiency"
        ],
        "fungicides": [
            {
                "name": "Mancozeb 75% WP",
                "active_ingredient": "Mancozeb",
                "dosage": "2.5 g/L water",
                "application": "Spray every 7-10 days",
                "brands": ["Dithane M-45", "Indofil M-45"]
            },
            {
                "name": "Chlorothalonil 75% WP",
                "active_ingredient": "Chlorothalonil",
                "dosage": "2 g/L water",
                "application": "Foliar spray at 10-day intervals",
                "brands": ["Kavach", "Daconil"]
            },
            {
                "name": "Copper Hydroxide 77% WP",
                "active_ingredient": "Copper Hydroxide",
                "dosage": "2.5 g/L water",
                "application": "Spray for bacterial leaf spot",
                "brands": ["Kocide", "Champion"]
            }
        ],
        "preventive_measures": [
            "Practice crop rotation",
            "Remove infected plant debris",
            "Improve air circulation",
            "Apply balanced fertilizers"
        ],
        "treatment_schedule": {
            "Day 1": "Initial fungicide application",
            "Day 7": "Second application",
            "Day 14": "Third application",
            "Day 21": "Assessment and final treatment if needed"
        },
        "safety_precautions": [
            "Use protective clothing and gloves",
            "Avoid spraying in hot sun",
            "Keep away from water sources",
            "Maintain 7-10 day pre-harvest interval"
        ],
        "recovery_timeline": "14-21 days with proper management"
    },
    
    "Root Rot": {
        "severity": "High",
        "symptoms": [
            "Wilting despite adequate soil moisture",
            "Yellowing of lower leaves",
            "Brown, mushy roots",
            "Stunted growth and plant death"
        ],
        "causes": [
            "Soil-borne fungi (Pythium, Phytophthora, Fusarium)",
            "Overwatering and poor drainage",
            "Compacted soil",
            "High soil temperature"
        ],
        "reasoning": "Fungal infection typically caused by Phytophthora or Rhizoctonia species in poorly drained soil.",
        "treatment": "Improve drainage; apply Copper-based fungicides like Copper Oxychloride (50WP).",
        "fertilizer": "Katyayani Root-Guard, Bio-Stimulants, IFFCO Nano-Urea protocols.",
        "fungicides": [
            {
                "name": "Metalaxyl 35% WS (Water Soluble)",
                "active_ingredient": "Metalaxyl",
                "dosage": "1 g/L water",
                "application": "Soil drench around root zone",
                "brands": ["Ridomil", "Apron"]
            },
            {
                "name": "Fosetyl-Al 80% WP",
                "active_ingredient": "Fosetyl Aluminium",
                "dosage": "2.5 g/L water",
                "application": "Soil drench every 15 days",
                "brands": ["Aliette", "Fosetic"]
            },
            {
                "name": "Carbendazim 50% WP",
                "active_ingredient": "Carbendazim",
                "dosage": "1 g/L water",
                "application": "Soil drench for Fusarium",
                "brands": ["Bavistin", "Derosal"]
            }
        ],
        "preventive_measures": [
            "Ensure proper soil drainage",
            "Avoid overwatering",
            "Use disease-free planting material",
            "Apply Trichoderma as biocontrol (5 g/L)"
        ],
        "treatment_schedule": {
            "Day 1": "Reduce watering, apply Metalaxyl soil drench",
            "Day 7": "Second soil drench application",
            "Day 15": "Third application if symptoms persist",
            "Day 30": "Final assessment and preventive measures"
        },
        "safety_precautions": [
            "Wear gloves when handling fungicides",
            "Avoid runoff into water bodies",
            "Do not apply to waterlogged soil",
            "Maintain 21-day pre-harvest interval"
        ],
        "recovery_timeline": "30-45 days; severe cases may not recover"
    },
    
    "Tomato Late Blight": {
        "severity": "Extreme",
        "symptoms": [
            "Dark, water-soaked spots on leaves",
            "White mold growth on leaf undersides in humid weather",
            "Firm, dark brown spots on green fruit",
            "Rapid plant collapse and death"
        ],
        "causes": [
            "Pathogen Phytophthora infestans",
            "High humidity (>90%) and cool temperatures (15-22°C)",
            "Poor air drainage",
            "Infected seed tubers or transplants"
        ],
        "fungicides": [
            {
                "name": "Katyayani COC 50 (Copper Oxychloride 50% WP)",
                "active_ingredient": "Copper Oxychloride",
                "dosage": "2.5 g/L water",
                "application": "Apply at 7-10 day intervals; effective in high rainfall",
                "brands": ["Katyayani", "Blitox", "Fytolan"]
            },
            {
                "name": "Katyayani Dr Blight (Metalaxyl-M + Chlorothalonil)",
                "active_ingredient": "Metalaxyl-M + Chlorothalonil",
                "dosage": "2 g/L water",
                "application": "Systemic + Contact action, apply at first sign",
                "brands": ["Katyayani", "Ridomil Gold"]
            },
            {
                "name": "MagicGro Baxil (Bio-Fungicide)",
                "active_ingredient": "Beneficial Microbes / Trichoderma",
                "dosage": "5 g/L water",
                "application": "Soil drench and foliar spray for organic control",
                "brands": ["MagicGro", "Zymo"]
            }
        ],
        "preventive_measures": [
            "Plant resistant varieties",
            "Avoid overhead irrigation",
            "Ensure wide plant spacing",
            "Destroy all volunteer tomato/potato plants"
        ],
        "treatment_schedule": {
            "Action": "Immediate destruction of heavily infected plants",
            "Day 1": "Protective spray of Mancozeb or Chlorothalonil",
            "Day 5": "Systemic spray (Dimethomorph) if symptoms spread",
            "Ongoing": "Monitor daily; remove infected leaves immediately"
        },
        "safety_precautions": [
            "Avoid contact with water sources",
            "Follow strict pre-harvest intervals (3-7 days)",
            "Wear full protective gear"
        ],
        "recovery_timeline": "Difficult to recover; focus is on containment"
    },

    "Mango Anthracnose": {
        "severity": "High",
        "symptoms": [
            "Small, dark brown to black spots on leaves/fruit",
            "Sunken lesions on ripe fruit",
            "Blossom blight and fruit drop",
            "Pinkish spore masses on fruit in wet weather"
        ],
        "causes": [
            "Fungus Colletotrichum gloeosporioides",
            "Frequent rainfall and high humidity during flowering/fruiting",
            "Spores spread by water splashes",
            "Infected twigs and leaves"
        ],
        "fungicides": [
            {
                "name": "ARKA MANGO SPECIAL (Micronutrient Formulation)",
                "active_ingredient": "Zn, B, Fe, Cu, Mn, Mo + Secondary Nutrients",
                "dosage": "5 g/L water",
                "application": "Foliar spray to enhance immunity and fruit quality",
                "brands": ["ICAR-IIHR", "Katyayani"]
            },
            {
                "name": "Katyayani Boron 20% EDTA",
                "active_ingredient": "Boron",
                "dosage": "1 g/L water",
                "application": "Essential for fruit set and reducing disease severity",
                "brands": ["Katyayani", "Dr. Soil"]
            },
            {
                "name": "Rimi Garden More Mango (Organic)",
                "active_ingredient": "Microorganisms + Micronutrients",
                "dosage": "Soil application",
                "application": "Improves overall plant health and resistance",
                "brands": ["Rimi Garden", "Erwon"]
            }
        ],
        "preventive_measures": [
            "Prune infected twigs before flowering",
            "Maintain orchard hygiene",
            "Hot water treatment of fruit post-harvest (52°C for 5-10 min)",
            "Spray copper fungicides before monsoon"
        ],
        "treatment_schedule": {
            "Flowering": "Spray Carbendazim to protect blossoms",
            "Fruiting": "Spray Mancozeb at 15-day intervals",
            "Post-Harvest": "Drip/Spray Prochloraz for shelf-life extension"
        },
        "safety_precautions": [
            "Avoid spraying near bees during peak flowering",
            "14-day pre-harvest interval",
            "Dispose of infected fruit away from orchard"
        ],
        "recovery_timeline": "Seasonal management; prevents fruit loss"
    },

    "Citrus Canker": {
        "severity": "High (Bacterial)",
        "symptoms": [
            "Raised, corky, necrotic lesions on leaves and fruit",
            "Yellow halo around leaf lesions",
            "Premature fruit drop",
            "Death of twigs and branches"
        ],
        "causes": [
            "Bacterium Xanthomonas citri",
            "Wind-blown rain spreading bacteria",
            "Injuries from citrus leaf miner",
            "Warm and wet weather (20-35°C)"
        ],
        "fungicides": [
            {
                "name": "Streptomycin Sulphate 9% + Tetracycline Hydrochloride 1%",
                "active_ingredient": "Antibiotic Mix",
                "dosage": "0.5 g/L water",
                "application": "Bactericidal spray at 15-day intervals",
                "brands": ["Streptocycline", "Plantomycin"]
            },
            {
                "name": "Copper Oxychloride 50% WP",
                "active_ingredient": "Copper Oxychloride",
                "dosage": "3 g/L water",
                "application": "Mix with antibiotic for better control",
                "brands": ["Blitox", "Fytolan"]
            }
        ],
        "preventive_measures": [
            "Control Citrus Leaf Miner (carrier)",
            "Prune and burn infected twigs",
            "Use certified disease-free nursery stock",
            "Create windbreaks around orchards"
        ],
        "treatment_schedule": {
            "Onset": "Pruning of infected parts following by Copper spray",
            "Cycle": "Antibiotic spray + Copper every 15-20 days in rainy season",
            "Maintenance": "Apply Neem oil to control leaf miners"
        },
        "safety_precautions": [
            "Avoid excessive use of antibiotics to prevent resistance",
            "Wear mask during spray",
            "Ensure no spray drift to neighboring crops"
        ],
        "recovery_timeline": "Long-term management; suppressed but not fully cured"
    },

    "Soil Salinity": {
        "severity": "Chronic / Structural",
        "symptoms": [
            "White crust on soil surface",
            "Stunted plant growth",
            "Leaf burn or tip necrosis",
            "Wilting despite wet soil"
        ],
        "causes": [
            "Poor quality irrigation water",
            "Inadequate drainage",
            "High evaporation in arid regions",
            "Over-fertilization"
        ],
        "fungicides": [],
        "preventive_measures": [
            "Implement proper soil drainage (leaching)",
            "Use salt-tolerant crop varieties",
            "Apply Gypsum or organic mulch",
            "Switch to drip irrigation to reduce water evaporation"
        ],
        "treatment_schedule": {
            "Initial": "Soil testing for Electrical Conductivity (EC)",
            "Phase 1": "Leaching with fresh water if drainage allows",
            "Phase 2": "Application of Gypsum (500-1000 kg/acre)",
            "Phase 3": "Planting cover crops to improve soil structure"
        },
        "safety_precautions": [
            "Avoid deep tillage",
            "Test water source regularly",
            "Monitor soil health index"
        ],
        "recovery_timeline": "6-12 months for significant improvement"
    },

    "Paddy Blast": {
        "severity": "Extreme",
        "symptoms": [
            "Spindle-shaped lesions with gray centers on leaves",
            "Brownish lesions on the neck of the panicle (Neck Blast)",
            "Chaffy or partially filled grains",
            "Drying and wilting of the entire plant"
        ],
        "causes": [
            "Fungus Magnaporthe oryzae (Pyricularia oryzae)",
            "High humidity (>90%) and cool night temperatures (20-25°C)",
            "Excessive nitrogenous fertilization",
            "Prolonged leaf wetness from dew or rain"
        ],
        "fungicides": [
            {
                "name": "Tricyclazole 75% WP",
                "active_ingredient": "Tricyclazole",
                "dosage": "0.6 g/L water",
                "application": "Foliar spray at first sign of lesions, repeat after 15 days",
                "brands": ["Beam", "Civic", "Baan"]
            },
            {
                "name": "Isoprothiolane 40% EC",
                "active_ingredient": "Isoprothiolane",
                "dosage": "1.5 ml/L water",
                "application": "Apply at boot leaf stage to prevent neck blast",
                "brands": ["Fujione", "Isopro"]
            },
            {
                "name": "Carbendazim 50% WP",
                "active_ingredient": "Carbendazim",
                "dosage": "1 g/L water",
                "application": "Used for seed treatment and foliar spray",
                "brands": ["Bavistin", "Indofil"]
            }
        ],
        "preventive_measures": [
            "Use resistant varieties (e.g., IR-64, Swarna)",
            "Avoid high nitrogen doses, split nitrogen application",
            "Burn infected stubble post-harvest",
            "Maintain proper water level in the field"
        ],
        "treatment_schedule": {
            "Seed stage": "Treat seeds with Carbendazim (2g/kg)",
            "Nursery": "Spray Tricyclazole if spots appear",
            "Tillering": "Monitor and spray if 2-5% leaf area is infected",
            "Heading": "Mandatory neck blast prevention spray"
        },
        "safety_precautions": [
            "Follow 15-day pre-harvest interval",
            "Wear protective masks during spraying",
            "Avoid spraying during high winds"
        ],
        "recovery_timeline": "14-25 days; Neck blast causes irreversible yield loss"
    },

    "Sugarcane Red Rot": {
        "severity": "Extreme (Cancer of Sugarcane)",
        "symptoms": [
            "Yellowing and drying of the 3rd and 4th leaves",
            "Internal reddening of the pith with white cross-wise bands",
            "Sour, alcoholic odor from split canes",
            "Shrinkage of canes and appearance of black acervuli"
        ],
        "causes": [
            "Fungus Colletotrichum falcatum",
            "Use of infected seed sets",
            "Waterlogging and poor drainage",
            "Presence of susceptible varieties in proximity"
        ],
        "fungicides": [
            {
                "name": "Carbendazim 50% WP (Sett Treatment)",
                "active_ingredient": "Carbendazim",
                "dosage": "1 g/L water (Drench/Dip)",
                "application": "Dip sugarcane sets for 30 mins before planting",
                "brands": ["Bavistin", "Goldenzim"]
            },
            {
                "name": "Copper Oxychloride 50% WP",
                "active_ingredient": "Copper Oxychloride",
                "dosage": "3 g/L water",
                "application": "Spray on soil and surrounding plants if disease is detected",
                "brands": ["Blitox", "Fytolan"]
            }
        ],
        "preventive_measures": [
            "Select healthy sets from disease-free nurseries",
            "Practice 2-3 year crop rotation",
            "Uprooting and burning of infected clumps with roots",
            "Use hot water treated sets (50°C for 2 hours)"
        ],
        "treatment_schedule": {
            "Planting": "Mandatory fungicidal set treatment",
            "Tillering": "Frequent field scouting every 15 days",
            "Infection": "Immediate eradication of infected clumps",
            "Post-Harvest": "Total burning of trash; refrain from ratoon cropping if infected"
        },
        "safety_precautions": [
            "Burn infected materials away from the field",
            "Sterilize farm tools after handling infected canes",
            "Avoid using canal water from infected fields"
        ],
        "recovery_timeline": "No cure for infected canes; focus on saving healthy plots"
    },

    "Micro-Irrigation Fault": {
        "severity": "Operational",
        "symptoms": [
            "Uneven water distribution across emitters",
            "Clogging of drippers with salt/algae",
            "Pressure drop at the lateral ends",
            "Wilting of plants in specific zones"
        ],
        "causes": [
            "Poor water filtration (Sand/Disc filters)",
            "High bicarbonate/iron content in water",
            "Bacterial sliming (Bio-fouling)",
            "Rat bites or mechanical damage to tubes"
        ],
        "fungicides": [],
        "preventive_measures": [
            "Install and clean filters weekly",
            "Acid treatment (HCl/HNO3) for salt removal",
            "Chlorination (Bleaching powder) for algae control",
            "Regular flushing of laterals (Sub-main flush)"
        ],
        "treatment_schedule": {
            "Acid Treatment": "Inject 33% HCl to bring water pH to 4.0; leave for 24 hrs",
            "Chlorination": "Apply 10-20 ppm available chlorine",
            "Maintenance": "Flush sub-mains every 15 days",
            "Filter": "Clean disc filter whenever pressure gauge diff > 0.5kg"
        },
        "safety_precautions": [
            "Handle acids with high-grade rubber gloves",
            "Flush system with fresh water after chemical treatment",
            "Do not mix fertilizers with acids in the same tank"
        ],
        "recovery_timeline": "Instant after flushing/cleaning"
    },

    "Mango Powdery Mildew": {
        "severity": "High (Economic Loss)",
        "symptoms": [
            "Whitish powdery growth on flowers, leaves, and fruits",
            "Premature dropping of flowers and young fruits",
            "Drying of inflorescences (blackening)",
            "Coating of leaves with white fungal mass"
        ],
        "causes": [
            "Fungus Oidium mangiferae",
            "High humidity with moderate temperatures",
            "Cloudy weather during flowering stage",
            "Lack of sunlight in dense canopies"
        ],
        "fungicides": [
            {
                "name": "Wettable Sulphur 80% WP",
                "active_ingredient": "Sulphur",
                "dosage": "2 g/L water",
                "application": "Apply at flower bud burst stage",
                "brands": ["Sulfex", "Insur"]
            },
            {
                "name": "Hexaconazole 5% EC",
                "active_ingredient": "Hexaconazole",
                "dosage": "1 ml/L water",
                "application": "Apply 15 days after first spray if weather is cloudy",
                "brands": ["Contaf", "Sitara"]
            }
        ],
        "preventive_measures": [
            "Prune dense branches to allow sunlight penetration",
            "Avoid excessive nitrogen during flowering",
            "Maintain clean orchard hygiene",
            "Spray at 50% flowering stage as a precaution"
        ],
        "treatment_schedule": {
            "Bud Burst": "Sulphur spray (2g/L)",
            "Full Bloom": "Hexaconazole or Dinocap spray",
            "Fruit Set": "Final spray with Sulphur or Carbendazim",
            "Maintenance": "Monitor weather; humidity > 80% warrants immediate spray"
        },
        "safety_precautions": [
            "Avoid spraying Sulphur during high temperatures (>35°C) to prevent leaf burn",
            "Follow 15-day Pre-Harvest Interval (PHI)",
            "Protect eyes during application"
        ],
        "recovery_timeline": "10-20 days; however, fruit set loss is irreversible"
    },

    "Banana Sigatoka": {
        "severity": "Extreme (Defoliation)",
        "symptoms": [
            "Small yellowish-green streaks on leaves",
            "Dark brown or black necrotic spots with yellow halos",
            "Drying of leaf margins and premature death of leaves",
            "Small fruit size and poor ripening quality"
        ],
        "causes": [
            "Fungus Mycosphaerella musicola (Yellow Sigatoka)",
            "Warm and wet weather (High rainfall)",
            "Poor soil drainage and high plant density",
            "Wind-borne spore dispersal"
        ],
        "fungicides": [
            {
                "name": "Propiconazole 25% EC",
                "active_ingredient": "Propiconazole",
                "dosage": "1 ml/L water + Mineral Oil",
                "application": "Foliar spray with oil-in-water emulsion",
                "brands": ["Tilt", "Bumper"]
            },
            {
                "name": "Chlorothalonil 75% WP",
                "active_ingredient": "Chlorothalonil",
                "dosage": "2 g/L water",
                "application": "Protective spray during monsoon onset",
                "brands": ["Kavach", "Contaf Plus"]
            }
        ],
        "preventive_measures": [
            "De-leafing: Remove and burn infected leaves immediately",
            "Maintain proper drainage to reduce humidity",
            "Avoid excessive plant population (Optimal spacing)",
            "Eradicate weed hosts around the plantation"
        ],
        "treatment_schedule": {
            "Vegetative": "Monthly monitoring; spray if spots appear",
            "Monsoon": "Shorten spray interval to 15-20 days",
            "Flowering": "Target younger leaves for maximum protection",
            "Post-Spray": "Apply Urea (1%) to help leaf recovery"
        },
        "safety_precautions": [
            "Rotate fungicides to prevent resistance",
            "Avoid direct skin contact with Propiconazole",
            "Ensure complete coverage of both leaf surfaces"
        ],
        "recovery_timeline": "2-3 months for new healthy leaf emergence"
    },
    "Healthy Neem": {
        "severity": "None",
        "symptoms": ["Green, serrated leaves", "Healthy leaf margins", "Vibrant growth"],
        "causes": ["Optimal soil and water conditions", "Natural pest resistance"],
        "fungicides": [],
        "preventive_measures": ["Regular monitoring", "Balanced NPK application"],
        "treatment_schedule": {"Day 1": "Maintain current care protocol"},
        "safety_precautions": ["No chemicals required"],
        "recovery_timeline": "Maintenance mode"
    },
    
    "Neem Leaf Webber": {
        "severity": "Moderate",
        "symptoms": ["Leaves webbed together", "Defoliation", "Scraping of green matter"],
        "causes": ["Larvae of Palpita unionalis", "Humid weather"],
        "fungicides": [
            {
                "name": "Malathion 50 EC",
                "active_ingredient": "Malathion",
                "dosage": "2 ml/L water",
                "application": "Apply as soon as webbing is noticed",
                "brands": ["Malathion", "Cythion"]
            }
        ],
        "preventive_measures": ["Prune webbed branches", "Light traps", "Spray Neem oil"],
        "treatment_schedule": {"Day 1": "Identify and remove webbed clusters", "Day 3": "Apply Malathion spray"},
        "safety_precautions": ["Avoid direct contact with spray"],
        "recovery_timeline": "10-15 days"
    },

    "Healthy Moringa": {
        "severity": "None",
        "symptoms": ["Small, oval leaflets", "Smooth margins", "Light green foliage"],
        "causes": ["Well-drained soil", "Adequate sunlight"],
        "fungicides": [],
        "preventive_measures": ["Mulching", "Proper pruning"],
        "treatment_schedule": {"Day 1": "Routine care"},
        "safety_precautions": ["No chemical treatment needed"],
        "recovery_timeline": "Healthy state"
    },
    "Coconut Bud Rot": {
        "severity": "Lethal",
        "symptoms": [
            "Yellowing and drooping of the spindle (innermost) leaf",
            "Soft rotting of tender bud tissues",
            "Foul smell from the infected crown",
            "Eventual falling of the crown (Death of palm)"
        ],
        "causes": [
            "Fungus/Water mold Phytophthora palmivora",
            "Heavy monsoon rainfall and high RH",
            "Presence of other infected palms (Spores spread by wind/rain)",
            "Poor air circulation in dense plantations"
        ],
        "fungicides": [
            {
                "name": "Copper Oxychloride 50% WP",
                "active_ingredient": "Copper Oxychloride",
                "dosage": "3-5 g/L water (Paste/Drench)",
                "application": "Clean the bud and apply paste/drench directly to the crown",
                "brands": ["Blitox", "Fytolan"]
            },
            {
                "name": "Bordeaux Mixture 1%",
                "active_ingredient": "Copper Sulphate + Lime",
                "dosage": "10 g/L (Freshly prepared)",
                "application": "Prophylactic spray on healthy palms during monsoon",
                "brands": ["Home-made", "Indofil Z-78"]
            }
        ],
        "preventive_measures": [
            "Regularly clean the crown (removal of dried leaves/spathes)",
            "Improve air circulation by pruning surrounding vegetation",
            "Practice soil drenching with fungicides in endemic areas",
            "Avoid injury to the crown during harvesting"
        ],
        "treatment_schedule": {
            "Discovery": "Immediate cleaning of affected bud tissue",
            "Phase 1": "Apply Copper Oxychloride paste to the cleaned bud",
            "Phase 2": "Protect the treated area from rain for 3 days",
            "Phase 3": "Apply Bordeaux Mixture to surrounding healthy palms"
        },
        "safety_precautions": [
            "Handle Copper Sulphate with care (Corrosive)",
            "Ensure the person climbing the tree is trained in bud surgery",
            "Use protective goggles when spraying overhead"
        ],
        "recovery_timeline": "6-12 months for new spindle growth; if bud is fully rotted, palm is lost"
    },
    "Watermelon Anthracnose": {
        "severity": "High to Extreme",
        "symptoms": [
            "Small, irregular, dark brown to black spots on leaves",
            "Sunken, circular to oval lesions on fruit (blisters)",
            "Salmon-colored spore masses in center of fruit lesions",
            "Spindle-shaped sunken lesions on stems/petioles",
            "Shot-hole appearance in older leaf lesions"
        ],
        "causes": [
            "Fungus Colletotrichum orbiculare",
            "High humidity (>90%) and warm temperatures (20-29°C)",
            "Frequent rainfall or overhead irrigation",
            "Infected seeds or plant debris"
        ],
        "fungicides": [
            {
                "name": "Chlorothalonil 75% WP",
                "active_ingredient": "Chlorothalonil",
                "dosage": "2 g/L water",
                "application": "Foliar spray at 7-10 day intervals",
                "brands": ["Kavach", "Bravo"]
            },
            {
                "name": "Azoxystrobin 23% SC",
                "active_ingredient": "Azoxystrobin",
                "dosage": "1 ml/L water",
                "application": "Spray when disease is detected, repeat every 14 days",
                "brands": ["Amistar", "Quadris"]
            },
            {
                "name": "Mancozeb 75% WP",
                "active_ingredient": "Mancozeb",
                "dosage": "2.5 g/L water",
                "application": "Preventative spray every 7 days in wet weather",
                "brands": ["Dithane M-45", "Indofil M-45"]
            }
        ],
        "preventive_measures": [
            "Use disease-free and certified seeds",
            "Practice 2-3 year crop rotation with non-cucurbits",
            "Improve air circulation by proper spacing",
            "Remove and destroy infected crop debris"
        ],
        "treatment_schedule": {
            "Day 1": "Initial spray with Azoxystrobin or Chlorothalonil",
            "Day 7": "Apply Mancozeb as a protective layer",
            "Day 14": "Rotate with different FRAC group (e.g. Copper Oxychloride)",
            "Ongoing": "Monitor fields every 3 days; remove infected fruit immediately"
        },
        "safety_precautions": [
            "Observe 5-7 day pre-harvest interval (PHI)",
            "Avoid sequential applications of Strobilurins (Group 11)",
            "Wear full protective gear including mask and gloves",
            "Apply early morning to avoid bee activity"
        ],
        "recovery_timeline": "14-25 days for leaf recovery; infected fruits cannot be recovered"
    },

    "Brown Rot": {
        "severity": "High (Fruit Loss)",
        "symptoms": [
            "Soft, brown, water-soaked spots on fruit",
            "Grayish-brown fuzzy mold growth on affected areas",
            "Mummification of infected fruits (they dry up and stay on plant)",
            "Cankers on twigs and wilting of flowers"
        ],
        "causes": [
            "Fungi (Monilinia species or specific fruit pathogens)",
            "Prolonged wet weather during ripening",
            "High fruit density and poor airflow",
            "Mechanical injuries/insect bites on fruit"
        ],
        "fungicides": [
            {
                "name": "Tebuconazole 25.9% EC",
                "active_ingredient": "Tebuconazole",
                "dosage": "1 ml/L water",
                "application": "Spray at bloom and fruit ripening stages",
                "brands": ["Folicur", "Orius"]
            },
            {
                "name": "Propiconazole 25% EC",
                "active_ingredient": "Propiconazole",
                "dosage": "1 ml/L water",
                "application": "Apply at first sign of infection",
                "brands": ["Tilt", "Bumper"]
            }
        ],
        "preventive_measures": [
            "Thin fruit clusters to improve air circulation",
            "Prune infected twigs and remove mummified fruit",
            "Maintain soil drainage to reduce humidity",
            "Avoid bruising fruit during harvest"
        ],
        "treatment_schedule": {
            "Day 1": "Apply Tebuconazole at first sign of rot",
            "Day 10": "Second application if wet weather persists",
            "Day 21": "Final spray before harvest (check PHI)"
        },
        "safety_precautions": [
            "Maintain a 7-day pre-harvest interval (PHI)",
            "Do not apply more than 3 times per season",
            "Work with the wind to avoid spray drift"
        ],
        "recovery_timeline": "Stops spread within 7-10 days; focus on protecting healthy fruit"
    }
}

def get_disease_info(disease_name):
    """
    Get comprehensive treatment information for a disease with Smart Token Matching.
    """
    if not disease_name:
        return None

    # Normalize disease name
    disease_key = disease_name.strip().title()
    disease_lower = disease_name.lower()
    
    # 1. Try exact match first
    if disease_key in DISEASE_TREATMENTS:
        return DISEASE_TREATMENTS[disease_key]
    
    # 2. Try partial match
    for key in DISEASE_TREATMENTS:
        if disease_lower in key.lower() or key.lower() in disease_lower:
            return DISEASE_TREATMENTS[key]
            
    # 3. Smart Token Match (e.g., "Tomato Late Blight" matches "Tomato Blight")
    query_tokens = set(disease_lower.replace("on", "").replace("the", "").split())
    for key, info in DISEASE_TREATMENTS.items():
        key_tokens = set(key.lower().split())
        # If at least 2 significant words match, or 50% of the key matches
        intersection = query_tokens.intersection(key_tokens)
        if len(intersection) >= 2 or (len(intersection) >= 1 and len(intersection) / len(key_tokens) >= 0.5):
            return info
    
    # Return generic info if not found
    return {
        "severity": "Unknown",
        "symptoms": ["Disease information not available in database"],
        "causes": ["Consult local agricultural expert"],
        "fungicides": [],
        "preventive_measures": ["Practice good agricultural hygiene"],
        "treatment_schedule": {},
        "safety_precautions": ["Always wear protective equipment"],
        "recovery_timeline": "Consult expert for timeline"
    }
