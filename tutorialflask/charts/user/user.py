#import copy

#from flask import request, jsonify
from flask_restful import Resource

#from tools.cerberus_validator import schema_validator_cerberus
#from tools.elasticsearchQueryBuilder import ElasticSearchQueryBuilder, TOPICS, BEHAVIORALS
#from tools.inputSchema import InputSchema
#from tools.manage_elasticsearch import ManageElasticsearch
#from tools.util import error_handler, remove_none_value, extract_platforms, bank_operator, find_peaks, \
#    get_top_hashtags, jalalish, get_persian_num

# manage_es = ManageElasticsearch()
# inputSchema = InputSchema()

# user_schema = {}
# user_schema.update(inputSchema.pagination(limit=0))
# user_schema.update(inputSchema.filter())

# bank_reg = [
#     ("meli", "603799"),
#     ("sepah", "589210"),
#     ("tosee_saderat", "627648"),
#     ("sanat&madan", "627961"),
#     ("keshavarzi", "603770"),
#     ("maskan", "628023"),
#     ("post_bank", "627760"),
#     ("tosee_taavon", "502908"),
#     ("eghtesad_novin", "627412"),
#     ("parsian", "622106"),
#     ("pasargad", "502229"),
#     ("ghavamin", "639599"),
#     ("karafarin", "627488"),
#     ("saman", "621986"),
#     ("sina", "639346"),
#     ("sarmayeh", "639607"),
#     ("shahr", "504706"),
#     ("shahr", "502706"),
#     ("dey", "502938"),
#     ("saderat", "603769"),
#     ("mellat", "610433"),
#     ("tejarat", "627353"),
#     ("tejarat", "585983"),
#     ("refah", "589463"),
#     ("ansar", "627381"),
#     ("mehr_eghtesad", "639370"),
#     ("noor", "507677"),
#     ("tousee", "628157"),
#     ("kosar", "505801"),
#     ("melal", "606256"),
#     ("mehr_iranian", "606373"),
# ]

# banks = {
#     "meli": 0,
#     "sepah": 0,
#     "tosee_saderat": 0,
#     "sanat&madan": 0,
#     "keshavarzi": 0,
#     "maskan": 0,
#     "post_bank": 0,
#     "tosee_taavon": 0,
#     "eghtesad_novin": 0,
#     "parsian": 0,
#     "pasargad": 0,
#     "ghavamin": 0,
#     "karafarin": 0,
#     "saman": 0,
#     "sina": 0,
#     "sarmayeh": 0,
#     "shahr": 0,
#     "dey": 0,
#     "saderat": 0,
#     "mellat": 0,
#     "tejarat": 0,
#     "refah": 0,
#     "ansar": 0,
#     "mehr_eghtesad": 0,
#     "noor": 0,
#     "tousee": 0,
#     "kosar": 0,
#     "melal": 0,
#     "mehr_iranian": 0
# }

# farsi_banks = {
#     "meli": "ملی",
#     "sepah": "سپه",
#     "tosee_saderat": "توسعه صادرات",
#     "sanat&madan": "صنعت و معدن",
#     "keshavarzi": "کشاورزی",
#     "maskan": "مسکن",
#     "post_bank": "پست بانک",
#     "tosee_taavon": "توسعه تعاون",
#     "eghtesad_novin": "اقتصاد نوین",
#     "parsian": "پارسیان",
#     "pasargad": "پاسارگاد",
#     "ghavamin": "قوامین",
#     "karafarin": "کارآفرین",
#     "saman": "سامان",
#     "sina": "سینا",
#     "sarmayeh": "سرمایه",
#     "shahr": "شهر",
#     "dey": "دی",
#     "saderat": "صادرات",
#     "mellat": "ملت",
#     "tejarat": "تجارت",
#     "refah": "رفاه",
#     "ansar": "انصار",
#     "mehr_eghtesad": "مهر اقتصاد",
#     "noor": "نور",
#     "tousee": "توسعه",
#     "kosar": "کوثر",
#     "melal": "ملل",
#     "mehr_iranian": "مهر ایرانیان"
# }

# operators = {
#     "hamrah_aval": 0,
#     "irancel": 0,
#     "rightel": 0
# }

# farsi_operators = {
#     "hamrah_aval": "همراه اول",
#     "irancel": "ایرانسل",
#     "rightel": "رایتل"
# }

