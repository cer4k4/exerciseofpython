from cerberus import Validator


def schema_validator_cerberus(document, schema):
    result = {"final_document": {}, "errors": {}}
    v = Validator(schema)
    
    # VALIDATE
    if v.validate(document):

        # NORMALIZED
        norm_doc = v.normalized(document)
        result["final_document"] = norm_doc
        # print("final_inputSchema =>", norm_doc)
    else:
        result["errors"] = v.errors

    return result


# def category_farsish(value):

#     # NER
#     if value == "person":
#         value = "اشخاص"
#     if value == "event":
#         value = "رویداد ها"
#     if value == "dateTime":
#         value = "تاریخ و زمان"
#     if value == "location":
#         value = "موقعیت های مکانی"
#     if value == "organization":
#         value = "سازمان ها"

#     if value == "keywords":
#         value = "کلمات مهم"

#     # METADATA
#     if value == "hashtags_one":
#         value = "هشتگ ها"
#     if value == "hashtags_multi":
#         value = "هشتگ خصوصی"
#     if value == "numbers":
#         value = "شماره تلفن"
#     if value == "emails":
#         value = "ایمیل"
#     if value == "cardNumbers":
#         value = "شماره کارت"
#     if value == 'emoji':
#         value = "ایموجی"
#     if value == "main_user":
#         value = "نام کاربری"
#     if value == "mentioned_user":
#         value = "نام کاربری شناسایی شده در متن"

#     # LINK
#     if value == "link":
#         value = "لینک"
#     if value == "main_link":
#         value = "لینک اصلی"
#     if value == "mentioned_link":
#         value = "لینک منشن"

#     # SENTIMENT ANALYZER
#     if value == "positive":
#         value = "مثبت"
#     if value == "negative":
#         value = "منفی"
#     if value == "neutral":
#         value = "خنثی"

#     # GEO
#     if value == "country":
#         value = "کشور"
#     if value == "city":
#         value = "شهر"
#     if value == "province":
#         value = "استان"
#     if value == "place":
#         value = "منطقه"

#     return value


# def generate_path_field_in_es(value):

#     # NER
#     if value == "person":
#         value = "ners_info.person.keyword"
#     if value == "event":
#         value = "ners_info.event.keyword"
#     if value == "dateTime":
#         value = "ners_info.dateTime.keyword"
#     if value == "location":
#         value = "ners_info.location.keyword"
#     if value == "organization":
#         value = "ners_info.organization.keyword"

#     if value == "keywords":
#         value = "keywords.keyword"

#     # METADATA
#     if value == "hashtags_one":
#         value = "metadata.hashtags_one.hashtag.keyword"
#     if value == "hashtags_multi":
#         value = "metadata.hashtags_multi.hashtag.keyword"
#     if value == "numbers":
#         value = "metadata.numbers.number.keyword"
#     if value == "emails":
#         value = "metadata.emails.email.keyword"
#     if value == "cardNumbers":
#         value = "metadata.cardNumbers.cardNumber.keyword"
#     if value == 'emoji':
#         value = "metadata.emoji.emoji.keyword"
#     if value == "main_user":
#         value = "user.username.keyword"
#     if value == "mentioned_user":
#         value = "metadata.usernames.username.keyword"

#     # LINK
#     if value == "link":
#         value = "user.url.keyword"
#     if value == "main_link":
#         value = "link.keyword"
#     if value == "mentioned_link":
#         value = "metadata.urls.url.keyword"

#     # SENTIMENT ANALYZER
#     if value == "positive":
#         value = "sentiment_analysis.probabilities.positive"
#     if value == "negative":
#         value = "sentiment_analysis.probabilities.negative"
#     if value == "neutral":
#         value = "sentiment_analysis.probabilities.neutral"

#     # GEO
#     if value == "country":
#         value = "location_finder.country.keyword"
#     if value == "city":
#         value = "location_finder.city.keyword"
#     if value == "province":
#         value = "location_finder.province.keyword"
#     if value == "place":
#         value = "location_finder.place.keyword"

#     return value


# def reverse_generate_path_field_in_es(value):
#     # NER
#     if value == "ners_info.person.keyword":
#         value = "person"
#     if value == "ners_info.event.keyword":
#         value = "event"
#     if value == "ners_info.dateTime.keyword":
#         value = "dateTime"
#     if value == "ners_info.location.keyword":
#         value = "location"
#     if value == "ners_info.organization.keyword":
#         value = "organization"

