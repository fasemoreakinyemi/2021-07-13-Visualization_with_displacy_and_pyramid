from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
import spacy
from spacy import displacy
from spacy.matcher import PhraseMatcher, Matcher
from spacy.tokens import Span
import json
    
nlp = spacy.load("en_core_web_sm")

with open("/home/mandela/Doctoral/2021-07-08_document_visualization_with_spacy/livivo_sru/livivo_sru/data/countries.json", encoding="utf8") as f:
    countries = json.loads(f.read())

with open("/home/mandela/Doctoral/2021-07-08_document_visualization_with_spacy/livivo_sru/livivo_sru/data/hosts/animals.txt") as anf:
    animals = list(nlp.pipe(anf.read().splitlines()))

countries_list = list(nlp.pipe(countries))

def find_mst_genotype(text, nlp):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    phrase_matcher.add("likely host", animals)
    phrase_matcher.add("Geo", countries_list)
    mst_pattern = [[{"IS_PUNCT": True}, {"LOWER": "st"}, {"IS_DIGIT": True}],
                    [{"LOWER": "mst"}, {"IS_DIGIT": True}],
                   [{"IS_PUNCT": True}, {"LOWER": "st"}, {"IS_DIGIT": True}],
                   [{"LOWER": "st"}, {"IS_DIGIT": True}],
                   [{"LOWER": "mst"}, {"LOWER": "type"}, {"IS_DIGIT": True},
                    {"POS": "CONJ"}, {"IS_DIGIT": True}],
                   [{"IS_PUNCT": True}, {"LOWER": "mst"}, {"IS_PUNCT": True},
                    {"IS_DIGIT": True}],
                   [{"TEXT": {"REGEX": "M?ST\d+"}}],
                   [{"TEXT": {"REGEX": "m?st\d+"}}]
                  ]
    matcher.add("mst genotype", mst_pattern)
    matches = matcher(doc)
    doc.ents = ()
    for match_id, start, end in matches:
    # create a new Span for each match and use the match_ID as the label
        span = Span(doc, start, end, label=match_id)
        if not span in doc.ents:
            doc.ents = list(doc.ents) + [span]  # add span to doc.ent
    matches = phrase_matcher(doc)
    for match_id, start, end in matches:
    # create a new Span for each match and use the match_ID as the label
        span = Span(doc, start, end, label=match_id)
        if not span in doc.ents:
            doc.ents = list(doc.ents) + [span]  # add span to doc.ent
    return doc

def get_options(ent_type):
    if ent_type == "mst":
        ent_list = ["mst genotype",
                    "likely host",
                    "Geo"
                   ]
        ent_color = {"mst genotype": "#7aecec",
                     "likely host": "#bfeeb7",
                     "Geo": "#feca74"}
        options = {"ents": ent_list, "colors": ent_color}
        return options



@view_config(route_name='retrieve', renderer='livivo_sru:templates/retrieve.jinja2')
def retrieve(request):
    return {}


@view_config(route_name='retrieve_api', renderer='json')
def retrieve_api(request):
    title = request.params['title']
    abstract = request.params['abstract']
    model = request.params['model']
    if int(model) == 1:
        doc = nlp(abstract)
        markup = displacy.render(doc, style="ent", page=False)
    elif int(model) == 2:
        opt = get_options("mst")
        doc = find_mst_genotype(abstract, nlp)
        markup = displacy.render(doc, style="ent", options=opt, page=False)

    return {"title": markup}


#    mst_pattern1 = [{"LOWER": "mst"}, {"IS_DIGIT": True}]
#    mst_pattern2 = [{"IS_PUNCT": True}, {"LOWER": "st"}, {"IS_DIGIT": True}]
#    mst_pattern3 = [{"LOWER": "st"}, {"IS_DIGIT": True}]
#    mst_pattern4 = [{"LOWER": "mst"}, {"LOWER": "type"}, {"IS_DIGIT": True}]
#    mst_pattern5 = [
#        {"LOWER": "mst"},
#        {"LOWER": "type"},
#        {"IS_DIGIT": True},
#        {"POS": "CONJ"},
#        {"IS_DIGIT": True},
#    ]
#    mst_pattern6 = [
#        {"IS_PUNCT": True},
#        {"LOWER": "mst"},
#        {"IS_PUNCT": True},
#        {"IS_DIGIT": True},
#    ]
#    mst_pattern7 = [{"TEXT": {"REGEX": "M?ST\d+"}}]
#    mst_pattern8 = [{"TEXT": {"REGEX": "m?st\d+"}}]
#    matcher.add("mst_pt_1", [mst_pattern1])
#    matcher.add("mst_pt_2", mst_pattern2)
#    matcher.add("mst_pt_3", mst_pattern3)
#    matcher.add("mst_pt_4", mst_pattern4)
#    matcher.add("mst_pt_5", mst_pattern5)
#    matcher.add("mst_pt_6", mst_pattern6)
#    matcher.add("mst_pt_7", mst_pattern7)
#    matcher.add("mst_pt_8", mst_pattern7)

#        ent_list = ["mst_pt_1",
#                    "mst_pt_2",
#                    "mst_pt_3",
#                    "mst_pt_4",
#                    "mst_pt_5",
#                    "mst_pt_6",
#                    "mst_pt_7",
#                    "mst_pt_8"]
#        ent_color = {"mst_pt_1": "#7aecec",
#                     "mst_pt_2": "#bfeeb7",
#                     "mst_pt_3": "#feca74",
#                     "mst_pt_4": "#ff9561",
#                     "mst_pt_5": "#aa9cfc",
#                     "mst_pt_6": "#aa9cfc",
#                     "mst_pt_7": "#9cc9cc",
#                     "mst_pt_8": "#ffeb80"}
#        options = {"ents": ent_list, "colors": ent_color}
