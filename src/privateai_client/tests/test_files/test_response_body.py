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


process_text_1 = [
    "Case info. Good afternoon. Thank you for calling the Georgia Division of Transportation. My name is miss Johanna, and it is a pleasure assisting you today. For security reasons, may I please have either your Social Security number or your case number? 614-5555 01. Thank you so much. Could you please verify your name, your date of birth, and the name of the other parent on the case you are calling for? Jiminy Cricket. 12345. I am Bob Douglas. Thank you, ma am. And lastly, could you please verify your address, phone number, and email? 123 Fake St, Atlanta, Georgia 40234, You said my phone number? Phone number and email, please. 555-666-7777@bob.douglas@gmail.com. Alright, ma am. Thank you so much for verifying that information today."
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


analyze_text_1 = [
    "Operator: Thanks for calling City Help Line, my name is Sean James. May I ask who I'm speaking with today? \nCaller: Ummmm... yes my name is Russel Forkton. How are you? \nOperator: I'm good, thanks for asking. Is it ok if I call you Russel? \nCaller: Yes that is ok. \nOperator: Russel... can you tell me, how can I help you today? \nCaller: I work up this morning with some pain in my left side, a sore throat, and a nasty cough. I'm curious if I need to visit a doctor, or if I can just go to a pharmacy and get some OTC drugs.\nOperator: Can I ask you a few more questions? Can you let me know your which city are you located in and your postal code? What's your health card number? And how long have you been feeling un well? \nCaller: I'm currently in Anchorage, Alaska. Whats a postal code? ... do you mean a zip code? If so, mine is 99515. My medicaid number is 12387654. I've only felt all these symptoms this morning, when I woke up. But I was vomitting 3 days ago on Monday. \nOperator: Thanks for sharing that info. Apologies, yes I meant zip code. I just moved here from France........What were you doing on Monday before you vomitted? \nCaller: I was out at Darcy's Restaurant on Linx Drive. It was opening week and the food was good. I had the char but the first order tasted odd. So I sent back and got the beef tacos. Other than that, I didn't do much that day or the days prior. \nOperator: Sounds like you may have food poissoning. I can prescribe some medicine for you at the local pharmacy. If you give me your credit card number, I can put it on file and you can pick it up at the Samo Pharmacy on Arctic Blvd. \nCaller: Yes that sounds great! My card is 7283-1234-5678-1290 expiring 10/23 and CCV 009. \nOperator: And to make sure I'm prescibing the right medication, can you let me know your age and any relevent medical history? \nCaller: I'm 35 and have no major medical concerns. I just have a small allergy to dogs. \nOperator: Sounds good. I've sent a prescription to your local pahramcy. You should be ablr to pick it up by 4pm today."
]
analyze_response_1 = [
    {
        "entities": [
            {
                "text": "Operator",
                "location": {"stt_idx": 0, "end_idx": 8},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9141576886177063},
            },
            {
                "text": "City Help Line",
                "location": {"stt_idx": 29, "end_idx": 43},
                "best_label": "ORGANIZATION",
                "labels": {"ORGANIZATION": 0.899942139784495},
            },
            {
                "text": "Sean James",
                "location": {"stt_idx": 56, "end_idx": 66},
                "best_label": "NAME",
                "labels": {
                    "NAME_GIVEN": 0.36585991382598876,
                    "NAME": 0.911472886800766,
                    "NAME_FAMILY": 0.4618450403213501,
                },
            },
            {
                "text": "Russel Forkton",
                "location": {"stt_idx": 140, "end_idx": 154},
                "best_label": "NAME",
                "labels": {
                    "NAME_GIVEN": 0.3860845480646406,
                    "NAME": 0.9096945077180862,
                    "NAME_FAMILY": 0.4553850442171097,
                },
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 170, "end_idx": 178},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.911968469619751},
            },
            {
                "text": "Russel",
                "location": {"stt_idx": 232, "end_idx": 238},
                "best_label": "NAME_GIVEN",
                "labels": {"NAME_GIVEN": 0.890722006559372, "NAME": 0.9068656861782074},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 266, "end_idx": 274},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9152776002883911},
            },
            {
                "text": "Russel",
                "location": {"stt_idx": 276, "end_idx": 282},
                "best_label": "NAME_GIVEN",
                "labels": {
                    "NAME": 0.9107279181480408,
                    "NAME_GIVEN": 0.8870137333869934,
                },
            },
            {
                "text": "doctor",
                "location": {"stt_idx": 460, "end_idx": 466},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9222273826599121},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 526, "end_idx": 534},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9173893332481384},
            },
            {
                "text": "Anchorage, Alaska",
                "location": {"stt_idx": 751, "end_idx": 768},
                "best_label": "LOCATION",
                "labels": {
                    "LOCATION": 0.9226748943328857,
                    "LOCATION_CITY": 0.5026662595131818,
                    "LOCATION_STATE": 0.33603206802816954,
                },
                "analysis_result": {
                    "subtypes": [
                        {
                            "text": "Anchorage",
                            "label": "LOCATION_CITY",
                            "location": {"stt_idx": 751, "end_idx": 760},
                        },
                        {
                            "text": "Alaska",
                            "label": "LOCATION_STATE",
                            "location": {"stt_idx": 762, "end_idx": 768},
                        },
                    ],
                    "validation_assertions": [],
                },
            },
            {
                "text": "99515",
                "location": {"stt_idx": 834, "end_idx": 839},
                "best_label": "LOCATION_ZIP",
                "labels": {
                    "LOCATION_ZIP": 0.952562689781189,
                    "LOCATION": 0.9334616462389628,
                },
            },
            {
                "text": "12387654",
                "location": {"stt_idx": 863, "end_idx": 871},
                "best_label": "HEALTHCARE_NUMBER",
                "labels": {"HEALTHCARE_NUMBER": 0.9383221715688705},
            },
            {
                "text": "3 days",
                "location": {"stt_idx": 957, "end_idx": 963},
                "best_label": "DURATION",
                "labels": {"DURATION": 0.9456221461296082},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 980, "end_idx": 988},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9156421422958374},
            },
            {
                "text": "France",
                "location": {"stt_idx": 1076, "end_idx": 1082},
                "best_label": "LOCATION_COUNTRY",
                "labels": {
                    "LOCATION_COUNTRY": 0.9481866359710693,
                    "LOCATION": 0.934725284576416,
                },
            },
            {
                "text": "Darcy's Restaurant",
                "location": {"stt_idx": 1163, "end_idx": 1181},
                "best_label": "ORGANIZATION",
                "labels": {
                    "NAME": 0.05924723007612758,
                    "NAME_GIVEN": 0.048312795244985156,
                    "ORGANIZATION": 0.9065962582826614,
                },
            },
            {
                "text": "Linx Drive",
                "location": {"stt_idx": 1185, "end_idx": 1195},
                "best_label": "LOCATION_ADDRESS_STREET",
                "labels": {
                    "LOCATION": 0.9210019111633301,
                    "LOCATION_ADDRESS": 0.8472446004549662,
                    "LOCATION_ADDRESS_STREET": 0.9137071371078491,
                },
            },
            {
                "text": "day",
                "location": {"stt_idx": 1365, "end_idx": 1368},
                "best_label": "DURATION",
                "labels": {"DURATION": 0.7074118852615356},
            },
            {
                "text": "days",
                "location": {"stt_idx": 1376, "end_idx": 1380},
                "best_label": "DURATION",
                "labels": {"DURATION": 0.6593054533004761},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 1389, "end_idx": 1397},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9270487427711487},
            },
            {
                "text": "Samo Pharmacy",
                "location": {"stt_idx": 1593, "end_idx": 1606},
                "best_label": "ORGANIZATION_MEDICAL_FACILITY",
                "labels": {
                    "ORGANIZATION": 0.9179188162088394,
                    "ORGANIZATION_MEDICAL_FACILITY": 0.9367475360631943,
                },
            },
            {
                "text": "Arctic Blvd",
                "location": {"stt_idx": 1610, "end_idx": 1621},
                "best_label": "LOCATION_ADDRESS_STREET",
                "labels": {
                    "LOCATION_ADDRESS": 0.784077306588491,
                    "LOCATION": 0.8879159688949585,
                    "LOCATION_ADDRESS_STREET": 0.8508630990982056,
                },
            },
            {
                "text": "7283-1234-5678-1290",
                "location": {"stt_idx": 1666, "end_idx": 1685},
                "best_label": "CREDIT_CARD",
                "labels": {"CREDIT_CARD": 0.9159488298676229},
                "analysis_result": {
                    "subtypes": [],
                    "validation_assertions": [
                        {"provider": "luhn", "status": "unknown"}
                    ],
                },
            },
            {
                "text": "10/23",
                "location": {"stt_idx": 1695, "end_idx": 1700},
                "best_label": "CREDIT_CARD_EXPIRATION",
                "labels": {"CREDIT_CARD_EXPIRATION": 0.8779167930285136},
            },
            {
                "text": "009",
                "location": {"stt_idx": 1709, "end_idx": 1712},
                "best_label": "CVV",
                "labels": {"CVV": 0.939374566078186},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 1715, "end_idx": 1723},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.919155478477478},
            },
            {
                "text": "35",
                "location": {"stt_idx": 1855, "end_idx": 1857},
                "best_label": "AGE",
                "labels": {"AGE": 0.9608771204948425},
                "analysis_result": {
                    "formatted": 35,
                    "subtypes": [],
                    "validation_assertions": [],
                },
            },
            {
                "text": "small allergy to dogs",
                "location": {"stt_idx": 1908, "end_idx": 1929},
                "best_label": "CONDITION",
                "labels": {"CONDITION": 0.6666376143693924},
            },
            {
                "text": "Operator",
                "location": {"stt_idx": 1932, "end_idx": 1940},
                "best_label": "OCCUPATION",
                "labels": {"OCCUPATION": 0.9210088849067688},
            },
            {
                "text": "4pm",
                "location": {"stt_idx": 2040, "end_idx": 2043},
                "best_label": "TIME",
                "labels": {"TIME": 0.9443846344947815},
            },
        ],
        "entities_present": True,
        "characters_processed": 2050,
        "languages_detected": {"en": 0.9613739848136902},
    }
]