# phone_reg = {
#     "hamrah_aval": ["0990", "0991", "0992", "0993", "0994",
#                     "0910", "0911", "0912", "0913", "0914", "0915", "0916", "0917", "0918"],
#     "irancel": ["0901", "0902", "0903", "0904", "0905",
#                 "0930", "0933", "0935", "0936", "0937", "0938", "0939", "0941"],
#     "rightel": ["0920", "0921", "0922"]
# }


# class UserInfo(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.username_email_link_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'sort': aux_filter.get("sort", dict()),
#             'user': aux_filter.get("user", dict())
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             user = valid_args.get('user', dict())
#             body = elastic_builder.get_username_email_link(user)
#             data = dict()
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict())
#             data = self.clean_data(data)
#             return jsonify(data)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data):
#         """
#         prepare data to return
#         """
#         output = {
#             "link_count": list(),
#             "username_count": list(),
#             "email_count": list()
#         }
#         for k, v in output.items():
#             output[k] = [{
#                 "value": item.get('key', None),
#                 "platform": item.get('platform_count', dict()).get('buckets', list())[0].get("key", None),
#                 "count": item.get('platform_count', dict()).get('buckets', list())[0].get("doc_count", 0)
#             } for item in data.get(k, dict()).get("buckets", list())]
#         output["platform_count"] = [{"key": item.get("key", None), "doc_count": item.get(
#             "doc_count", 0)} for item in data.get("platform_count", dict()).get("buckets", list())]
#         total = 0
#         for platform in output["platform_count"]:
#             total += platform["doc_count"]
#         output["platform_count"].append({"key": "total", "doc_count": total})
#         total_platforms = ["instagram",
#                            "telegram",
#                            "facebook",
#                            "twitter",
#                            "rss",
#                            "newspaper"]
#         response_platforms = [item.get("key", None)
#                               for item in output["platform_count"]]
#         for platform in total_platforms:
#             if platform not in response_platforms:
#                 output["platform_count"].append(
#                     {"key": platform, "doc_count": 0})
#         output["text"] = f""
#         return output


# class UserInfoTimeseries(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.timeseries_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'timeseries': aux_filter.get("timeseries", dict()),
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             timeseries = valid_args.get('timeseries', dict())
#             body = elastic_builder.get_username_email_link_timeseries(
#                 timeseries)
#             data = {"aggregations": {"username_link_email": dict()}}
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict()).get("username_link_email", dict())
#             data = self.clean_data(data, my_index)
#             return jsonify(data)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data, my_index):
#         """
#         prepare data to return
#         """
#         lst = list()
#         for item in data.get("buckets", list()):
#             for type in ["email", "link", "username"]:
#                 lst.append({
#                     "type": type,
#                     "publish_date": item.get("key_as_string", None),
#                     "timestamp": item.get("key", None),
#                     "count": item.get(type, dict()).get("value", 0)
#                 })
#         context = str()
#         if lst:
#             email_lst = [item for item in lst if item["type"] == "email"]
#             link_lst = [item for item in lst if item["type"] == "link"]
#             username_lst = [item for item in lst if item["type"] == "username"]
#             email_peaks = find_peaks(email_lst, "count")
#             link_peaks = find_peaks(link_lst, "count")
#             username_peaks = find_peaks(username_lst, "count")
#             for k, v in {"ایمیل": email_peaks, "لینک": link_peaks, "نام کاربری": username_peaks}.items():
#                 if len(v) >= 3:
#                     first_tophashtags = ", ".join(get_top_hashtags(my_index, v[0]['publish_date']))
#                     second_tophashtags = ", ".join(get_top_hashtags(my_index, v[1]['publish_date']))
#                     third_tophashtags = ", ".join(get_top_hashtags(my_index, v[2]['publish_date']))
#                     v = jalalish(v)
#                     context += f"بیشترین محتوای منتشر شده دارای {k} در تاریخ {v[0]['publish_date']} با {v[0]['value']} داده کل و پرتکرارترین هشتگ های {first_tophashtags} و تاریخ {v[1]['publish_date']} با {v[1]['value']} داده کل و پرتکرارترین هشتگ های {second_tophashtags} و تاریخ {v[2]['publish_date']} با {v[2]['value']} داده کل و پرتکرار ترین هشتگ های {third_tophashtags} بوده است."
#         output = {
#             "data": lst,
#             "text": get_persian_num(context)
#         }
#         return output


