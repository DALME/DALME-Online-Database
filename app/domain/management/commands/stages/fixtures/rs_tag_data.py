"""Ancillary data for RS tag processing."""

import regex as re  # https://pypi.org/project/regex/

REMOVAL_MATCHES = [
    None,
    'all the above pensioners',
    'blank',
    'blank camerario dicti comunis',
    'eidem',
    'g.',
    'G.',
    'of several words',
    'penes se habere',
    'to comuni de renvoi',
    'unnamed consuli dicti comunis',
    'NAMED ENTITY',
    'apud se habet',
    '; ser Guido did his own plundering',
    'consuli dicti loci',
    'consuli dicte contrate',
    'consuli dicti comunis',
    'consulis novi dicti comunis',
    'consulis veteris dicti comunis',
    'dicto presbitero',
    'dicto priori',
    'dicto sindico',
    'dictus actor',
    'dictus plebanus',
    'dictus presbiter',
    'dictus presbiter dixit apd se habere',
    'domine Abbatisse dicti monasterii',
    'eidem domine',
    'camerario Lucani comunis',
    'dictis redditoribus',
    'la quale e nella cas di lodovico tedaldi',
    'pagolo di luccha razanti',
    'predicto presbitero dicto nomine',
    'suprascripto presbitero',
]

CONTENT_CLEANUP_EXPRESSIONS = [
    [r'\[|\]', ''],
    [r'\^', ''],
    [r'>', ''],
    [r'<', ''],
    [r'\n', ' '],
    [r'\s,\s', ', '],
    [r'\s;\s', '; '],
    [r'\?', ' '],
    [r'\d words? omitted', ' '],
    [r' - ', ' '],
    [r'\s+', ' '],
]

RS_TYPES = {
    1: 'person',
    2: 'organization',
}

ONE_OFF_TRANSFORMS = {
    'Be rart': 'Berart',
    'Fran ces Dodon': 'Frances Dodon',
    'Guill el mi de colle': 'Guillelmi de Colle',
    'Johan A lamon': 'Johan Alamon',
    'Lupori no condam Coscii muratore de Luce': 'Luporino Coscii',
    'Miche le Dati': 'Michele Dati',
    'Ninum magistri Johannis': 'Ninum Johannis',
    'anier d’a lon': 'Anier d’Alon',  # noqa: RUF001
    'antoni gar naut': 'Antoni Garnaut',
    'ar naut quolombier': 'Arnaut Quolombier',
    'eidem Chomo Chomus Bernardi consul comunis Sancti Petris de Guamo': 'Chomus Bernardi',
    'Comune de Capannoro videlicet contra Chellum Chellum Marconaldi de Capannore obligatus dicto ser Johanni simul et insolidum cum dicto suo comuni et imbannitum pro affictu dicto ser Johanni retento': 'Chellum Marconaldi',
    'jacme lo qurasier': 'Jacme Loqurasier',
    'jo han de quinsasc': 'Johan de Quinsasc',
    'jo han telha': 'Johan Telha',
    'guilhem lo quorso': 'Guilhem Loquorso',
    'johan lio net': 'Johan Lionet',
    'johan lo prinse': 'Johan Loprinse',
    'ma tieu brondel': 'Matieu Brondel',
    'pons ba u dric': 'Pons Baudric',
    'pons bau dric': 'Pons Baudric',
    'rainaut bar naut i a': 'Rainaut Barnautia',
    'dicto Mingosso =Minghosso consuli dicti comunis de plebe Sancti Stefani': 'Minghosso',
    'magisgtro Bartholomeo': 'magistro Bartholomeo',
    'b. bertran': 'B. Bertran',
    'francescho di berto da filichaia': 'Francescho di Berto',
    'g. bertran': 'G. Bertran',
    'g. tornaire': 'G. Tornaire',
    'suprascripotus Bene': 'Bene',
    'ser michele di ser Aldobrando': 'Michele di Aldobrando',
    'dona antoneta d’alans': 'Antoneta d’Alans',  # noqa: RUF001
}

