import random
import re
from functools import partial, reduce
from html.parser import HTMLParser
from itertools import chain

import bleach
from django_countries import countries
from unidecode import unidecode

from expert_management import data
from expert_management.models import Affiliation, User
from expert_management.utils.common import non_zero_keys

__all__ = [
    'parse_expertise', 'parse_gender', 'parse_speciality',
    'classify_expertise', 'get_unique_username', 'create_or_get_affiliation'
]


class StartTag:
    def __init__(self, tag):
        self.tag = tag

class EndTag:
    def __init__(self, tag):
        self.tag = tag

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.list_items = []
        self.tags = []
        super().__init__()
    def handle_starttag(self, tag, attrs):
        self.tags.append(StartTag(tag))

    def handle_endtag(self, tag):
        self.tags.append(EndTag(tag))

    def handle_data(self, _data):
        if self.tags:
            last_tag = self.tags[-1]
            if isinstance(last_tag, StartTag) and last_tag.tag == "li":
                self.list_items.append(_data.strip())


def remove_link(attrs, new=False):
    link = attrs[(None, 'href')]
    if link:
        attrs["_text"] = f" {link} "
        attrs.pop((None, 'href'))
        return attrs
    return None

def parse_expertise(expertise):
    if isinstance(expertise, str):
        match = re.search("\d+", expertise)
        if match:
            number_len = len(match[0])
            expertise = expertise[number_len:]
        return [string.strip() for string in expertise.split(" ; ") if string.strip()]
    return []