# class PhoneCardTimeseries(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on time
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.timeseries_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'timeseries': aux_filter.get("timeseries", dict()),
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             timeseries = valid_args.get('timeseries', dict())
#             body = elastic_builder.get_phone_card_timeseries(timeseries)
#             data = list()
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict()).get("phone_card", dict()).get("buckets", list())
#             data = self.clean_data(data)
#             return jsonify(data)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def platform(self, type: str, buckets: list) -> dict():
#         """
#         distibute count for platforms
#         """
#         output = {
#             "instagram": 0,
#             "telegram": 0,
#             "twitter": 0,
#             "facebook": 0,
#             "rss": 0,
#             "newspaper": 0,
#         }
#         for obj in buckets:
#             output[obj["key"]] = obj[type]["value"]
#         output = [{"key": k, "count": v if isinstance(
#             v, int) and v > 0 else 0} for k, v in output.items()]

#         return output

#     def total_count(self, _type: str, buckets: list):
#         """
#         count bucket type
#         """
#         c = 0
#         for obj in buckets:
#             c += obj.get(_type, dict()).get("value", 0)
#         return c

#     def clean_data(self, data):
#         """
#         prepare data to return
#         """
#         lst = list()
#         for item in data:
#             for type in ["phone", "card"]:
#                 buckets = item.get("platforms", dict()).get("buckets", list())
#                 lst.append({
#                     "type": type,
#                     "platform": self.platform(type, buckets),
#                     "publish_date": item.get("key_as_string", None),
#                     "timestamp": item.get("key", None),
#                     "count": self.total_count(type, buckets)
#                 })
#         output = {"data": lst,
#                   "text": f"لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد."}
#         return output