ORG_NAME_PATTERNS = [
    (
        re.compile(
            r'^((?:(?:C|c)onsul(?:ibus|atem|atum|es|i) )?(?:C|c)omun(?:em|is|i|e) et homin(?:ibus|es) (?:(?:et )?(?:corpor|officialib|universitat)(?:em|us|is|i) )?)(dict(?:is|i) )?((?:Sanct(?:i|o|a) [A-Z][a-z]+ (?:de|ad|in) [A-Z][a-z]+)|(?:(?:comunis )?(?:de )?[A-Z][a-z]+)|(?:de [A-Z][a-z]+)|(?:[A-Z][A-z]+)|(?:(?:plebis )?(?:[A-Z][a-z]+)))$',
            re.UNICODE,
        ),
        ['{}{}', [1, 3]],
        ['cap_first'],
    ),
    (
        re.compile(
            r'^(?:(?:(?:C|c)omun(?:em|is|i|e))|(?:(?:P|p)leb(?:is|i|e))) (?:de )?(?:(?:(?:(?:Sanct(?:a|o|i) )?(?:[A-Z][a-z]+)) (?:(?:pleb(?:is|i|e)) (?:Sanct(?:a|o|i) )?(?:[A-Z][a-z]+)))|(?:(?:(?:Sanct(?:a|o|i) )?(?:[A-Z][a-z]+))))$',
            re.UNICODE,
        ),
        None,
        ['cap_first'],
    ),
    (
        re.compile(
            r'^(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us|bus))|(?:convent(?:us|u))|(?:abbatie) )?(?: ?domin(?:a|o|um|us))?(?: ?(?:A|a)bbat(?:e|issa) )(?: ?et )?((?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us|bus))|(?:convent(?:us|u))|(?:abbatie))(?:(?: et )(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie)))?(?:(?: et )(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie)))?)( suprascript(?:um|o))?((?: de)?(?:(?: Sanct(?:e|a|i))?(?: [A-Z][a-z]+)))',
            re.UNICODE,
        ),
        ['{}{}', [1, 3]],
        ['cap_first'],
    ),
    (
        re.compile(
            r'^(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie) )?(?: ?et )?(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie))(?:(?: et )(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie)))?(?:(?: et )(?:(?:(?:monialibus |capituli )?(?:monasteri(?:o|i)))|(?:moniali(?:um|us))|(?:convent(?:us|u))|(?:abbatie)))?(?: de)?(?:(?: Sanct(?:e|a|i))?(?: [A-Z][a-z]+))',
            re.UNICODE,
        ),
        None,
        ['cap_first'],
    ),
]

PERSONAL_NAME_PATTERNS = [
    (
        re.compile(r'(?:(?:fratr|frat|magistr|magist|presbit|peir)(?:ero|er|um|e|o|i)) ([A-Z][a-z]+)', re.UNICODE),
        None,
        None,
    ),
    (
        re.compile(
            r'(?<!Sanct(?:i|e|o|a) )(?!Sanct)([A-Z][a-z]+)(?: (?:condam domin(?:i|e|a|um|us)|condam|quondam|upocai|suprascripto|suprascriptum|familie|ser|dict(?:us|um|a|o)|vocat(?:us|um|a|o)|uxor(?:i|e)))?( [A-Z][a-z]+)',
            re.UNICODE,
        ),
        ['{}{}', [1, 2]],
        None,
    ),
    (
        re.compile(
            r'(?<!Sanct(?:i|e|o|a) )(?!Sanct)([A-Z][a-z]+)(?: (?:condam))?( (?:del|de|di) [A-Z][a-z]+)', re.UNICODE
        ),
        ['{}{}', [1, 2]],
        None,
    ),
    (
        re.compile(
            r'(?<!Sanct(?:i|e|o|a) )(?!Sanct)(?:[A-Z][a-z]+)(?: (?:della|delle|dello|dal|del|de|di))?(?: [A-Z][a-z]+)',
            re.UNICODE,
        ),
        None,
        None,
    ),
    (
        re.compile(r"(?<!Sanct(?:i|e|o|a) )(?!Sanct)(?:[A-Z][a-z]+)(?: d’|d')(?:[A-Z][a-z]+)", re.UNICODE),  # noqa: RUF001
        None,
        None,
    ),
    (
        re.compile(
            r'^(?:(?:eisd|eod|eid|predict|dict|suprascript|id)(?:is|em|us|um|o|a|e|i) )?(?:ser )?([A-Z][a-z]+)(?: (?:predict|dict|suprascript)(?:is|us|um|o|a|e|i))?$',
            re.UNICODE,
        ),
        ['{}', [1]],
        None,
    ),
    (
        re.compile(
            r"^(?!(?:(?:eisd|eod|eid|predict|dict|suprascript)(?:is|em|us|um|o|a|e|i)))[a-z]+(?: (?:della|delle|dello|dal|del|de|di))? (?:d'|d’)?[a-z]+$",  # noqa: RUF001
            re.UNICODE,
        ),
        None,
        ['cap_name'],
    ),
    (
        re.compile(
            r'^(?:(?:suprascript|ips|eisd|dict|eid)(?:is|um|us|em|a|i|e|o) )?(?:domin(?:abus|um|us|am|e|o|a) |dompno |ominum |dopno |dona |icti |ser )?(?:consul(?:ibus|i) )?([A-Z][a-z]+)',
            re.UNICODE,
        ),
        ['{}', [1]],
        None,
    ),
    (
        re.compile(r'^[a-z]+$', re.UNICODE),
        None,
        ['cap_first'],
    ),
]
