import copy
import calendar
import jdatetime
from typing import Union
from builtins import list
from config.configer import Configer
from datetime import datetime, timedelta
#from tools.cerberus_validator import generate_path_field_in_es
#from tools.util import period, get_timestamp, remove_empty_elements, build_elastic_query_from_regular_expression

myConf = Configer()
# from elasticsearchquerygenerator.elasticsearchquerygenerator import ElasticSearchQuery

TOPICS = {
    "user", "adabi", "amniati", "amozeshi", "eghtesadi", "ejtemaee", "farhangi", "elmi",
    "filmocinema", "fun", "havades", "honari", "mazhabi", "mokhadderoalkol", "mostahjan",
    "music", "nezami", "pezeshki", "romanodastan", "siasi", "tabiatvahava", "tablighofrosh",
    "tarikhi", "varzeshi"
}

BEHAVIORALS = {
    "asabaniat", "dastoori", "etemad_etminan", "gham_afsordegi", "khonsa", "naOmidi", "vahshat"
                                                                                      "naRahati", "omid", "porseshi",
    "rezayat", "shadi_khoshhali", "shak_tardid", "tavgho_darkhast"
                                                 "taajob", "tahrik_targhib", "tamjid_defa_tarafdari", "tanafor",
    "tars_negarani", "tohin_tamaskhor"
}