# class PhoneCount(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of phones
#         """
#         # This variable will hold json object that taken from input(user)
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             data = {
#                 "hamrah_aval": 0,
#                 "irancel": 0,
#                 "rightel": 0
#             }
#             for k, v in phone_reg.items():
#                 keys = list(data.keys())
#                 keys.remove(k)
#                 # Build Query and Aggs ElasticSearch
#                 elastic_builder = ElasticSearchQueryBuilder(valid_args)
#                 elastic_builder.query_builder()
#                 timestamps = elastic_builder.get_timestamps()
#                 my_index = manage_es.get_index(timestamps, platforms)
#                 body = elastic_builder.get_phone_count(
#                     phone_reg[k], phone_reg[keys[0]] + phone_reg[keys[1]])
#                 if my_index:
#                     data[k] = manage_es.search(
#                         my_index, body).get("aggregations", dict()).get("phone_count", dict()).get("value", 0)
#             lst = [{"key": k, "count": v if isinstance(
#                 v, int) and v > 0 else 0} for k, v in data.items()]
#             if lst:
#                 lst = sorted(lst, key=lambda x: x["count"], reverse=True)
#                 output = {
#                     "data": lst,
#                     "text": get_persian_num(
#                         f"با توجه به نمودار تعداد شماره تلفن دریافتی از اپراتور {farsi_operators[lst[0]['key']]} برابر با {lst[0]['count']} و اپراتور {farsi_operators[lst[1]['key']]} برابر با {lst[1]['count']} و اپراتور {farsi_operators[lst[2]['key']]} برابر با {lst[2]['count']} است.")
#                 }
#             else:
#                 output = {
#                     "data": lst,
#                     "text": str()
#                 }

#             return jsonify(output)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400


# class PhoneCountTimeseries(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of phones
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.timeseries_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'timeseries': aux_filter.get("timeseries", dict()),
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             for k, v in phone_reg.items():
#                 keys = list(operators.keys())
#                 keys.remove(k)
#                 # Build Query and Aggs ElasticSearch
#                 elastic_builder = ElasticSearchQueryBuilder(valid_args)
#                 elastic_builder.query_builder()
#                 timestamps = elastic_builder.get_timestamps()
#                 my_index = manage_es.get_index(timestamps, platforms)
#                 interval = valid_args.get(
#                     'timeseries', dict()).get("interval", "month")
#                 body = elastic_builder.get_phone_count_timeseries(
#                     phone_reg[k], phone_reg[keys[0]] + phone_reg[keys[1]], interval)
#                 if my_index:
#                     operators[k] = manage_es.search(
#                         my_index, body).get("aggregations", dict()).get("phone_count", dict()).get("buckets", list())
#             data = bank_operator(operators, "phone_count")
#             output = {"data": data,
#                       "text": f"لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد."}
#             return jsonify(output)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400


# class CardCount(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of cards
#         """
#         # This variable will hold json object that taken from input(user)
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             for i, item in enumerate(bank_reg):
#                 # Build Query and Aggs ElasticSearch
#                 elastic_builder = ElasticSearchQueryBuilder(valid_args)
#                 elastic_builder.query_builder()
#                 timestamps = elastic_builder.get_timestamps()
#                 my_index = manage_es.get_index(timestamps, platforms)
#                 body = elastic_builder.get_card_count(
#                     item[1], [bank[1] for bank in bank_reg[i + 1:] + bank_reg[:i]])
#                 if my_index:
#                     banks[item[0]] = manage_es.search(
#                         my_index, body).get("aggregations", dict()).get("card_count", dict()).get("value", 0)

#             lst = [{"key": k, "count": v if isinstance(
#                 v, int) and v > 0 else 0} for k, v in banks.items()]
#             if lst:
#                 lst = sorted(lst, key=lambda x: x["count"], reverse=True)
#                 output = {
#                     "data": lst,
#                     "text": get_persian_num(
#                         f"با توجه به نمودار تعداد شماره کارت دریافتی از بانک {farsi_banks[lst[0]['key']]} برابر با {lst[0]['count']} و بانک {farsi_banks[lst[1]['key']]} برابر با {lst[1]['count']} و بانک {farsi_banks[lst[2]['key']]} برابر با {lst[2]['count']} است که بیشترین تعداد دریافت را داشته اند.")
#                 }
#             else:
#                 output = {
#                     "data": lst,
#                     "text": str()
#                 }
#             return jsonify(output)

#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400


# class CardCountTimeseries(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of cards
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.timeseries_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'timeseries': aux_filter.get("timeseries", dict()),
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             for i, item in enumerate(bank_reg):
#                 # Build Query and Aggs ElasticSearch
#                 elastic_builder = ElasticSearchQueryBuilder(valid_args)
#                 elastic_builder.query_builder()
#                 timestamps = elastic_builder.get_timestamps()
#                 my_index = manage_es.get_index(timestamps, platforms)
#                 interval = valid_args.get(
#                     'timeseries', dict()).get("interval", "month")
#                 body = elastic_builder.get_card_count_timeseries(
#                     item[1], [bank[1] for bank in bank_reg[i + 1:] + bank_reg[:i]], interval)
#                 if my_index:
#                     banks[item[0]] = manage_es.search(
#                         my_index, body).get("aggregations", dict()).get("card_count", dict()).get("buckets", list())
#                 if not isinstance(banks[item[0]], list):
#                     banks[item[0]] = list()
#             data = bank_operator(banks, "card_count")
#             output = {"data": data,
#                       "text": f"لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد."}
#             return jsonify(output)
#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400


# class TopCard(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         """
#         # This variable will hold json object that taken from input(user)
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             body = elastic_builder.get_top_card()
#             data = list()
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict()).get("top_card", dict()).get("buckets", list())
#             data = self.clean_data(data)
#             return jsonify(data)

#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data):
#         """
#         prepare data to return
#         """
#         lst = list()
#         for item in data:
#             lst.append({"key": item.get("key", None),
#                         "count": item.get("doc_count", 0)})

#         if lst:
#             output = {
#                 "data": lst,
#                 "text": get_persian_num(
#                     f"با توجه به نمودار بیشترین شماره کارت های تکرار شده به ترتیب {lst[0]['key']} با {lst[0]['count']} مرتبه تکرار و {lst[1]['key']} با {lst[1]['count']} مرتبه تکرار و {lst[2]['key']} با {lst[2]['count']} مرتبه تکرار بوده اند.")
#             }

#         else:
#             output = {
#                 "data": lst,
#                 "text": str()
#             }

#         return output


# class TopPhone(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         """
#         # This variable will hold json object that taken from input(user)
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             body = elastic_builder.get_top_phone()
#             data = list()
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict()).get("top_phone", dict()).get("buckets", list())
#             data = self.clean_data(data)
#             return jsonify(data)

#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data):
#         """
#         prepare data to return
#         """
#         lst = list()
#         for item in data:
#             phone = item.get("key", None)
#             count = item.get("doc_count", 0)
#             if phone[:2] == "09" or phone[:4] == "+989":
#                 lst.append({"key": phone,
#                             "count": count})

