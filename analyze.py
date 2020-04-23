import re


def analyze_article(article, overrides):
    """제목, 본문, 키워드를 분석해서 분류용 태그들을 추출"""
    analyzers = {
        'trivialize': analyze_trivialize,
        'demonize': analyze_demonize,
        'molka': analyze_molka,
        'porn': analyze_porn,
        'abuse': analyze_abuse,
        'metoo': analyze_metoo,
        'bearing': analyze_bearing,
        'gender': analyze_gender,
        'profession': analyze_profession,
    }

    sep = '‖'  # 기사 제목이나 본문에 나오지 않을 특수 기호
    text = sep.join([
        article['title'],
        article['description'],
        article['keywords'],
    ])

    if article['article_id'] in overrides:
        rules = overrides[article['article_id']]
        tags_to_add = {rule[1:] for rule in rules if rule[0] == '+'}
        tags_to_del = {rule[1:] for rule in rules if rule[0] == '-'}
    else:
        tags_to_add = set()
        tags_to_del = set()

    tags = set()
    for tag, analyzer in analyzers.items():
        if tag in tags_to_del:
            continue
        m, text = analyzer(text)
        if m:
            tags.add(tag)

    title, description, _ = text.split(sep)
    return {
        **article,
        'title': title,
        'description': description,
        'tags': sorted(tags | tags_to_add),
    }


def analyze_trivialize(text):
    """'몹쓸 짓' 등 성범죄를 미화하거나 축소하는 표현이 나오는지 검사"""
    if not is_gender_related(text):
        return False, text
    return analyze(
        'trivialize',
        text,
        r'(몹쓸\s?짓|검은\s?손|홧김에|신체\s?접촉)',
        r'(방화|주식|코로나|질병|감염|바이러스|예방)',
    )


def analyze_demonize(text):
    """'인면수심' 등 범죄자를 악마화하거나 비일상적 인물로 묘사하는지 검사"""
    if not is_gender_related(text):
        return False, text
    return analyze(
        'demonize',
        text,
        r'(인면수심|악마|괴물)',
        r'최(영미)?\s시인|봉준호|액체\s?괴물|괴물\s?가면'
    )


def analyze_molka(text):
    """'몰카', '몰래카메라'라는 표현이 나오는지 검사"""
    return analyze(
        'molka',
        text,
        r'(몰카|몰래\s?카메라)',
        r'파파라치\s?학원',
    )


def analyze_metoo(text):
    """'미투'를 '나도 당했다'로, 고발을 고백으로 잘못 표기하는지 검사"""
    return analyze(
        'metoo',
        text,
        r'((미투|me\s?too).{0,5}\(.*?나도 당했다.*?\))|' \
        r'(미투.{1,5}피해.{1,5}고백)'
    )


def analyze_porn(text):
    """'리벤지 포르노'라는 표현이 나오는지 검사"""
    return analyze('porn', text, r'(리벤지\s?포르노)')


def analyze_abuse(text):
    """'아동 포르노'라는 표현이 나오는지 검사"""
    return analyze(
        'abuse',
        text,
        r'((?:아동|청소년|미성년자)\s?(?:포르노|음란물?))',
        r'착취',
    )


def analyze_bearing(text):
    """'저출산'이라는 용어를 쓰는지 검사"""
    return analyze('bearing', text, r'(저출산)', r'저출생')


PROFESSIONS = ['가수','교사', '교수', '기자', '배우', '연예인', '의사']

OCCUPATIONS = ['중생', '고생', '대생', '학생', '종업원', '직원']


def analyze_gender(text):
    """여성만 성별 표기를 하는지 검사"""
    REGIONS = ['여수', '여의도', '여주']

    return analyze(
        'gender',
        text,
        r'(\w+\((\d{0,3}.?[여|女]성?|[여|女]성?.?\d{0,3})\)|' \
        r'\b[여女]\s?(' + '|'.join(OCCUPATIONS) +  '))',
        r'(\w+\((\d{0,3}.?[남|男]성?|[남|男]성?.?\d{0,3})\)|' \
        r'\b[남男][자성]?\s?(' + '|'.join(PROFESSIONS + OCCUPATIONS) + ')|' \
        '(' + '|'.join(REGIONS) + '))',
    )


def analyze_profession(text):
    """여의사 등 여성 전문직만 차별적으로 표현하는지 검사"""
    return analyze(
        'profession',
        text,
        r'\b([여女][자성]?\s?(?:' + '|'.join(PROFESSIONS) + '))',
        r'\b[남男][자성]?\s?(' + '|'.join(PROFESSIONS + OCCUPATIONS) + ')',
    )


def analyze(tag, text, p_pos, p_neg=None):
    """텍스트가 p_pos와 일치하고 p_neg와 불일치하는지 검사"""
    if p_neg and re.search(p_neg, text, re.I):
        return False, text

    marked = re.sub(p_pos, lambda m: markup(tag, m), text, re.I)
    return text != marked, marked


def is_gender_related(text):
    p = r'성[매매|범죄|추행|폭력|행위]|임신|' \
        r'여(성|중생|고생|대생|학생)|(친|의붓)딸|동생|동료|제자|후배'
    return re.search(p, text, re.I)


def markup(tag, m):
    g = next(g for g in m.groups() if g is not None)
    return '{' + tag + '}' + g + '{/' + tag + '}'
