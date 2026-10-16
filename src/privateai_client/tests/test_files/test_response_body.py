age_repsonse_1 = [
    {
        "entities": [
            {
                "text": "32",
                "location": {"stt_idx": 2, "end_idx": 4},
                "best_label": "AGE",
                "labels": {"AGE": 0.9599081873893738},
                "analysis_result": {
                    "formatted": 32,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            }
        ],
        "entities_present": True,
        "characters_processed": 30,
        "languages_detected": {"en": 0.9850051403045654},
    }
]


age_repsonse_2 = [
    {
        "entities": [
            {
                "text": "32",
                "location": {"stt_idx": 2, "end_idx": 4},
                "best_label": "AGE",
                "labels": {"AGE": 0.9599081873893738},
                "analysis_result": {
                    "formatted": None,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            }
        ],
        "entities_present": True,
        "characters_processed": 30,
        "languages_detected": {"en": 0.9850051403045654},
    }
]


date_response_1 = [
    {
        "entities": [
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {"formatted": "1", "label": "DAY"},
                        {"formatted": "1", "label": "MONTH"},
                        {"formatted": "1990", "label": "YEAR"},
                    ],
                    "validation_assertions": [],
                },
            }
        ],
        "entities_present": True,
        "characters_processed": 20,
        "languages_detected": {"en": 0.7509669661521912},
    }
]


date_response_2 = [
    {
        "entities": [
            {
                "text": "1990-01-01",
                "location": {"stt_idx": 9, "end_idx": 19},
                "best_label": "DOB",
                "labels": {"DOB": 0.8460723161697388, "DATE": 0.07507945299148559},
                "analysis_result": {
                    "formatted": "1990-01-01T00:00:00",
                    "subtypes": [
                        {
                            "formatted": "1",
                            "label": "DAY",
                            "location": {"stt_idx": 17, "end_idx": 19},
                        },
                        {
                            "formatted": "1",
                            "label": "MONTH",
                            "location": {"stt_idx": 14, "end_idx": 16},
                        },
                        {
                            "formatted": "1990",
                            "label": "YEAR",
                            "location": {"stt_idx": 9, "end_idx": 13},
                        },
                    ],
                    "validation_assertions": [],
                },
            }
        ],
        "entities_present": True,
        "characters_processed": 20,
        "languages_detected": {"en": 0.7509669661521912},
    }
]
