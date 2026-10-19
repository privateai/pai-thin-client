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


processed_text_response_1 = [
    {
        "entities": [
            {
                "processed_text": "ORGANIZATION_1",
                "text": "info",
                "location": {
                    "stt_idx": 5,
                    "end_idx": 9,
                    "stt_idx_processed": 5,
                    "end_idx_processed": 21,
                },
                "best_label": "ORGANIZATION",
                "labels": {"ORGANIZATION": 0.5608},
            },
            {
                "processed_text": "ORGANIZATION_2",
                "text": "Georgia Division of Transportation",
                "location": {
                    "stt_idx": 53,
                    "end_idx": 87,
                    "stt_idx_processed": 65,
                    "end_idx_processed": 81,
                },
                "best_label": "ORGANIZATION",
                "labels": {
                    "LOCATION": 0.1905,
                    "ORGANIZATION": 0.9191,
                    "LOCATION_STATE": 0.1953,
                },
            },
            {
                "processed_text": "NAME_GIVEN_1",
                "text": "Johanna",
                "location": {
                    "stt_idx": 105,
                    "end_idx": 112,
                    "stt_idx_processed": 99,
                    "end_idx_processed": 113,
                },
                "best_label": "NAME_GIVEN",
                "labels": {"NAME": 0.9123, "NAME_GIVEN": 0.917},
            },
            {
                "processed_text": "NUMERICAL_PII_1",
                "text": "614-5555 01",
                "location": {
                    "stt_idx": 252,
                    "end_idx": 263,
                    "stt_idx_processed": 253,
                    "end_idx_processed": 270,
                },
                "best_label": "NUMERICAL_PII",
                "labels": {"NUMERICAL_PII": 0.9335},
            },
            {
                "processed_text": "NAME_1",
                "text": "Jiminy Cricket",
                "location": {
                    "stt_idx": 405,
                    "end_idx": 419,
                    "stt_idx_processed": 412,
                    "end_idx_processed": 420,
                },
                "best_label": "NAME",
                "labels": {"NAME": 0.9329, "NAME_GIVEN": 0.3458, "NAME_FAMILY": 0.296},
            },
            {
                "processed_text": "DOB_1",
                "text": "12345",
                "location": {
                    "stt_idx": 421,
                    "end_idx": 426,
                    "stt_idx_processed": 422,
                    "end_idx_processed": 429,
                },
                "best_label": "DOB",
                "labels": {"DOB": 0.9707},
            },
            {
                "processed_text": "NAME_2",
                "text": "Bob Douglas",
                "location": {
                    "stt_idx": 433,
                    "end_idx": 444,
                    "stt_idx_processed": 436,
                    "end_idx_processed": 444,
                },
                "best_label": "NAME",
                "labels": {"NAME_FAMILY": 0.5939, "NAME_GIVEN": 0.2492, "NAME": 0.9162},
            },
            {
                "processed_text": "LOCATION_ADDRESS_1",
                "text": "123 Fake St, Atlanta, Georgia 40234",
                "location": {
                    "stt_idx": 539,
                    "end_idx": 574,
                    "stt_idx_processed": 539,
                    "end_idx_processed": 559,
                },
                "best_label": "LOCATION_ADDRESS",
                "labels": {
                    "LOCATION": 0.9145,
                    "LOCATION_ZIP": 0.1365,
                    "LOCATION_ADDRESS": 0.934,
                    "LOCATION_CITY": 0.189,
                    "LOCATION_STATE": 0.1846,
                    "LOCATION_ADDRESS_STREET": 0.2914,
                },
            },
            {
                "processed_text": "PHONE_NUMBER_1",
                "text": "555-666-7777",
                "location": {
                    "stt_idx": 634,
                    "end_idx": 646,
                    "stt_idx_processed": 619,
                    "end_idx_processed": 635,
                },
                "best_label": "PHONE_NUMBER",
                "labels": {"PHONE_NUMBER": 0.8716},
            },
            {
                "processed_text": "EMAIL_ADDRESS_1",
                "text": "bob.douglas@gmail.com",
                "location": {
                    "stt_idx": 647,
                    "end_idx": 668,
                    "stt_idx_processed": 636,
                    "end_idx_processed": 653,
                },
                "best_label": "EMAIL_ADDRESS",
                "labels": {"EMAIL_ADDRESS": 0.8037},
            },
        ],
        "entities_present": True,
        "characters_processed": 741,
        "languages_detected": {"en": 0.8577668070793152},
        "processed_text": "Case [ORGANIZATION_1]. Good afternoon. Thank you for calling the [ORGANIZATION_2]. My name is miss [NAME_GIVEN_1], and it is a pleasure assisting you today. For security reasons, may I please have either your Social Security number or your case number? [NUMERICAL_PII_1]. Thank you so much. Could you please verify your name, your date of birth, and the name of the other parent on the case you are calling for? [NAME_1]. [DOB_1]. I am [NAME_2]. Thank you, ma am. And lastly, could you please verify your address, phone number, and email? [LOCATION_ADDRESS_1], You said my phone number? Phone number and email, please. [PHONE_NUMBER_1]@[EMAIL_ADDRESS_1]. Alright, ma am. Thank you so much for verifying that information today.",
    }
]


