import urllib3
from config import configer
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch


urllib3.disable_warnings()

# Get list of month between two dates


def months_two_dates(timestamps=[]):
    days = []
    date_time = [datetime.fromtimestamp(
        timestamps[0]), datetime.fromtimestamp(timestamps[1])]

    dates = [date_time[0].strftime(
        '%Y-%m-%d'), date_time[1].strftime('%Y-%m-%d')]
    # print("dates", dates)
    sdate, edate = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]

    delta = edate - sdate
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        days.append(day)
    # list_month = OrderedDict(
    #     ((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys()
    return days


class ManageElasticsearch(object):
    def __init__(self):
        myConfig = configer.Configer()

        # Get connection parameters from config file
        es_port = myConfig.get("es", "port")
        es_user = myConfig.get("es", "user")
        es_pass = myConfig.get("es", "pass")
        es_connection = myConfig.get("es", "host")

        # ElasticSearch
        if myConfig.get('es', 'host_mode') == "company":
            self.es = Elasticsearch(es_connection, use_ssl=False, ca_certs=False, http_auth=(
                es_user, es_pass), verify_certs=False)
        elif myConfig.get('es', 'host_mode') == "infra_access":
            pass
        elif myConfig.get('es', 'host_mode') == "ip":
            self.es = Elasticsearch([{'host': myConfig.get("es", "host_ip"), 'port': int(es_port)}],
                                    http_auth=(es_user,
                                               es_pass))

        # self.es = Elasticsearch(es_connection, use_ssl=False, ca_certs=False, http_auth=(
        #         es_user, es_pass), verify_certs=False)

        self.request_timeout = int(myConfig.get("es", "request_timeout"))
        self.current_index = None

    def search(self, index, body, size=None, from_=None, sort=None, filter_path=None):
        valid_indexes = self.remove_not_found_index(index)

        result = self.es.search(index=valid_indexes, body=body, size=size, from_=from_, request_timeout=self.request_timeout, ignore=[400, 404, 500, 503], max_concurrent_shard_requests=5, sort=sort, filter_path=filter_path, ignore_unavailable=True)
        return result

    def count(self, index, body):
        count_hits = self.es.count(index=index, body=body, ignore=[400, 404, 500])
        if "count" in count_hits:
            return count_hits["count"]

    def get_index(self, timestamp, media_type):
        # print("timestamps", timestamp)
        # Define as a set to delete duplicate indexes
        current_index = set()

        dates = []

        if isinstance(timestamp, list):

            # this variable have this format 2020-10
            list_month = months_two_dates(timestamp)

            for date_obj in list_month:
                # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                dates.append({
                    "date_time": date_obj,
                    "year": date_obj.year,
                    # "month": '{:02}'.format(date_obj.month),
                    "month": date_obj.month,
                    "day": date_obj.day
                })
        else:
            date_obj = datetime.fromtimestamp(timestamp)
            dates.append({
                "date_time": date_obj,
                "year": date_obj.year,
                # "month": '{:02}'.format(date_obj.month),
                "month": date_obj.month,
                "day": date_obj.day
            })

        for date in dates:
            for media in media_type:

                # NEWSPAPER
                if media == "newspaper":
                    current_index.add("newspaper-{}-{}".format(date["year"], date["month"]))

                # TWITTER
                elif media == "twitter":
                    if 1 <= date["day"] <= 10:
                        current_index.add("twitter-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("twitter-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("twitter-{}-{}-21_31".format(date["year"], date["month"]))

                # TELEGRAM
                elif media == "telegram":
                    if 1 <= date["day"] <= 10:
                        current_index.add("telegram-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("telegram-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("telegram-{}-{}-21_31".format(date["year"], date["month"]))

                # INSTAGRAM
                elif media == "instagram":
                    if 1 <= date["day"] <= 10:
                        current_index.add("instagram-{}-{}-1_10".format(date["year"], date["month"]))
                        # current_index.add(
                        # "instagram-comments-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("instagram-{}-{}-11_20".format(date["year"], date["month"]))
                        # current_index.add(
                        #     "instagram-comments-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("instagram-{}-{}-21_31".format(date["year"], date["month"]))
                        # current_index.add(
                        #     "instagram-comments-{}-{}-21_31".format(date["year"], date["month"]))

                # INSTAGRAM_COMMENTS
                elif media == "instagram_comment":
                    if 1 <= date["day"] <= 10:
                        current_index.add("instagram_comment-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("instagram_comment-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("instagram_comment-{}-{}-21_31".format(date["year"], date["month"]))

                # INSTAGRAM_COMMENTS
                elif media == "instagram_story":
                    if 1 <= date["day"] <= 10:
                        current_index.add("instagram_story-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("instagram_story-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("instagram_story-{}-{}-21_31".format(date["year"], date["month"]))

                # EITTA
                elif media == "eitaa":
                    if 1 <= date["day"] <= 10:
                        current_index.add("sa-eitaa-{}-{}-1_10".format(date["year"], date["month"]))

                    elif 11 <= date["day"] <= 20:
                        current_index.add("sa-eitaa-{}-{}-11_20".format(date["year"], date["month"]))

                    elif 21 <= date["day"] <= 31:
                        current_index.add("sa-eitaa-{}-{}-21_31".format(date["year"], date["month"]))

                # RSS
                elif media == "rss":
                    current_index.add("rss-{}-{}".format(date["year"], date["month"]))

                elif media == "web":
                    current_index.add("web-{}-{}".format(date["year"], date["month"]))

        generated_indexes = list(current_index)
        # print("Generated indexes", generated_indexes)
        self.current_index = self.remove_not_found_index(generated_indexes)
        # print("valid_indexes", self.current_index)

        return self.current_index

    def count_hints(self, indexes, query):
        try:
            if "filter" in list(query):
                del query["bool"]["filter"]
            # Structure count
            counts = {"indexes": [], "all": 0}
            c = 0
            # print("MY Print", query)
            for index in indexes:
                res = self.es.count(index=index, body={
                                    "query": query}, ignore=[400, 404, 500])
                # print("res =>", res)
                # print("curr_Index =>", index)
                if "error" not in res:
                    counts["indexes"].append({
                        "index": index,
                        "_shards": res["_shards"],
                        "count": res["count"]
                    })
                    c += res["count"]
            counts["all"] = c
            return counts
        except Exception as e:
            print("error", e)

    def remove_not_found_index(self, indexes):
        valid_indexes = []
        for index in indexes:
            try:
                if self.es.indices.exists(index):
                    valid_indexes.append(index)
            except:
                pass
        return valid_indexes
