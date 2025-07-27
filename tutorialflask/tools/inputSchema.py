from time import time
from tools.cerberus_validator import generate_path_field_in_es
from config.configer import Configer

myConf = Configer()
# Cerberus provides powerful yet simple and lightweight data validation functionality out of the box and is designed to be easily extensible, allowing for custom validation.

category_list = [
    "keywords",
    "hashtags_one",
    "hashtags_multi",
    "person",
    "organization",
    "dateTime",
    "event",
    "location",
    "emoji",
    "emails",
    "cardNumbers",
    "numbers",
    "country",
    "province",
    "city",
    "place",
    "link",
    "main_link",
    "mentioned_link",
    "main_user",
    "mentioned_user"
]


# Generate cerberus schema
class InputSchema:

    @staticmethod
    def pagination(page=1, limit=100):
        paginition_schema = {
            "pagination": {
                "type": "dict",
                "default": {
                    "page": page,
                    "limit": limit
                },
                "schema": {
                    "limit": {
                        "type": "integer",
                        "default": 100,
                        "min": 0,
                        "max": 1000
                    },
                    "page": {
                        "type": "integer",
                        "default": 1,
                        "min": 0,
                        "max": 1000
                    }
                }
            }
        }
        return paginition_schema

    @staticmethod
    def extra_sort_schema():
        filter_schema = {
            "extrasort": {
                "type": "dict",
                "schema": {
                    "field": {
                        "type": "string",
                        "empty": True,
                        # "default": "positive",
                        "allowed": [
                            "positive",
                            "negative"
                        ]
                    },
                    "order": {
                        "type": "string",
                        "default": "desc",
                        "allowed": [
                            "asc",
                            "desc"
                        ]
                    }
                }
            }
        }
        return filter_schema

    @staticmethod
    def filter():
        filter_schema = {
            "timeseries_setting": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean",
                        "default": False
                    },
                    "data": {
                        "type": "dict",
                        "schema": {
                            "type": {
                                "type": "string",
                                "allowed": ["gap_time", "bar_count"],
                                "default": "bar_count"
                            },
                            "value": {
                                "type": "string",
                                "default": str(myConf.get("es", "bar_count")),
                            }
                        }
                    }
                }
            },
            "sort": {
                "type": "dict",
                "schema": {
                    "field": {
                        "type": "string",
                        "empty": True,
                        # "default": "publish_date",
                        "allowed": [
                            "positive",
                            "negative",
                            "publish_date",
                            "text_similarity",
                            "text_exact"
                        ]
                    },
                    "order": {
                        "type": "string",
                        "default": "desc",
                        "allowed": [
                            "asc",
                            "desc"
                        ]
                    }
                }
            },
            "timespan": {
                "type": "dict",
                "required": False,
                "schema": {
                    "type": {
                        "type": "string",
                        "allowed": ["date", "period"]
                    },
                    "date": {
                        "type": "dict",
                        "required": False,
                        "range": True,
                        "schema": {
                            "start": {
                                'nullable': True,
                                "type": "integer",
                                "min": 1420113600 * 1000,
                                "max": 1000000000000000000000000000
                            },
                            "end": {
                                'nullable': True,
                                "type": "integer",
                                "min": 1420113600 * 1000,
                                "max": 100000000000000000000000000
                            }
                        }
                    },
                    "period": {
                        "type": "dict",
                        "required": False,
                        "schema": {
                            "type": {
                                "type": "string",
                                'nullable': True,
                                "allowed": [
                                    "s"
                                    "m",
                                    "h",
                                    "d",
                                    "w",
                                    "M"
                                ]
                            },
                            "value": {
                                "type": "integer",
                                'nullable': True,
                            }
                        }
                    }
                }
            },
            "platform": {
                "type": "dict",
                "required": False,
                "empty": False,
                "default": {
                    "isActive": False,
                    "data": [
                        "instagram",
                        "instagram_comment",
                        "instagram_story",
                        "telegram",
                        # "facebook",
                        "twitter",
                        # "rss",
                        # "web",
                        # "newspaper",
                        "eitaa"
                    ]
                },
                "schema": {
                    "isActive": {
                        "type": "boolean",
                        "default": False
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "allowed": [
                                "instagram",
                                "instagram_comment",
                                "instagram_story",
                                "telegram",
                                # "facebook",
                                "twitter",
                                # "rss",
                                # "web",
                                # "newspaper",
                                "eitaa"
                            ]
                        },
                        "default": [
                            "instagram",
                            "instagram_comment",
                            "instagram_story",
                            "telegram",
                            # "facebook",
                            "twitter",
                            # "rss",
                            # "web",
                            # "newspaper",
                            "eitaa"
                        ]
                    }
                }
            },
            "words": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "type": {
                                    "type": "string",
                                    "allowed": [
                                        "hashtags_one",
                                        "hashtags_multi",
                                        "keywords",
                                        "subject"
                                    ]
                                },
                                "value": {
                                    "type": "string",
                                    "empty": False
                                },
                                "status": {
                                    "type": "string",
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "regularExpression": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "string"
                    }
                }
            },
            "hasImage": {
                "type": "boolean",
                "required": False
            },
            "sentiment": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "allowed": [
                                "positive",
                                "negative",
                                "neutral"
                            ]
                        }
                    }
                }
            },
            "behavior": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "value": {
                                    "type": "string",
                                    "empty": False,
                                    "allowed": [
                                        "shak_tardid",
                                        "naRahati",
                                        "etemad_etminan",
                                        "tohin_tamaskhor",
                                        "porseshi",
                                        "tamjid_defa_tarafdari",
                                        "rezayat",
                                        "tavgho_darkhast",
                                        "asabaniat",
                                        "taajob",
                                        "shadi_khoshhali",
                                        "tanafor",
                                        "omid",
                                        "tahrik_targhib",
                                        "naOmidi",
                                        "tars_negarani",
                                        "dastoori",
                                        "khonsa",
                                        "vahshat",
                                        "gham_afsordegi"
                                    ]
                                },
                                "status": {
                                    "type": "string",
                                    "empty": False,
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "topicAnalyzer": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "value": {
                                    "type": "string",
                                    "empty": False,
                                    "allowed": [
                                        "varzeshi",
                                        "eghtesadi",
                                        "filmocinema",
                                        "havades",
                                        "siasi",
                                        "ejtemaee",
                                        "nezami",
                                        "tabiatvahava",
                                        "pezeshki",
                                        "adabi",
                                        "elmi",
                                        "farhangi",
                                        "honari",
                                        "amniati",
                                        "mazhabi",
                                        "mokhadderoalkol",
                                        "amozeshi",
                                        "music",
                                        "fun",
                                        "romanodastan",
                                        "ITkhabar",
                                        "tarikhi",
                                        "tablighofrosh",
                                        "mostahjan"
                                    ]
                                },
                                "status": {
                                    "type": "string",
                                    "empty": False,
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "NER": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "includes": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "allowed": category_list
                        }
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "type": {
                                    "type": "string",
                                    "allowed": category_list
                                },
                                "value": {
                                    "type": "string",
                                    "empty": False
                                },
                                "status": {
                                    "type": "string",
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "userInfo": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "includes": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "allowed": category_list
                        }
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    'empty': False
                                },
                                "type": {
                                    "type": "string",
                                    "allowed": category_list
                                },
                                "value": {
                                    "type": "string",
                                    "empty": False
                                },
                                "status": {
                                    "type": "string",
                                    "empty": False,
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "keywordCategory": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean",
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "name": {
                                    "type": "string",
                                    "empty": False
                                },
                                "status": {
                                    "type": "string",
                                    "allowed": [
                                        "and",
                                        "or",
                                        "not"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "linkCategory": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "id": {
                                    "type": "string",
                                    "empty": False
                                },
                                "public_category_name": {
                                    "type": "string",
                                    "empty": False
                                },
                                "title": {
                                    "type": "string",
                                    "empty": True
                                }
                            }
                        }
                    }
                }
            },
            "private_categories": {
                "type": "dict",
                "required": False,
                "schema": {
                    "isActive": {
                        "type": "boolean"
                    },
                    "data": {
                        "type": "list",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        }
        return filter_schema

    word_cloud_schema = {
        "chart": {
            "type": "dict",
            "schema": {
                "category": {
                    "type": "list",
                    "required": True,
                    "allowed": category_list,
                    "coerce": generate_path_field_in_es
                },
                "sort": {
                    "type": "dict",
                    "default": {
                        "key": "_count",
                        "order": "desc"
                    },
                    "schema": {
                        "key": {
                            "type": "string",
                            "allowed": ["_count"],
                            "default": "_count"
                        },
                        "order": {
                            "type": "string",
                            "regex": "asc|desc",
                            "default": "desc"
                        }
                    }
                },
                "size": {
                    "type": "integer",
                    "default": 500
                },
                "min_doc_count": {
                    "type": "integer",
                    "default": 1
                },
                "limit": {
                    "type": "integer",
                    "default": 100,
                    "min": 0,
                    "max": 1000
                },
                "page": {
                    "type": "integer",
                    "default": 0,
                    "min": 0,
                    "max": 1000
                }
            }
        }
    }

    @ staticmethod
    def word_cloud():
        word_cloud_schema = {
            "chart": {
                "type": "dict",
                "schema": {
                    "category": {
                        "type": "list",
                        "required": True,
                        "allowed": category_list,
                        "coerce": generate_path_field_in_es
                    },
                    "sort": {
                        "type": "dict",
                        "default": {
                            "key": "_count",
                            "order": "desc"
                        },
                        "schema": {
                            "key": {
                                "type": "string",
                                "allowed": ["_count"],
                                "default": "_count"
                            },
                            "order": {
                                "type": "string",
                                "regex": "asc|desc",
                                "default": "desc"
                            }
                        }
                    },
                    "size": {
                        "type": "integer",
                        "default": 500
                    },
                    "min_doc_count": {
                        "type": "integer",
                        "default": 1
                    },
                    "limit": {
                        "type": "integer",
                        "default": 100,
                        "min": 0,
                        "max": 1000
                    },
                    "page": {
                        "type": "integer",
                        "default": 0,
                        "min": 0,
                        "max": 1000
                    }
                }
            }
        }
        return word_cloud_schema

    @ staticmethod
    def geo_distance_schema():
        """
        method to create schema for geo distance input rest api
        radius scale :: km
        """
        schema = {
            "geo": {
                "type": "dict",
                "schema": {
                    "limit": {
                        "type": "integer",
                        "default": 10000
                    },
                    "category": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "allowed": category_list
                        }
                    },
                    "radius": {
                        "type": "float",
                        "required": True,
                    },
                    "coordinate": {
                        "type": "dict",
                        "required": True,
                        "schema": {
                            "lat": {
                                "type": "float"
                            },
                            "lon": {
                                "type": "float"
                            }
                        }
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def geo_bounding_box_schema():
        """
        method to create schema for geo distance input rest api
        radius scale :: km
        """
        schema = {
            "geo": {
                "type": "dict",
                "schema": {
                    "limit": {
                        "type": "integer",
                        "default": 10000
                    },
                    "category": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "empty": False,
                            "allowed": category_list
                        }
                    },
                    "coordinates": {
                        "type": "dict",
                        "required": True,
                        "schema": {
                            "top_left": {
                                "type": "dict",
                                "schema": {
                                    "lat": {
                                        "type": "float"
                                    },
                                    "lon": {
                                        "type": "float"
                                    }
                                }
                            },
                            "bottom_right": {
                                "type": "dict",
                                "schema": {
                                    "lat": {
                                        "type": "float"
                                    },
                                    "lon": {
                                        "type": "float"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def geo_grid_bounding_box_schema():
        """
        method to create schema for geo distance input rest api
        radius scale :: km
        """
        schema = {
            "geo": {
                "type": "dict",
                "schema": {
                    "category": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "empty": False,
                            "allowed": category_list
                        }
                    },
                    "coordinates": {
                        "type": "dict",
                        "required": True,
                        "schema": {
                            "top_left": {
                                "type": "dict",
                                "schema": {
                                    "lat": {
                                        "type": "float"
                                    },
                                    "lon": {
                                        "type": "float"
                                    }
                                }
                            },
                            "bottom_right": {
                                "type": "dict",
                                "schema": {
                                    "lat": {
                                        "type": "float"
                                    },
                                    "lon": {
                                        "type": "float"
                                    }
                                }
                            }
                        }
                    },
                    "precision": {
                        "type": "integer",
                        "default": 1,
                        "allowed": list(range(1, 13))
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def geo_location_schema():
        """
        method to create schema for geo location input rest api
        """
        schema = {
            "geo": {
                "type": "dict",
                "location": True,
                "schema": {
                    "limit": {
                        "type": "integer",
                        "default": 10000
                    },
                    "category": {
                        "type": "list",
                        "required": True,
                        "empty": False,
                        "schema": {
                            "type": "string",
                            "empty": False,
                            "allowed": category_list
                        }
                    },
                    "country": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "empty": False
                        }
                    },
                    "province": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "empty": False
                        }
                    },
                    "city": {
                        "type": "list",
                        "schema": {
                            "type": "string",
                            "empty": False
                        }
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def geo_polygon_schema():
        """
        method to create schema for geo location input rest api
        """
        schema = {
            "geo": {
                "type": "dict",
                "schema": {
                    "limit": {
                        "type": "integer",
                        "default": 10000
                    },
                    "category": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "empty": False,
                            "allowed": category_list
                        }
                    },
                    "polygon_points": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "lat": {
                                    "type": "float"
                                },
                                "lon": {
                                    "type": "float"
                                }
                            }
                        }
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def aux_sentiments_schema():
        sentiment_schema = {
            "aux_sentiment": {
                "type": "dict",
                "schema": {
                    "sense": {
                        "type": "list",
                        "required": False,
                        "default": [
                            'negative',
                            'positive',
                            'neutral'
                        ],
                        "schema": {
                            'type': 'string',
                            "allowed": [
                                'negative',
                                'positive',
                                'neutral'
                            ],
                        }
                    },
                    "metric": {
                        'type': "string",
                        'required': False,
                        'default': 'count',
                        "allowed": [
                            'count',
                            'avg',
                            'min_max'
                        ]
                    }
                }
            }
        }
        return sentiment_schema

    @ staticmethod
    def username_email_link_schema():
        schema = {
            "user": {
                "type": "dict",
                "schema": {
                    "username_limit": {
                        "type": "integer",
                        "default": 100,
                        "min": 1
                    },
                    "email_limit": {
                        "type": "integer",
                        "default": 100,
                        "min": 1
                    },
                    "link_limit": {
                        "type": "integer",
                        "default": 100,
                        "min": 1
                    },
                }
            }
        }
        return schema

    @ staticmethod
    def username_schema():
        schema = {
            "user": {
                "type": "dict",
                "schema": {
                    "username": {
                        "type": "string",
                        "required": True,
                        "empty": False
                    }
                }
            }
        }
        return schema

    @ staticmethod
    def keyword_schema():
        schema = {
            "keywords": {
                "type": "dict",
                "schema": {
                    "data": {
                        "type": "list",
                        "required": True,
                        "empty": False,
                        "schema": {
                            "type": "string",
                            "required": True,
                            "empty": False
                        }

                    }
                }
            }
        }
        return schema

    @ staticmethod
    def timeseries_schema():
        schema = {
            "timeseries": {
                "type": "dict",
                "schema": {
                    "interval": {
                        "type": "string",
                        "default": "day",
                        "allowed": [
                            "minute",
                            "hour",
                            "day",
                            "week",
                            "month",
                            "quarter",
                            "year",
                        ]
                    },
                }
            }
        }
        return schema