#         if lst:
#             output = {
#                 "data": lst,
#                 "text": get_persian_num(
#                     f"با توجه به نمودار بیشترین شماره کارت های تکرار شده به ترتیب {lst[0]['key']} با {lst[0]['count']} مرتبه تکرار و {lst[1]['key']} با {lst[1]['count']} مرتبه تکرار و {lst[2]['key']} با {lst[2]['count']} مرتبه تکرار بوده اند.")

#             }
#         else:
#             output = {
#                 "data": lst,
#                 "text": str()

#             }
#         return output


# class UserName(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         alirezamahmoodi desire api
#         """
#         # This variable will hold json object that taken from input(user)
#         user_schema.update(inputSchema.username_schema())
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         aux_filter = raw_args.get("aux_filter", dict())
#         total.update({
#             'user': aux_filter.get("user", dict())
#         })
#         total.update(aux_filter)
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             user = valid_args.get('user', dict())
#             body = elastic_builder.get_username(user)
#             data = dict()
#             if my_index:
#                 data: dict = manage_es.search(
#                     my_index, body).get("aggregations", dict())
#             data = self.clean_data(data)
#             return jsonify(data)

#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data: dict):
#         """
#         prepare data to return
#         """
#         topics = list()
#         behaviors = list()
#         for k, v in data.items():
#             if k in TOPICS:
#                 topics.append({
#                     "topic": k,
#                     "count": v.get("value", 0)
#                 })
#             elif k in BEHAVIORALS:
#                 behaviors.append({
#                     "behavior": k,
#                     "count": v.get("value", 0)
#                 })
#         sens = data.get("sens", dict()).get("buckets", list())
#         sentiments = [
#             {
#                 "sense": "positive" if item.get("key") == 1
#                 else "negative" if item.get("key") == 0
#                 else "neutral",
#                 "count": item.get("doc_count")
#             } for item in sens
#         ]

#         output = {
#             "sentiment": sentiments,
#             "topic": sorted(topics, key=lambda x: x["count"], reverse=True)[:3],
#             "behavior": sorted(behaviors, key=lambda x: x["count"], reverse=True)[:3]
#         }

#         if not sentiments:
#             output = {
#                 "sentiment": list(),
#                 "topic": list(),
#                 "behavior": list()
#             }

#         return output


# class CardPhonePlatform(Resource):
#     @error_handler
#     def post(self):
#         """
#         post method to recieve count of username, email, link based on platform
#         """
#         # This variable will hold json object that taken from input(user)
#         raw_args = request.get_json()
#         total = {}
#         main_filter = raw_args.get("main_filter", dict())
#         total.update(main_filter)
#         # using deepcopy to deep copy
#         no_none_args = copy.deepcopy(total)
#         # Remove none Value from args
#         remove_none_value(no_none_args)
#         # validation arguments by cerberus lib.
#         res = schema_validator_cerberus(no_none_args, user_schema)
#         valid_args = res["final_document"]
#         if not res["errors"]:
#             platforms = extract_platforms(valid_args)
#             # Build Query and Aggs ElasticSearch
#             elastic_builder = ElasticSearchQueryBuilder(valid_args)
#             elastic_builder.query_builder()
#             timestamps = elastic_builder.get_timestamps()
#             my_index = manage_es.get_index(timestamps, platforms)
#             body = elastic_builder.get_phone_card_platform()
#             data = list()
#             if my_index:
#                 data = manage_es.search(
#                     my_index, body).get("aggregations", dict()).get("platforms", dict()).get("buckets", list())
#             data = self.clean_data(data)
#             return jsonify(data)

#         else:
#             return {
#                 "Error": {
#                     "statusCode": 400,
#                     "message": "Validation errors",
#                     "validation_msg": res["errors"]
#                 }
#             }, 400

#     def clean_data(self, data: list):
#         """
#         prepare data to return
#         """
#         platforms = ["instagram", "telegram", "twitter",
#                      "facebook", "rss", "newspaper"]
#         lst = [{"key": item.get("key", None),
#                 "value": item.get("phone", dict()).get("value", 0) +
#                          item.get("card", dict()).get("value", 0)} for item in data]
#         output_platforms = [item.get("key", None) for item in lst]
#         for item in platforms:
#             if item not in output_platforms:
#                 lst.append({
#                     "key": item,
#                     "value": 0
#                 })
#         output = {"data": lst, "text": f""}
#         return output


class RegisterUser(Resource):
    def post(self):
        return {
            "name":"RegisterUser"
        }
    

class UserLogin(Resource):
    def post(self):
        return {
            "name":"UserLogin"
        }
    