processed_text_response_2 = [
    {
        "entities": [
            {
                "processed_text": "####",
                "text": "info",
                "location": {
                    "stt_idx": 5,
                    "end_idx": 9,
                    "stt_idx_processed": 5,
                    "end_idx_processed": 9,
                },
                "best_label": "ORGANIZATION",
                "labels": {"ORGANIZATION": 0.5608},
            },
            {
                "processed_text": "##################################",
                "text": "Georgia Division of Transportation",
                "location": {
                    "stt_idx": 53,
                    "end_idx": 87,
                    "stt_idx_processed": 53,
                    "end_idx_processed": 87,
                },
                "best_label": "ORGANIZATION",
                "labels": {
                    "LOCATION": 0.1905,
                    "ORGANIZATION": 0.9191,
                    "LOCATION_STATE": 0.1953,
                },
            },
            {
                "processed_text": "#######",
                "text": "Johanna",
                "location": {
                    "stt_idx": 105,
                    "end_idx": 112,
                    "stt_idx_processed": 105,
                    "end_idx_processed": 112,
                },
                "best_label": "NAME_GIVEN",
                "labels": {"NAME": 0.9123, "NAME_GIVEN": 0.917},
            },
            {
                "processed_text": "###########",
                "text": "614-5555 01",
                "location": {
                    "stt_idx": 252,
                    "end_idx": 263,
                    "stt_idx_processed": 252,
                    "end_idx_processed": 263,
                },
                "best_label": "NUMERICAL_PII",
                "labels": {"NUMERICAL_PII": 0.9335},
            },
            {
                "processed_text": "##############",
                "text": "Jiminy Cricket",
                "location": {
                    "stt_idx": 405,
                    "end_idx": 419,
                    "stt_idx_processed": 405,
                    "end_idx_processed": 419,
                },
                "best_label": "NAME",
                "labels": {"NAME": 0.9329, "NAME_GIVEN": 0.3458, "NAME_FAMILY": 0.296},
            },
            {
                "processed_text": "#####",
                "text": "12345",
                "location": {
                    "stt_idx": 421,
                    "end_idx": 426,
                    "stt_idx_processed": 421,
                    "end_idx_processed": 426,
                },
                "best_label": "DOB",
                "labels": {"DOB": 0.9707},
            },
            {
                "processed_text": "###########",
                "text": "Bob Douglas",
                "location": {
                    "stt_idx": 433,
                    "end_idx": 444,
                    "stt_idx_processed": 433,
                    "end_idx_processed": 444,
                },
                "best_label": "NAME",
                "labels": {"NAME_FAMILY": 0.5939, "NAME_GIVEN": 0.2492, "NAME": 0.9162},
            },
            {
                "processed_text": "###################################",
                "text": "123 Fake St, Atlanta, Georgia 40234",
                "location": {
                    "stt_idx": 539,
                    "end_idx": 574,
                    "stt_idx_processed": 539,
                    "end_idx_processed": 574,
                },
                "best_label": "LOCATION_ADDRESS",
                "labels": {
                    "LOCATION": 0.9145,
                    "LOCATION_ZIP": 0.1365,
                    "LOCATION_ADDRESS": 0.934,
                    "LOCATION_CITY": 0.189,
                    "LOCATION_STATE": 0.1846,
                    "LOCATION_ADDRESS_STREET": 0.2914,
                },
            },
            {
                "processed_text": "############",
                "text": "555-666-7777",
                "location": {
                    "stt_idx": 634,
                    "end_idx": 646,
                    "stt_idx_processed": 634,
                    "end_idx_processed": 646,
                },
                "best_label": "PHONE_NUMBER",
                "labels": {"PHONE_NUMBER": 0.8716},
            },
            {
                "processed_text": "#####################",
                "text": "bob.douglas@gmail.com",
                "location": {
                    "stt_idx": 647,
                    "end_idx": 668,
                    "stt_idx_processed": 647,
                    "end_idx_processed": 668,
                },
                "best_label": "EMAIL_ADDRESS",
                "labels": {"EMAIL_ADDRESS": 0.8037},
            },
        ],
        "entities_present": True,
        "characters_processed": 741,
        "languages_detected": {"en": 0.8577668070793152},
        "processed_text": "Case ####. Good afternoon. Thank you for calling the ##################################. My name is miss #######, and it is a pleasure assisting you today. For security reasons, may I please have either your Social Security number or your case number? ###########. Thank you so much. Could you please verify your name, your date of birth, and the name of the other parent on the case you are calling for? ##############. #####. I am ###########. Thank you, ma am. And lastly, could you please verify your address, phone number, and email? ###################################, You said my phone number? Phone number and email, please. ############@#####################. Alright, ma am. Thank you so much for verifying that information today.",
    }
]