def parse_speciality(speciality, first_name, last_name):
    def get_delimiter(string):
        delimiter = {
            "unknown": 0,
            ",": string.count(","),
            ";": string.count(";"),
            "<li>": string.count("<li>") + string.count("</li>")
        }
        delimiter_contenders = non_zero_keys(delimiter)
        most_frequent_delimiter = max(delimiter, key=lambda k: delimiter[k])
        return most_frequent_delimiter, delimiter_contenders

    def transform_speciality(speciality):
        if not speciality:
            speciality = ""

        speciality = bleach.clean(
            bleach.linkify(speciality, callbacks=[remove_link]), tags=set(bleach.sanitizer.ALLOWED_TAGS) - {'a', 'i'}, strip=True
        )

        most_frequent_delimiter, delimiter_contenders = get_delimiter(speciality)
        if most_frequent_delimiter == "unknown":
            most_frequent_delimiter = ";"

        speciality = speciality.replace("¶", most_frequent_delimiter)
        if "<li>" in delimiter_contenders:
            if not speciality.startswith("<li>"):
                speciality = "<li>" + speciality
            speciality = bleach.clean(speciality)
        return speciality

    speciality = transform_speciality(speciality)
    most_frequent_delimiter, delimiter_contenders = get_delimiter(speciality)

    # If the speciality field contains "I am" or "I have", it probably means that the expert have
    # described its specialities in a descriptive way and we can't parse it
    if "I am" in speciality or "I have" in speciality or (first_name and first_name in speciality) or (last_name and last_name in speciality):
        speciality = []

    elif most_frequent_delimiter == "<li>" or (most_frequent_delimiter == "," and "<li>" in delimiter_contenders \
            and delimiter_contenders["<li>"] >= delimiter_contenders[","] // 2):
        parser = MyHTMLParser()
        parser.feed(speciality)
        speciality = parser.list_items

    # If there is no delimiter, it mean there are probably one speciality, so we just put it in a list
    elif most_frequent_delimiter == "unknown":
        speciality = [speciality]

    elif most_frequent_delimiter == "," and ";" in delimiter_contenders and delimiter_contenders[";"] >= delimiter_contenders[","]//2:
        speciality = re.split(";|,", speciality)

    else:
        speciality = speciality.split(most_frequent_delimiter)

    return [s.strip() for s in speciality if s.strip() and len(s.strip()) > 3]

def insensitive_intersection(a, b, a_transformers=None, b_transformers=None):
    def apply_transformers(transformers, obj):
        return [_transformer(obj) for _transformer in transformers]

    def replace_slash_with_and(string):
        return string.replace("/", "and")

    # Filling default, it would be nice if python have builtin support for function composition
    a_transformers = a_transformers or [str.lower, lambda x: replace_slash_with_and(str.lower(x))]
    b_transformers = b_transformers or [str.lower]

    intersection_a, intersection_b = [], []
    for element in a:
        found = set(chain.from_iterable(map(partial(apply_transformers, b_transformers), b))).intersection(
            apply_transformers(a_transformers, element)
        )
        if found:
            intersection_a.append(element)
            intersection_b.append(found.pop())
    return intersection_a, intersection_b

def classify_expertise(user_expertise):
    EXPERTISE_CATEGORY_TO_FIELD_MAPPING = {
        "RESEARCH_EXPERTISE": "research_expertise",
        "ATMOSPHERIC_SCIENCES_SUBCATEGORIES": "atmospheric_sciences",
        "HYDROSPHERIC_SCIENCES_SUBCATEGORIES": "hydrospheric_sciences",
        "CRYOSPHERIC_SCIENCES_SUBCATEGORIES": "cryospheric_sciences",
        "EARTH_SCIENCES_SUBCATEGORIES": "earth_sciences",
        "BIOLOGICAL_SCIENCES_SUBCATEGORIES": "biological_sciences",
        "SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES": "social_sciences_and_humanities",
        "INTEGRATED_SYSTEMS_SUBCATEGORIES": "integrated_systems",
        "SPATIAL_SCALE_OF_EXPERTISE": "spatial_scale_of_expertise",
        "STATISTICAL_FOCUS": "statistical_focus",
        "TIME_SCALES": "time_scales",
        "METHODS": "methods",
        "ASSESSMENT_TYPES": "participation_in_assessments",
        "UN_CONVENTIONS_POLICY_PROCESSES": "inputs_or_participation_to_un_conventions",
        "OTHER_EXPERTISE": "other_expertise"
    }

    EXPERTISE_CATEGORIES = list(EXPERTISE_CATEGORY_TO_FIELD_MAPPING.keys())[:-1]

    found = {key: [] for key in EXPERTISE_CATEGORIES}

    for expertise_category in EXPERTISE_CATEGORIES:
        expertise = ", ".join(dict(getattr(data, expertise_category)).keys())
        get_compiled_pattern = lambda phrase: re.compile(
            re.escape(phrase).replace("/", r"(/|and)").replace("and", r"(/|and)"),
            re.IGNORECASE
        )
        _found = {
            usr_expertise: get_compiled_pattern(usr_expertise).search(expertise).group(0)
            for usr_expertise in user_expertise
            if get_compiled_pattern(usr_expertise).search(expertise)
        }

        found[expertise_category] = list(_found.values())
        list(map(user_expertise.remove, _found.keys()))

    # Just throw aways non-categorized expertise
    # found['OTHER_EXPERTISE'] = ', '.join(user_expertise)
    return {
        EXPERTISE_CATEGORY_TO_FIELD_MAPPING[key]: value for key, value in found.items()
    }

def get_unique_username(first_name, last_name):
    def get_possible_usernames(first_name, last_name):
        if first_name:
            first_name = unidecode("".join(first_name.lower().split(" "))).strip(".")
            yield first_name

        if last_name:
            last_name = unidecode("".join(last_name.lower().split(" "))).strip(".")
            yield last_name

        if first_name and last_name:
            yield f"{first_name}.{last_name}"

        if first_name:
            while True:
                yield f"{first_name}{random.randint(1, 99999)}"

    for username in get_possible_usernames(first_name, last_name):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

def parse_gender(gender):
    if gender:
        return {k.value: k for k in data.Gender}.get(gender.upper())

def parse_title(title):
    if title:
        return {k.label: k for k in data.Title}.get(title)

def create_or_get_affiliation(abbreviation, name, street, city, zip_code, country):
    if abbreviation and abbreviation.isupper() and name:
        affiliation_name = name
    else:
        affiliation_name = abbreviation or name

    # some entries have unrelated i.e misc data inside affiliation_name column
    if affiliation_name and len(affiliation_name) < 512:
        try:
            affiliation = Affiliation.objects.get(name__unaccent=affiliation_name)
        except Affiliation.DoesNotExist:
            _data = non_zero_keys({
                "name": affiliation_name,
                "street": street,
                "post_code": zip_code,
                "city": city,
                "country": countries.by_name(country or '')
            })
            affiliation = Affiliation.objects.create(**_data)
        return affiliation