class ElasticSearchQueryBuilder():

    def __init__(self, query) -> None:
        self.query = query
        self.body = {
            "size": 100,
            "from": 0,
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "should": [],
                    "minimum_should_match": 0,
                    "filter": []
                },
            },
            "indices_boost": [],
            "sort": [],
            "aggs": {},
            # "terminate_after": 19000,
            "track_total_hits": True
        }
        self.timestamps = []
        self.body_query = self.body["query"]
        self.body_query_bool = self.body["query"]["bool"]
        self.body_must = self.body["query"]["bool"]["must"]
        self.body_must_not = self.body["query"]["bool"]["must_not"]
        self.body_should = self.body["query"]["bool"]["should"]
        self.body_filter = self.body["query"]["bool"]["filter"]
        self.body_indices_boost = self.body["indices_boost"]
        self.body_aggs = self.body["aggs"]
        self.body_sort = self.body["sort"]
        self.bar_count = int(myConf.get("es", "bar_count")) - 1

        if "metadata" in self.query:
            self.metadata = self.query["metadata"]
        else:
            self.metadata = None

        if "location_finder" in self.query:
            self.location_finder = self.query["location_finder"]
        else:
            self.location_finder = None

    def _pagination_setter(self):
        if "pagination" in self.query:
            pagination = self.query["pagination"]
            self.body["size"] = pagination["limit"]
            self.body["from"] = (pagination["page"] - 1) * pagination["limit"]

    def _sort_setter(self):
        if self.query.get('sort'):
            if self.query["sort"].get("field") == "publish_date":
                self.body["sort"].append({
                    "publish_date": {
                        "order": self.query["sort"]["order"]
                    }
                })

            elif self.query["sort"].get("field") == "text_similarity":
                self.body["sort"].append({
                    "text_similarity_count": {
                        "mode": "max",
                        "order": self.query["sort"]["order"]
                    }
                })
                self.body["sort"].append({
                    "text_similarity_status": {
                        "order": "asc"
                    }
                })
            elif self.query["sort"].get("field") == "text_exact":
                self.body["sort"].append({
                    "text_exact_count": {
                        "order": self.query["sort"]["order"]
                    }
                })

    def _extra_sort_setter(self):
        if self.query.get('extrasort'):
            if self.query["extrasort"].get("field") == "positive":
                self.body_must.append({
                    "term": {
                        "sentiment_analysis.state": {
                            "value": 1
                        }
                    }
                })
                self.body["sort"].append({
                    "sentiment_analysis.probabilities.positive": {
                        "order": self.query["sort"]["order"]
                    }
                })

            elif self.query["extrasort"].get("field") == "negative":
                self.body_must.append({
                    "term": {
                        "sentiment_analysis.state": {
                            "value": -1
                        }
                    }
                })
                self.body["sort"].append({
                    "sentiment_analysis.probabilities.negative": {
                        "order": self.query["sort"]["order"]
                    }
                })

    def _topic_analysis_setter(self):
        if "topicAnalyzer" in self.query and self.query["topicAnalyzer"]["isActive"]:
            for item in self.query["topicAnalyzer"]["data"]:
                if item["status"] == "and":
                    self.body_must.append({
                        "exists": {
                            "field": f"topic_analysis.{item.get('value')}"
                        }
                    })
                elif item["status"] == "not":
                    self.body_must_not.append({
                        "exists": {
                            "field": f"topic_analysis.{item.get('value')}"
                        }
                    })
                elif item["status"] == "or":
                    self.body_should.append({
                        "exists": {
                            "field": f"topic_analysis.{item.get('value')}"
                        }
                    })

    def _behavioral_analysis_setter(self):
        if "behavior" in self.query and self.query["behavior"]["isActive"]:
            for item in self.query["behavior"]["data"]:
                if item["status"] == "and":
                    self.body_must.append({
                        "exists": {
                            "field": f"behavioral_analysis.{item.get('value')}"
                        }
                    })
                elif item["status"] == "not":
                    self.body_must_not.append({
                        "exists": {
                            "field": f"behavioral_analysis.{item.get('value')}"
                        }
                    })
                elif item["status"] == "or":
                    self.body_should.append({
                        "exists": {
                            "field": f"behavioral_analysis.{item.get('value')}"
                        }
                    })

    def _sentiment_analysis_setter(self):
        query_exists = {
            "exists": {
                "field": "sentiment_analysis"
            }
        }
        if "sentiment" in self.query:

            if self.query["sentiment"]["isActive"]:
                self.body_must.append(query_exists)

                schema_state = {
                    "terms": {
                        "sentiment_analysis.state": []
                    }
                }
                for state in self.query["sentiment"]["data"]:
                    if state == "positive":
                        schema_state["terms"]["sentiment_analysis.state"].append(
                            1)
                    elif state == "negative":
                        schema_state["terms"]["sentiment_analysis.state"].append(
                            -1)
                    elif state == "neutral":
                        schema_state["terms"]["sentiment_analysis.state"].append(
                            0)

                self.body_must.append(schema_state)

    def _keywords_setter(self):
        if "regularExpression" in self.query and self.query["regularExpression"]["isActive"] and self.query["regularExpression"]["data"] != "":
            regular_expression_query = build_elastic_query_from_regular_expression(
                expression=self.query.get("regularExpression", {}).get("data", ""))
            if not regular_expression_query.get("error"):
                must = regular_expression_query.get(
                    "query", {}).get("bool", {}).get("must")
                must_not = regular_expression_query.get(
                    "query", {}).get("bool", {}).get("must_not")
                should = regular_expression_query.get(
                    "query", {}).get("bool", {}).get("should")
                if must:
                    self.body_must.extend(must)
                if must_not:
                    self.body_must_not.extend(must_not)
                if should:
                    self.body_should.extend(should)

        elif "words" in self.query and self.query["words"]["isActive"]:
            for item in self.query["words"]["data"]:
                if item["type"] == "keywords":
                    aggs = {
                        "term": {
                            "keywords.keyword": {
                                "value": item["value"]
                            }
                        }
                    }
                    if item["status"] == "and":
                        self.body_must.append(aggs)
                    elif item["status"] == "not":
                        self.body_must_not.append(aggs)
                    elif item["status"] == "or":
                        self.body_should.append(aggs)
                elif item["type"] == "hashtags_one":
                    aggs = {
                        "term": {
                            "metadata.hashtags_one.hashtag.keyword": {
                                "value": item["value"]
                            }
                        }
                    }
                    if item["status"] == "and":
                        self.body_must.append(aggs)
                    elif item["status"] == "not":
                        self.body_must_not.append(aggs)
                    elif item["status"] == "or":
                        self.body_should.append(aggs)
                elif item["type"] == "hashtags_multi":
                    aggs = {
                        "term": {
                            "metadata.hashtags_multi.hashtag.keyword": {
                                "value": item["value"]
                            }
                        }
                    }
                    if item["status"] == "and":
                        self.body_must.append(aggs)
                    elif item["status"] == "not":
                        self.body_must_not.append(aggs)
                    elif item["status"] == "or":
                        self.body_should.append(aggs)
                elif item["type"] == "subject":
                    if item["status"] == "and":
                        # self.body_must.append({
                        #     "match_phrase": {
                        #         "text": item["value"]
                        #     }
                        # })
                        value = item["value"]
                        self.body_must.append(
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "wildcard": {
                                                "metadata.hashtags.hashtag": {
                                                    "value": f"*{value}*"
                                                }
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "text": value
                                            }
                                        }
                                    ]
                                }
                            }
                        )
                    elif item["status"] == "not":
                        self.body_must_not.append({
                            "match_phrase": {
                                "text": value
                            }
                        })
                    elif item["status"] == "or":
                        self.body_should.append({
                            "match_phrase": {
                                "text": value
                            }
                        })

    def _ner_setter(self):
        if "NER" in self.query and self.query["NER"]["isActive"]:
            for item in self.query["NER"]["data"]:
                query = {"term": {generate_path_field_in_es(
                    item["type"]): item["value"]}}
                if item["status"] == "and":
                    self.body_must.append(query)
                elif item["status"] == "not":
                    self.body_must_not.append(query)
                elif item["status"] == "or":
                    self.body_should.append(query)
            for item in self.query["NER"]["includes"]:
                self.body_must.append(
                    {"exists": {"field": generate_path_field_in_es(item)}})

    def _has_image(self):
        query_exists = {
            "exists": {
                "field": "media.images"
            }
        }
        if "hasImage" in self.query and self.query["hasImage"]:
            self.body_must.append(query_exists)

    def _timestamps_setter(self):
        if "timespan" in self.query:
            timespan = self.query["timespan"]
            timespan_type = timespan["type"]
            if timespan_type == "date":
                self.timestamps.append(timespan["date"]["start"] / 1000)
                self.timestamps.append(timespan["date"]["end"] / 1000)
            elif timespan_type == "period":
                time_period = period(
                    timespan["period"]["type"], timespan["period"]["value"])
                self.timestamps.append(time_period[0])
                self.timestamps.append(time_period[1])

        if not self.timestamps:
            self.timestamps.append(get_timestamp() - (60 * 60 * 24 * 30))
            self.timestamps.append(get_timestamp())

        self.body_filter.append({
            "range": {
                "timestamp": {
                    "gte": float(self.timestamps[0]),
                    "lte": float(self.timestamps[1])
                }
            }
        })

    def _user_info(self):
        """
        search user info
        """
        if "userInfo" in self.query and self.query["userInfo"]["isActive"]:
            includes = self.query["userInfo"]["includes"]
            for included in includes:
                self.body_must.append(
                    {"exists": {"field": generate_path_field_in_es(included)}})
            data = self.query["userInfo"]["data"]
            for item in data:
                query = {"term": {generate_path_field_in_es(
                    item["type"]): item["value"]}}
                if item["status"] == "and":
                    self.body_must.append(query)
                elif item["status"] == "not":
                    self.body_must_not.append(query)
                elif item["status"] == "or":
                    self.body_should.append(query)

    def _keyword_category(self):
        pass

    def _link_category(self):
        if "linkCategory" in self.query and self.query["linkCategory"]["isActive"]:
            grouped_data = {}
            for item in self.query["linkCategory"]["data"]:
                if grouped_data.get(item["public_category_name"]) is None:
                    grouped_data[item["public_category_name"]] = []
                grouped_data[item["public_category_name"]].append(item)
            for key, value in grouped_data.items():
                or_conditions = []
                for filter in value:
                    condition = {
                        "term": {
                            str(filter["public_category_name"]) + ".keyword": {
                                "value": filter["id"]
                            }
                        }
                    }
                    or_conditions.append(condition)
                or_conditions = {"bool": {"should": or_conditions}}
                self.body_must.append(or_conditions)

    def _links_setter(self):
        if "privateCategories" in self.query and self.query["privateCategories"]["isActive"]:
            private_categories = self.query["privateCategories"]["data"]
            if private_categories != [] and type(private_categories) == list:
                mongodb_management_obj = MongoDBManagement()
                links = mongodb_management_obj.get_private_category_links(
                    private_category_ids=private_categories)
                condition = {
                    "terms": {
                        "link_info.url.keyword": links.get("links", [])
                    }
                }
                self.body_must.append(condition)
                return links.get("notify")
            return "لیست دسته بندی های خصوصی خالی است"
        return "(تمامی لینک ها مورد بررسی قرار می گیرد ) لیست دسته بندی های خصوصی غیر فعال است"

    ######################################################################
    # AGGS
    def word_cloud_main(self, _category, _min_doc_count, _order, _from, _size):

        _category_in_es = generate_path_field_in_es(_category)

        aggs = {
            "aggs": {
                "chart": {
                    "terms": {
                        "field": _category_in_es,
                        "min_doc_count": _min_doc_count,
                        "size": 500
                    },
                    "aggs": {
                        "sort": {
                            "bucket_sort": {
                                "sort": [
                                    {
                                        "_count": {
                                            "order": _order
                                        }
                                    }
                                ],
                                "from": _from,
                                "size": _size
                            }
                        }
                    }
                }
            }
        }
        self.body_aggs.update(aggs["aggs"])

    def count_all(self):
        aggs = {
            "aggs": {
                "platforms": {
                    "terms": {
                        "field": "platform.keyword"
                    }
                },
                "count_total": {
                    "value_count": {
                        "field": "platform.keyword"
                    }
                }
            },
            "track_total_hits": True,
            "size": 0
        }
        self.body_aggs.update(aggs["aggs"])

    def by_sentiment_analysis(self, timestamps, metric='count'):
        interval_clause = self.get_interval_clause(timestamps)
        aggs = {
            "aggs": {
                "all_data_model": {
                    "aggs": dict(),
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause,
                    }
                }
            }
        }
        if metric == 'count':
            aggs['aggs']['all_data_model']['aggs'].update({"sentiment_count": {
                "terms": {
                    "field": "sentiment_analysis.state"
                }
            }})
        if metric == 'avg':
            aggs['aggs']['all_data_model']['aggs'].update(
                {
                    "negative_avg": {
                        "avg": {
                            "field": "sentiment_analysis.probabilities.negative"
                        }
                    },
                    "neutral_avg": {
                        "avg": {
                            "field": "sentiment_analysis.probabilities.neutral"
                        }
                    },
                    "positive_avg": {
                        "avg": {
                            "field": "sentiment_analysis.probabilities.positive"
                        }
                    },
                }
            )
        if metric == 'min_max':
            dct = dict()
            for el in ['max', 'min']:
                for state in ['positive', 'neutral', 'negative']:
                    dct[f'{state}_{el}'] = {
                        f'{el}': {
                            "field": f"sentiment_analysis.probabilities.{state}"
                        }
                    }

            aggs['aggs']['all_data_model']['aggs'].update(dct)
        self.body_aggs.update(aggs["aggs"])

    def get_username_sentiment(self, size):
        aggs = {
            "aggs": {
                "user_username_model": {
                    "aggs": {
                        "sentiment_count": {
                            "terms": {
                                "field": "sentiment_analysis.state"
                            }
                        }
                    },
                    "terms": {
                        "field": "user.username.keyword",
                        "size": size
                    }
                }
            }
        }
        self.body_aggs.update(aggs["aggs"])

    def get_ner_sentiment_count(self, size, ner):
        field = self._generate_ner_term_query(ner)
        aggs = {
            "aggs": {
                "ner_model": {
                    "aggs": {
                        "sentiment_count": {
                            "terms": {
                                "field": "sentiment_analysis.state"
                            }
                        }
                    },
                    "terms": {
                        "field": field,
                        "size": size
                    }
                }
            }
        }
        self.body_aggs.update(aggs['aggs'])

    def _generate_ner_term_query(self, ner_name):
        field = 'person'
        if ner_name == "datetime":
            field = "ners_info.dateTime.keyword"
        elif ner_name == "location":
            field = "ners_info.location.keyword"
        elif ner_name == "event":
            field = "ners_info.event.keyword"
        elif ner_name == "organization":
            field = "ners_info.organization.keyword"
        elif ner_name == "person":
            field = "ners_info.person.keyword"
        return field

    def get_behevioral_count(self):
        aggs = dict()
        for behavor in BEHAVIORALS:
            aggs.update({
                behavor: {
                    "value_count": {
                        "field": f"behavioral_analysis.{behavor}"
                    }
                }
            })
        self.body_aggs.update(aggs)

    def get_topics_count(self):
        aggs = dict()
        for topic in TOPICS:
            aggs.update({
                topic: {
                    "value_count": {
                        "field": f"topic_analysis.{topic}"
                    }
                }
            })
        self.body_aggs.update(aggs)

    def get_behevioral_histogram(self, timestamps):
        interval_clause = self.get_interval_clause(timestamps)
        aggs = {
            "all_data_model": {
                "aggs": dict(),
                "date_histogram": {
                    "extended_bounds": {
                        "max": timestamps[1] * 1000,
                        "min": timestamps[0] * 1000
                    },
                    "field": "publish_date",
                    "interval": interval_clause
                }
            }
        }

        for behavor in BEHAVIORALS:
            aggs["all_data_model"]["aggs"].update({
                behavor: {
                    "value_count": {
                        "field": f"behavioral_analysis.{behavor}"
                    }
                }
            })

        self.body_aggs.update(aggs)

    def get_keyword_histogram(self, timestamps, keywords: list):
        should = [{"term": {"keywords.keyword": {"value": el}}}
                  for el in keywords]
        must = {
            'range': {
                'timestamp': {
                    'gte': timestamps[0],
                    'lte': timestamps[1]
                }
            }
        }
        output = {
            "query": {
                "bool": {
                    "should": should,
                    "must": must
                }
            },
            "aggs": {
                "all_data_model": {
                    "aggs": {
                        "keywords": {
                            "terms": {
                                "field": "keywords.keyword",
                                "size": 100
                            }
                        }
                    },
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": "day"
                    }
                }
            },
            "size": 0
        }
        return output

    def get_geo_distance(self, timestamps, _category, geo, size=10):

        self.body["size"] = size
        self.body_filter.append(
            {
                "geo_distance": {
                    "distance": f"{geo.get('radius', 0)}km",
                    "location_finder.coordinate": {
                        "lat": geo.get('coordinate', dict()).get('lat', 0),
                        "lon": geo.get('coordinate', dict()).get('lon', 0)
                    }
                }
            }
        )

        return self.body

    def get_geo_distance_new(self, geo, size=10):

        self.body_filter.append(
            {
                "geo_distance": {
                    "distance": f"{geo.get('radius', 0)}km",
                    "location_finder.coordinate": {
                        "lat": geo.get('coordinate', dict()).get('lat', 0),
                        "lon": geo.get('coordinate', dict()).get('lon', 0)
                    }
                }
            }
        )
        self.body_aggs.update(
            {
                "geo": {
                    "terms": {
                        "field": "location_finder.full_address.keyword",
                        "size": int(1000 / (len(geo.get('category', list())) + 1))
                    },
                    "aggs": {
                        cat: {
                            "terms": {
                                "field": generate_path_field_in_es(cat),
                                "size": size
                            },
                        } for cat in geo.get('category', list())
                    }
                }
            }
        )
        self.body["size"] = 0
        return self.body

    def get_geo_bounding_box(self, timestamps, _category, geo, size=10):

        self.body["size"] = size
        self.body_filter.append(
            {
                "geo_bounding_box": {
                    "location_finder.coordinate": {
                        "top_left": {
                            "lat": geo.get('coordinates', dict()).get('top_left', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('top_left', dict()).get('lon', 0)
                        },
                        "bottom_right": {
                            "lat": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lon', 0)
                        }
                    }
                }
            }
        )

        return self.body

    def get_geo_bounding_box_new(self, geo, size=10):

        self.body_filter.append(
            {
                "geo_bounding_box": {
                    "location_finder.coordinate": {
                        "top_left": {
                            "lat": geo.get('coordinates', dict()).get('top_left', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('top_left', dict()).get('lon', 0)
                        },
                        "bottom_right": {
                            "lat": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lon', 0)
                        }
                    }
                }
            }
        )
        self.body_aggs.update(
            {
                "geo": {
                    "terms": {
                        "field": "location_finder.full_address.keyword",
                        "size": 80
                    },
                    "aggs": {
                        cat: {
                            "terms": {
                                "field": generate_path_field_in_es(cat),
                                "size": size
                            },
                        } for cat in geo.get('category', list())
                    }
                }
            }
        )

        self.body["size"] = 0
        return self.body

    def get_geo_grid_bounding_box(self, geo):
        self.body_filter.append(
            {
                "geo_bounding_box": {
                    "location_finder.coordinate": {
                        "top_left": {
                            "lat": geo.get('coordinates', dict()).get('top_left', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('top_left', dict()).get('lon', 0)
                        },
                        "bottom_right": {
                            "lat": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lat', 0),
                            "lon": geo.get('coordinates', dict()).get('bottom_right', dict()).get('lon', 0)
                        }
                    }
                }
            }
        )
        self.body_aggs.update(
            {
                "geo_grid": {
                    "geohash_grid": {
                        "field": "location_finder.coordinate",
                        "precision": geo.get('precision', 1)
                    },
                    "aggs": {
                        cat: {
                            "terms": {
                                "field": generate_path_field_in_es(cat)}
                        } for cat in geo.get('category', list())
                    }
                }
            }
        )
        self.body["size"] = 0
        return self.body

    def get_geo_polygon(self, timestamps, _category, geo, size=10):

        self.body["size"] = size
        self.body_filter.append(
            {
                "geo_polygon": {
                    "location_finder.coordinate": {
                        "points": geo.get("polygon_points", list())
                    }
                }
            }
        )

        return self.body

    def get_geo_location(self, timestamps, _category, geo, size=10):

        location = None
        field_path = None

        if geo.get("country"):
            field_path = "location_finder.country.keyword"
            location = geo.get("country")
        elif geo.get("province"):
            field_path = "location_finder.province.keyword"
            location = geo.get("province")
        elif geo.get("city"):
            field_path = "location_finder.city.keyword"
            location = geo.get("city")

        self.body["size"] = size
        lst = [{"term": {field_path: location[i]}}
               for i in range(len(location))]

        self.body_should.extend(lst)
        return self.body

    def get_geo_location_new(self, geo, size=10):

        location = None
        field_path = None

        if geo.get("country"):
            field_path = "location_finder.country.keyword"
            location = geo.get("country")
        elif geo.get("province"):
            field_path = "location_finder.province.keyword"
            location = geo.get("province")
        elif geo.get("city"):
            field_path = "location_finder.city.keyword"
            location = geo.get("city")

        self.body_aggs.update(
            {
                "geo": {
                    "terms": {
                        "field": "location_finder.full_address.keyword",
                        "size": 150
                    },
                    "aggs": {
                        cat: {
                            "terms": {
                                "field": generate_path_field_in_es(cat),
                                "size": size
                            },
                        } for cat in geo.get('category', list())
                    }
                }
            }
        )

        self.body["size"] = 0
        lst = [{"term": {field_path: location[i]}}
               for i in range(len(location))]

        self.body_should.extend(lst)
        return self.body

    def get_username_email_link(self, user):
        """
        method to generate elastic query
        """
        username_limit = user.get('username_limit', 100)
        email_limit = user.get('email_limit', 100)
        link_limit = user.get('link_limit', 100)

        aggs = {
            "username_count": {
                "terms": {
                    "field": "user.username.keyword",
                    "size": username_limit
                },
                "aggs": {
                    "platform_count": {
                        "terms": {
                            "field": "platform.keyword"
                        }
                    }
                }
            },
            "email_count": {
                "terms": {
                    "field": "metadata.emails.email.keyword",
                    "size": email_limit
                },
                "aggs": {
                    "platform_count": {
                        "terms": {
                            "field": "platform.keyword"
                        }
                    }
                }
            },
            "link_count": {
                "terms": {
                    "field": "user.url.keyword",
                    "size": link_limit
                },
                "aggs": {
                    "platform_count": {
                        "terms": {
                            "field": "platform.keyword"
                        }
                    }
                }
            },
            "platform_count": {
                "terms": {
                    "field": "platform.keyword"
                }
            }
        }

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_username(self, user):
        """
        method to generate elastic query
        """
        username = user.get("username", "")

        self.body_must.append({
            "term": {
                "user.username": {
                    "value": username
                }
            }
        })
        aggs = dict()
        for behavor in BEHAVIORALS:
            aggs.update({
                behavor: {
                    "value_count": {
                        "field": f"behavioral_analysis.{behavor}"
                    }
                }
            })
        for topic in TOPICS:
            aggs.update({
                topic: {
                    "value_count": {
                        "field": f"topic_analysis.{topic}"
                    }
                }
            })
        aggs.update({
            "sens": {
                "terms": {
                    "field": "sentiment_analysis.state"
                }
            }
        })
        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_username_email_link_timeseries(self, timeseries):
        """
        method to generate elastic query for 
        """

        interval = timeseries.get('interval', "day")

        aggs = {
            "username_link_email": {
                "aggs": {
                    "email": {
                        "value_count": {
                            "field": "metadata.emails.email.keyword"
                        }
                    },
                    "link": {
                        "value_count": {
                            "field": "metadata.urls.url.keyword"
                        }
                    },
                    "username": {
                        "value_count": {
                            "field": "metadata.usernames.username.keyword"
                        }
                    }
                },
                "date_histogram": {
                    "field": "publish_date",
                    "interval": interval
                }
            }
        }

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_phone_card_timeseries(self, timeseries):
        """
        method to generate elastic query for 
        """

        interval = timeseries.get('interval', "day")

        aggs = {
            "phone_card": {
                "aggs": {
                    "platforms": {
                        "terms": {
                            "field": "platform.keyword"
                        },
                        "aggs": {
                            "phone": {
                                "value_count": {
                                    "field": "metadata.numbers.number.keyword"
                                }
                            },
                            "card": {
                                "value_count": {
                                    "field": "metadata.cardNumbers.cardNumber.keyword"
                                }
                            }
                        }
                    }
                },
                "date_histogram": {
                    "field": "publish_date",
                    "interval": interval
                }
            }
        }

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_phone_count(self, should, must_not):
        """
        method to generate elastic query for 
        """
        aggs = {
            "phone_count": {
                "value_count": {
                    "field": "metadata.numbers.number.keyword"
                }
            }
        }

        should_query = [{
            "prefix": {
                "metadata.numbers.number": {
                    "value": code
                }
            }
        } for code in should]

        must_not_query = [{
            "prefix": {
                "metadata.numbers.number": {
                    "value": code
                }
            }
        } for code in must_not]

        self.body_should.extend(should_query)
        self.body_must_not.extend(must_not_query)

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_phone_count_timeseries(self, should, must_not, interval):
        """
        method to generate elastic query for 
        """
        aggs = {
            "phone_count": {
                "aggs": {
                    "phone_count": {
                        "value_count": {
                            "field": "metadata.numbers.number.keyword"
                        }
                    }
                },
                "date_histogram": {
                    "field": "publish_date",
                    "interval": interval
                }
            }
        }

        should_query = [{
            "prefix": {
                "metadata.numbers.number": {
                    "value": code
                }
            }
        } for code in should]

        must_not_query = [{
            "prefix": {
                "metadata.numbers.number": {
                    "value": code
                }
            }
        } for code in must_not]

        self.body_should.extend(should_query)
        self.body_must_not.extend(must_not_query)

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_card_count(self, must, must_not):
        """
        method to generate elastic query for 
        """

        aggs = {
            "card_count": {
                "value_count": {
                    "field": "metadata.cardNumbers.cardNumber.keyword"
                }
            }
        }

        must_query = [{
            "prefix": {
                "metadata.cardNumbers.cardNumber": {
                    "value": must
                }
            }
        }]

        must_not_query = [{
            "prefix": {
                "metadata.cardNumbers.cardNumber": {
                    "value": code
                }
            }
        } for code in must_not]

        self.body_must.extend(must_query)
        self.body_must_not.extend(must_not_query)

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_card_count_timeseries(self, must, must_not, interval):
        """
        method to generate elastic query for 
        """

        aggs = {
            "card_count": {
                "aggs": {
                    "card_count": {
                        "value_count": {
                            "field": "metadata.cardNumbers.cardNumber.keyword"
                        }
                    }
                },
                "date_histogram": {
                    "field": "publish_date",
                    "interval": interval
                }
            }
        }

        must_query = [{
            "prefix": {
                "metadata.cardNumbers.cardNumber": {
                    "value": must
                }
            }
        }]

        must_not_query = [{
            "prefix": {
                "metadata.cardNumbers.cardNumber": {
                    "value": code
                }
            }
        } for code in must_not]

        self.body_must.extend(must_query)
        self.body_must_not.extend(must_not_query)

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_top_card(self):
        """
        method to generate elastic query for 
        """

        aggs = {
            "top_card": {
                "terms": {
                    "field": "metadata.cardNumbers.cardNumber.keyword",
                    "size": 20
                }
            }
        }

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_top_phone(self):
        """
        method to generate elastic query for 
        """

        aggs = {
            "top_phone": {
                "terms": {
                    "field": "metadata.numbers.number.keyword",
                    "size": 20
                }
            }
        }

        should_query = [
            {
                "prefix": {
                    "metadata.numbers.number": {
                        "value": "09"
                    }
                }
            },
            {
                "prefix": {
                    "metadata.numbers.number": {
                        "value": "+989"
                    }
                }
            }
        ]

        self.body_should.extend(should_query)

        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_phone_card_platform(self):
        """
        count phone and cards on platforms
        """
        aggs = {
            "platforms": {
                "terms": {
                    "field": "platform.keyword"
                },
                "aggs": {
                    "card": {
                        "value_count": {
                            "field": "metadata.cardNumbers.cardNumber.keyword"
                        }
                    },
                    "phone": {
                        "value_count": {
                            "field": "metadata.numbers.number.keyword"
                        }
                    }
                }
            }
        }
        self.body_aggs.update(aggs)
        self.body["size"] = 0
        return self.body

    def get_topics_histogram(self, timestamps):
        interval_clause = self.get_interval_clause(timestamps)
        topics = {
            "ITkhabar", "adabi", "amniati", "amozeshi", "eghtesadi", "ejtemaee", "farhangi", "elmi",
            "filmocinema", "fun", "havades", "honari", "mazhabi", "mokhadderoalkol", "mostahjan",
            "music", "nezami", "pezeshki", "romanodastan", "siasi", "tabiatvahava", "tablighofrosh",
            "tarikhi", "varzeshi"
        }
        sub_aggs = dict()
        for topic in topics:
            sub_aggs.update({
                topic: {
                    "value_count": {
                        "field": f"topic_analysis.{topic}"
                    }
                }
            })
        aggs = {
            "all_data_model": {
                "aggs": sub_aggs,
                "date_histogram": {
                    "extended_bounds": {
                        "max": timestamps[1] * 1000,
                        "min": timestamps[0] * 1000
                    },
                    "field": "publish_date",
                    "interval": interval_clause
                }
            }
        }
        self.body_aggs.update(aggs)

    def get_ner_sentiment(self):
        aggs = {
            "aggs": {
                "ner_model": {
                    "aggs": {
                        "sentiment_count": {
                            "terms": {
                                "field": "sentiment_analysis.state"
                            }
                        }
                    },
                    "terms": {
                        "field": "ner.location.keyword",
                        "size": 10
                    }
                }
            }
        }
        self.body_aggs.update(aggs["aggs"])

    def time_series_platforms(self, timestamps):
        interval_clause = self.get_interval_clause(timestamps)
        aggs = {
            "aggs": {
                "all_data_model": {
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause
                    },
                    "aggs": {
                        "platforms": {
                            "terms": {
                                "field": "platform.keyword"
                            }
                        }
                    }
                }
            }
        }
        self.body_aggs.update(aggs["aggs"])

    def get_link_info_political_orientation(self, timestamps, metric):
        interval_clause = self.get_interval_clause(timestamps)
        sub_aggs = {
            "political_orient": {
                "terms": {
                    "field": "link_info.politicalOrientation.keyword"
                },
                "aggs": {
                    "sentiment_count": {
                        "terms": {
                            "field": "sentiment_analysis.state",
                            "size": 10
                        }
                    }
                }
            }
        }
        aggs = {
            "aggs": {
                "all_data_model": {
                    "aggs": sub_aggs,
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause
                    }
                }
            },
        }
        self.body_aggs.update(aggs["aggs"])

    def get_link_info_location(self, timestamps, metric):
        interval_clause = self.get_interval_clause(timestamps)
        sub_aggs = {
            "location": {
                "terms": {
                    "field": "link_info.location.keyword"
                },
                "aggs": {
                    "sentiment_count": {
                        "terms": {
                            "field": "sentiment_analysis.state",
                            "size": 10
                        }
                    }
                }
            }
        }
        aggs = {
            "aggs": {
                "all_data_model": {
                    "aggs": sub_aggs,
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause
                    }
                }
            },
        }
        self.body_aggs.update(aggs["aggs"])

    def get_link_info_activity(self, timestamps, metric):
        interval_clause = self.get_interval_clause(timestamps)
        sub_aggs = {
            "activity": {
                "terms": {
                    "field": "link_info.activity.keyword"
                },
                "aggs": {
                    "sentiment_count": {
                        "terms": {
                            "field": "sentiment_analysis.state",
                            "size": 10
                        }
                    }
                }
            }
        }
        aggs = {
            "aggs": {
                "all_data_model": {
                    "aggs": sub_aggs,
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause
                    }
                }
            },
        }
        self.body_aggs.update(aggs["aggs"])

    def get_link_info_impact(self, timestamps, metric):
        interval_clause = self.get_interval_clause(timestamps)
        sub_aggs = {
            "impactRate": {
                "terms": {
                    "field": "link_info.impactRate.keyword"
                },
                "aggs": {
                    "sentiment_count": {
                        "terms": {
                            "field": "sentiment_analysis.state",
                            "size": 10
                        }
                    }
                }
            }
        }
        aggs = {
            "aggs": {
                "all_data_model": {
                    "aggs": sub_aggs,
                    "date_histogram": {
                        "extended_bounds": {
                            "max": timestamps[1] * 1000,
                            "min": timestamps[0] * 1000
                        },
                        "field": "publish_date",
                        "interval": interval_clause
                    }
                }
            },
        }
        self.body_aggs.update(aggs["aggs"])

    def get_sense(self):

        self.body["size"] = 0
        self.body_aggs.update(
            {
                "all_data_model": {
                    "terms": {
                        "field": "sentiment_analysis.state"
                    }
                }
            }
        )

        return self.body

    def get_recived_data(self):
        filters_aggs = self.get_filters_aggs()
        # aggs = {
        #     "recived_data": {
        #         "date_histogram":
        #         {
        #             "field": "publish_date",
        #             "fixed_interval": interval_clause,
        #             "format": "yyyy-MM-dd-hh-mm-ss",
        #             "extended_bounds": {
        #                 "min": self.timestamps[0] * 1000,
        #                 "max": self.timestamps[1] * 1000
        #             },
        #             "missing": 0
        #         }
        #     }
        # }
        aggs = {
            "recived_data": {
                "filters":
                {
                    "filters": filters_aggs
                }
            }
        }
        self.body_aggs.update(aggs)

    def get_filters_aggs(self):
        week = {'Saturday': 1,
                'Sunday': 2,
                'Monday': 3,
                'Tuesday': 4,
                'Wednesday': 5,
                'Thursday': 6,
                'Friday': 7}
        interval_clause = self.get_interval_clause(self.timestamps)
        interval_clause = int(interval_clause.replace("s", ""))
        current_date = int(self.timestamps[0])
        date_dict = dict()
        if self.query.get("timeseries_setting", {}).get("isActive", False):
            if self.query.get("timeseries_setting", {}).get("data", {}).get("type", "bar_count") == "gap_time":
                value = self.query.get(
                    "timeseries_setting", {}).get("data", {}).get("value", 1)
                value.strip()
                value.replace(" ", "")
                type = value[-1]
                value = int(value[:-1])
                exception_interval = 0
                if value == 1 or True:
                    next_date_temp = int(self.timestamps[0] + interval_clause)
                    if type == "d":
                        exception_interval = int(datetime.timestamp(datetime.fromtimestamp(
                            next_date_temp).replace(hour=00, minute=00, second=00)))
                    if type == "w":
                        weekday = calendar.day_name[datetime.fromtimestamp(
                            current_date).weekday()]
                        date_temp = datetime.fromtimestamp(
                            current_date) + timedelta(days=(8-week.get(weekday, 1)))
                        exception_interval = int(datetime.timestamp(
                            date_temp.replace(hour=00, minute=00, second=00)))
                    if type == "M":
                        date_temp = datetime.fromtimestamp(current_date)
                        jdate = jdatetime.date.fromgregorian(date=date_temp)
                        if jdate.month <= 6:
                            date_temp = jdate + timedelta(days=(32-jdate.day))
                        elif 6 < jdate.month < 12:
                            date_temp = jdate + timedelta(days=(31-jdate.day))
                        else:
                            if calendar.isleap(datetime.fromtimestamp(current_date).year-1):
                                date_temp = jdate + \
                                    timedelta(days=(31-jdate.day))
                            else:
                                date_temp = jdate + \
                                    timedelta(days=(30-jdate.day))
                        date_temp = date_temp.togregorian()
                        date_temp = datetime(
                            date_temp.year, date_temp.month, date_temp.day)
                        exception_interval = int(datetime.timestamp(
                            date_temp.replace(hour=00, minute=00, second=00)))
            while (current_date + interval_clause) < self.timestamps[1]:
                if exception_interval:
                    next_date = exception_interval
                    exception_interval = 0
                else:
                    if type == "M" and value == 1:
                        date_temp = datetime.fromtimestamp(current_date)
                        jdate = jdatetime.date.fromgregorian(date=date_temp)
                        if jdate.month <= 6:
                            next_date = current_date + \
                                (31 * 24 * 60 * 60)
                        elif 6 < jdate.month < 12:
                            next_date = current_date + (30 * 24 * 60 * 60)
                        else:
                            if calendar.isleap(datetime.fromtimestamp(current_date).year-1):
                                next_date = current_date + \
                                    (30 * 24 * 60 * 60)
                            else:
                                next_date = current_date + \
                                    (29 * 24 * 60 * 60)
                    else:
                        next_date = current_date + interval_clause
                agg = {
                    next_date: {
                        "range": {
                            "timestamp": {
                                "gte": current_date,
                                "lt": next_date
                            }
                        }
                    }
                }
                current_date = int(next_date)
                date_dict.update(dict(agg))
            date_dict.update({
                int(self.timestamps[1]): {
                    "range": {
                        "timestamp": {
                            "gte": current_date,
                            "lte": int(self.timestamps[1])
                        }
                    }
                }
            })
            return date_dict

    def query_builder(self):
        self._pagination_setter()
        self._sort_setter()
        self._extra_sort_setter()
        self._topic_analysis_setter()
        self._behavioral_analysis_setter()
        self._sentiment_analysis_setter()
        self._keywords_setter()
        self._ner_setter()
        self._has_image()
        self._timestamps_setter()
        self._user_info()
        self._keyword_category()
        self._link_category()
        notify = self._links_setter()
        self.get_recived_data()
        if len(self.body_should) > 0:
            self.body_query_bool["minimum_should_match"] = 1

        return {"notify": notify}

    def get_body(self):
        body = remove_empty_elements(copy.deepcopy(self.body))
        return body

    def get_timestamps(self):
        return self.timestamps

    def get_seconds(self, value: str) -> str:
        try:
            value.strip()
            value.replace(" ", "")
            type = value[-1]
            value = int(value[:-1])
            if type == "s":
                return str(value)+"s"
            elif type == "m":
                return str(value * 60)+"s"
            elif type == "h":
                return str(value * 3600)+"s"
            elif type == "d":
                return str(value * 86400)+"s"
            elif type == "w":
                return str(value * 604800)+"s"
            elif type == "M":
                return str(value * 2678400)+"s"
        except:
            return str(86400)+"s"

    def get_interval_clause(self, timestamps):
        interval = timestamps[1] - timestamps[0]
        if self.query.get("timeseries_setting", {}).get("isActive", False):
            if self.query.get("timeseries_setting", {}).get("data", {}).get("type", "bar_count") == "gap_time":
                gap_time = self.query.get(
                    "timeseries_setting", {}).get("data", {}).get("value", 1)
                return self.get_seconds(gap_time)
            else:  # bar_count
                if self.query.get("timeseries_setting", {}).get("data", {}).get("value"):
                    self.bar_count = int(self.query.get(
                        "timeseries_setting", {}).get("data", {}).get("value")) - 1
                return str(int(int(interval)/self.bar_count))+"s"
        else:
            return str(int(int(interval)/self.bar_count))+"s"

    def get_timespan(self, timespan_type: str = "period", period_type: str = "M",
                     period_value: int = 1, start_timestamp: Union[int, None] = None,
                     end_timestamp: Union[int, None] = None):
        if timespan_type == 'period':
            timespan_dict = self.get_timespan_by_period(period_type=period_type,
                                                        period_value=period_value)
        elif timespan_type == 'date':
            timespan_dict = self.get_timespan_by_date(start_timestamp=start_timestamp,
                                                      stop_timestamp=end_timestamp)
        else:
            return "now-100m/m", "now/m", "10m"
        return timespan_dict['start'], timespan_dict['stop'], '1m' if timespan_dict['interval'] == '0m' else \
            timespan_dict['interval']

    def get_timespan_by_period(self, period_type, period_value):
        total_min = 0
        if period_type == 'w':
            total_min = period_value * 60 * 24 * 7
        elif period_type == 'd':
            if period_value > 0:
                total_min = period_value * 60 * 24
            else:
                total_min = datetime.utc().minute + datetime.utc().hour * 60
                if period_value == -1:
                    start = 1 * 24 * 60 + total_min
                    return {
                        "start": 'now-' + str(start) + 'm/m',
                        "stop": 'now-' + str(total_min) + 'm/m',
                        "interval": str(int((start - total_min) / self.bar_count)) + 'm'
                    }
        elif period_type == 'h':
            total_min = period_value * 60

        elif period_type == 'M':
            total_min = period_value * 60 * 24 * 31

        elif period_type == 'm':
            total_min = period_value
        return {
            "start": 'now-' + str(total_min) + 'm/m',
            "stop": "now/m",
            "interval": str(int(total_min / self.bar_count)) + 'm'
        }

    def get_timespan_by_date(self, start_timestamp, stop_timestamp):
        now = int(datetime.timestamp(datetime.now()))
        start_timestamp = int(
            start_timestamp / 1000) if len(str(start_timestamp)) == 13 else int(start_timestamp)
        stop_timestamp = int(
            stop_timestamp / 1000) if len(str(stop_timestamp)) == 13 else int(stop_timestamp)
        if stop_timestamp > now:
            stop_timestamp = now - 1
        start = int((start_timestamp - now) / 60)
        start = -1 * start if start != 0 and start > 0 else start
        stop = int((stop_timestamp - now) / 60)
        every = abs(int((stop - start) / self.bar_count))
        stop = stop if stop < 0 else -1
        # if stop >= 0:
        #     stop = -1
        return {
            "start": "now" + str(start) + 'm/m',
            "stop": "now" + str(stop) + 'm/m',
            "interval": str(every) + 'm'
        }