#     if value == "keywords.keyword":
#         value = "keywords"

#     # METADATA
#     if value == "metadata.hashtags_one.hashtag.keyword":
#         value = "hashtags_one"
#     if value == "metadata.hashtags_multi.hashtag.keyword":
#         value = "hashtags_multi"
#     if value == "metadata.numbers.number.keyword":
#         value = "numbers"
#     if value == "metadata.emails.email.keyword":
#         value = "emails"
#     if value == "metadata.cardNumbers.cardNumber.keyword":
#         value = "cardNumbers"
#     if value == "metadata.emoji.emoji.keyword":
#         value = 'emoji'
#     if value == "user.username.keyword":
#         value = "main_user"
#     if value == "metadata.usernames.username.keyword":
#         value = "mentioned_user"

#     # LINK
#     if value == "user.url.keyword":
#         value = "link"
#     if value == "link.keyword":
#         value = "main_link"
#     if value == "metadata.urls.url.keyword":
#         value = "mentioned_link"

#     # SENTIMENT ANALYZER
#     if value == "sentiment_analysis.probabilities.positive":
#         value = "positive"
#     if value == "sentiment_analysis.probabilities.negative":
#         value = "negative"
#     if value == "sentiment_analysis.probabilities.neutral":
#         value = "neutral"

#     # GEO
#     if value == "location_finder.country.keyword":
#         value = "country"
#     if value == "location_finder.city.keyword":
#         value = "city"
#     if value == "location_finder.province.keyword":
#         value = "province"
#     if value == "location_finder.place.keyword":
#         value = "place"

#     return value


# def cat_col(value):
#     """
#     convertor functions for pandas aggregator
#     """
#     # NER
#     if value == "person":
#         value = "ner.person"
#     if value == "event":
#         value = "ner.event"
#     if value == "dateTime":
#         value = "ner.dateTime"
#     if value == "location":
#         value = "ner.location"
#     if value == "organization":
#         value = "ner.organization"

#     # KEYWORDS
#     if value == "keywords":
#         value = "keywords"

#     # METADATA
#     if value == "hashtags_one":
#         value = "metadata.hashtags_one"
#     if value == "hashtags_multi":
#         value = "metadata.hashtags_multi"
#     if value == "number":
#         value = "metadata.numbers"
#     if value == "email":
#         value = "metadata.emails"
#     if value == "cardNumbers":
#         value = "metadata.cardNumbers"

#     # emoji
#     if value == "emoji":
#         value = "metadata.emoji"

#     # USERNAME AND urls
#     if value == "username":
#         value = "user.username"

#     # SENTIMENT ANALYZER
#     if value == "positive":
#         value = "sentiment_analysis.probabilities.positive"
#     if value == "negative":
#         value = "sentiment_analysis.probabilities.negative"
#     if value == "neutral":
#         value = "sentiment_analysis.probabilities.neutral"

#     return value


# def col_cat(value):
#     """
#     convertor functions for pandas aggregator
#     """
#     # NER
#     if value == "ner.person":
#         value = "person"
#     if value == "ner.event":
#         value = "event"
#     if value == "ner.dateTime":
#         value = "dateTime"
#     if value == "ner.location":
#         value = "location"
#     if value == "ner.organization":
#         value = "organization"

#     # KEYWORDS
#     if value == "keywords":
#         value = "keywords"

#     # METADATA
#     if value == "metadata.hashtags_one":
#         value = "hashtags_one"
#     if value == "metadata.hashtags_multi":
#         value = "hashtags_multi"
#     if value == "metadata.numbers":
#         value = "number"
#     if value == "metadata.emails":
#         value = "email"
#     if value == "metadata.cardNumbers":
#         value = "cardNumbers"

#     # emoji
#     if value == "metadata.emoji":
#         value = "emoji"

#     # USERNAME AND urls
#     if value == "user.username":
#         value = "username"

#     # SENTIMENT ANALYZER
#     if value == "sentiment_analysis.probabilities.positive":
#         value = "positive"
#     if value == "sentiment_analysis.probabilities.negative":
#         value = "negative"
#     if value == "sentiment_analysis.probabilities.neutral":
#         value = "neutral"

#     return value
