import re, json, requests, hashlib
from django.contrib import messages
from .models import par_inventories, par_folios, par_tokens, error_messages, par_objects
from django.contrib.auth.models import User
from async_messages import message_user
#from django.contrib.staticfiles.templatetags.staticfiles import static as _static
#local files for testing
#input_file_name = 'AM_FF_501.txt'
#input_file_name = _static + 'dev_test/test_data.txt'


def inventory_check(_file):
    """Takes the data from a DALME Inventory Package and makes sure it's properly formatted"""

    #ALSO NEEDS TO CHECK IF INVENTORY ALREADY EXISTS

    status = {}

    with _file as f:
        text = f.read()
        text = text.decode("utf-8")

    #check that the metadata section is there
    if '*METADATA*' in text:
        status['has_metadata'] = 1
    else:
        status['has_metadata'] = 0

    #check if the file has a STRUCTURE section
    if '*STRUCTURE*' in text:
        status['has_structure'] = 1
    else:
        status['has_structure'] = 0

    #check if the file has a TRANSCRIPTION section
    if '*TRANSCRIPTION*' in text:
        status['has_transcription'] = 1
    else:
        status['has_transcription'] = 0

    #if the STRUCTURE section is missing, just stop and send the report back
    if status['has_structure'] == 0:
        return status

    else:
        #remove blank lines
        empty_pattern = re.compile(r'\n$', re.MULTILINE)
        text = empty_pattern.sub('', text)
        status['text'] = text

        #determine the boundaries of each section
        metadata_tag = '*METADATA*'
        structure_tag = '*STRUCTURE*'
        transcription_tag = '*TRANSCRIPTION*'
        lines = text.split('\n')
        #get the starting lines for all the sections and the file's last line
        last_line = len(lines)
        for num, line in enumerate(lines, 1):
            if metadata_tag in line:
                status['metadata_start'] = num

            elif structure_tag in line:
                status['structure_start'] = num

            elif transcription_tag in line:
                status['transcription_start'] = num

        #assign the outer boundaries of each section
        #if it has a METADATA section, assign outer boundary and parse it
        if status['has_metadata'] == 1:
            status['metadata_end'] = status['structure_start'] - 1
            meta_lines = lines[status['metadata_start']:status['metadata_end']]
            label_pattern = re.compile(r'^([\w ]+):', re.IGNORECASE)
            line_pattern = re.compile(r'([\w ]+): (.+)', re.IGNORECASE)
            full_pattern = re.compile(r'(.+)', re.IGNORECASE)
            #get metadata
            meta_dict = {}
            for line in meta_lines:
                if label_pattern.match(line) != None:
                    m = line_pattern.match(line)
                    label = m.group(1)
                    content = m.group(2)
                    meta_dict[label] = content.rstrip()

                else:
                    new_content = line.rstrip()
                    old_content = meta_dict[label]
                    meta_dict[label] = old_content + '\n' + new_content

            status['metadata'] = meta_dict

            #see which fields are included and whether all the required ones are present
            required_fields = ['Title', 'Archival source', 'Country', 'Series', 'Shelf', 'Transcriber']
            required = 1
            fields = []
            for i in required_fields:
                if i in meta_dict:
                    present = 1
                else:
                    present = 0
                    required = 0
                fields.append((i,present))

            status['fields'] = fields
            status['required'] = required

        if status['has_transcription'] == 1:
            status['structure_end'] = status['transcription_start'] - 1
            status['transcription_end'] = last_line
        else:
            status['structure_end'] = last_line

    return status


def tokenise(line, t_type):
    """takes a line and returns a list of dictionaries, one for each token, with all the pertinent attributes"""

    #create the tokens
    tokens = line.split(' ')
    keyword_substract = 0
    type_pattern = re.compile(r'(CONTEXT|INVENTORY):')
    token_type = t_type
    tokens_dict = {}
    tokens_list = []

    for num, token in enumerate(tokens, 1):
        if type_pattern.match(token):
            m = type_pattern.match(token)
            token_type = m.group(1)
            keyword_substract = keyword_substract + 1

        else:
            #deal with flags, situations to consider:
            #[nostri]
            #presen[tibus]
            #lxxxxvii^o^
            #-Ad evit-
            #(word missing) or (word or words missing)
            #?sin[e]berti?
            #^quondam^
            #-dicti-
            #-?Raymunde?-
            #?als arcs?

            #also flags for need punctuation, so it can be used later for defining sentences
            #and tokens should be lower-case, but track uppercase for determining sentences+proper names?

            tags_pattern = re.compile(r'(-|\?|\^|\[|\]|\.)')
            tags_pattern_enc = re.compile(r'^(-|\?|\^|\[|\.)([a-z]+)(-|\?|\^|\]|\.)$', re.IGNORECASE)
            tags_pattern_hyphen = re.compile(r'(_|\[_\])$')
            tags_pattern_period = re.compile(r'\.$')
            tags_pattern_partial = re.compile(r'([a-z]+)(-|\?|\^|\[|\]|\{|\()([a-z]+)(-|\?|\^|\[|\]|\{|\()(-|\?|\^|\[|\]|\{|\(|([a-z]*))', re.IGNORECASE)

            if tags_pattern.search(token):

                #first check for simple cases of flags that enclose words
                if tags_pattern_enc.search(token):
                    m = tags_pattern_enc.search(token)
                    flags = m.group(1)
                    clean_token = m.group(2)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #then words that break at the end of a line, we'll just flag them here and rejoin them later
                elif tags_pattern_hyphen.search(token):
                    flags = '_'
                    clean_token = tags_pattern_hyphen.sub('', token)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #then check for full stops, i.e. flag tokens that mark end-of-sentence
                elif tags_pattern_period.search(token):
                    flags = 'eos'
                    clean_token = tags_pattern_period.sub('', token)
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None

                #check for tags enclosing only part of the word
                elif tags_pattern_partial.search(token):
                     m = tags_pattern_partial.search(token)
                     t = tags_pattern.search(token)
                     flags = t.group(1)
                     clean_token = m.group(1) + m.group(3) + m.group(5)
                     norm_token = clean_token.lower()
                     span_start = str(m.start())
                     span_end = str(m.end())
                     tokens_dict = {}
                     tokens_dict['position'] = num - keyword_substract
                     tokens_dict['raw_token'] = token
                     tokens_dict['clean_token'] = clean_token
                     tokens_dict['norm_token'] = norm_token
                     tokens_dict['token_type'] = token_type
                     tokens_dict['flags'] = flags
                     tokens_dict['span_start'] = span_start
                     tokens_dict['span_end'] = span_end

                else:
                    flags = ''
                    clean_token = 'FUCK'
                    norm_token = clean_token.lower()
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['norm_token'] = norm_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span_start'] = None
                    tokens_dict['span_end'] = None
            else:
                flags = ''
                clean_token = token
                norm_token = clean_token.lower()
                tokens_dict = {}
                tokens_dict['position'] = num - keyword_substract
                tokens_dict['raw_token'] = token
                tokens_dict['clean_token'] = clean_token
                tokens_dict['norm_token'] = norm_token
                tokens_dict['token_type'] = token_type
                tokens_dict['flags'] = flags
                tokens_dict['span_start'] = None
                tokens_dict['span_end'] = None

            tokens_list.append(tokens_dict)

    results = [token_type, tokens_list]

    return results

def get_inventory(inv, output_type):
    """ returns information associated with an inventory in the specified format """

    if output_type == 'full':
        results = []
        folios = inv.par_folios_set.all()
        folios = folios.order_by('folio_no')
        line = 1
        for i in folios:
            folio_no = i.folio_no
            image_url = get_dam_preview(i.dam_id)
            folio_list = [folio_no,image_url]
            tokens = i.par_tokens_set.all()
            tokens = tokens.order_by('line_no', 'position')
            all_lines = []
            line_list = [line]
            line_tokens = []
            no_tokens = len(tokens)
            for num, token in enumerate(tokens, 1):
                if num == no_tokens:
                    out_token = token.clean_token
                    out_class = get_display_token_class(token.flags)
                    line_tokens.append((out_token, out_class))
                    line_list.append(line_tokens)
                    all_lines.append(line_list)
                    line = line + 1
                    line_list = [line]
                    line_tokens = []

                else:
                    if token.line_no != line:
                        line_list.append(line_tokens)
                        all_lines.append(line_list)
                        line = line + 1
                        line_list = [line]
                        line_tokens = []
                        out_token = token.clean_token
                        out_class = get_display_token_class(token.flags)
                        line_tokens.append((out_token, out_class))

                    else:
                        out_token = token.clean_token
                        out_class = get_display_token_class(token.flags)
                        line_tokens.append((out_token, out_class))

            folio_list.append(all_lines)
            results.append(folio_list)

    return results

def get_display_token_class(flag):
    if flag == '-':
        token_class = 'token_strikeout'

    elif flag == '^':
        token_class = 'token_superscript'

    elif flag == '?':
        token_class = 'token_uncertain'

    elif flag == '[':
        token_class = 'token_supplied'

    elif flag == '{':
        token_class = 'token_imputed'

    elif flag == '':
        token_class = 'token_clean'

    elif flag == '.':
        token_class = 'token_periods'

    elif flag == 'eos':
        token_class = 'token_eos'

    else:
        token_class = 'token_flag_error'

    return token_class

def get_new_error(level):
    errors = error_messages.objects.filter(e_level=level)
    no = errors.count()

    if no == None:
        if level == 10:
            new = 1000
        elif level == 20:
            new = 2000
        elif level == 25:
            new = 2500
        elif level == 30:
            new = 3000
        elif level == 40:
            new = 4000
    else:
        if level == 10:
            new = 1001 + no
        elif level == 20:
            new = 2001 + no
        elif level == 25:
            new = 2501 + no
        elif level == 30:
            new = 3001 + no
        elif level == 40:
            new = 4001 + no

    return new

def notification(request, code, **kwargs):
    base_message = error_messages.objects.get(pk=code)
    msg_text = base_message.e_text
    msg_level = base_message.e_level

    if 'para' in kwargs:
        para = kwargs['para']
        msg_output = msg_text.format(**para)

    elif 'data' in kwargs:
        data = kwargs['data']
        msg_output = msg_text + '<p>' + str(data) + '</p>'

    else:
        msg_output = msg_text

    if 'user' in kwargs:
        user = kwargs['user']
        the_user = User.objects.get(username=user)
        message_user(the_user, msg_output, msg_level)

    else:
        messages.add_message(request, msg_level, msg_output)

def bar_chart():
    results = []
    materials = par_objects.objects.order_by().values_list('material', flat=True).distinct()

    for i in materials:
        count = par_objects.objects.filter(material=i).count()
        entry = (i, count)
        results.append(entry)

    return results

def get_count(item):
    if item == 'inventories':
        counter = par_inventories.objects.count()

    elif item == 'objects':
        counter = par_objects.objects.count()

    elif item == 'wiki-articles':
        wiki_user = 'api_bot'
        wiki_pass = 'ouvyq9b'
        base_url = 'http://dighist.fas.harvard.edu/projects/DALME/wiki/'
        params = '?action=login&lgname=%s&lgpassword=%s&format=json'% (wiki_user,wiki_pass)
        # Login request
        r1 = requests.post(base_url+'api.php'+params)
        token = r1.json()['login']['token']
        params2 = params+'&lgtoken=%s'% token
        r2 = requests.post(base_url+'api.php'+params2,cookies=r1.cookies)
        r3 = requests.get(base_url+'api.php?action=query&meta=siteinfo&siprop=statistics&format=json',cookies=r2.cookies)
        json_data = str(r3.json())
        json_data = json_data.replace('\'', '\"')
        stats = json.loads(json_data)
        counter = stats['query']['statistics']['articles']

    elif item == 'assets':

        counter = 7342

    else:
        counter = None

    return counter

def get_dam_preview(resource):
    #private_key = '98d63d2457fee21dd6100d109422b890'
    auth_key = 'eGV8SXt6bW97Lyx2eyF2JXxwLSYrISgnKiUiLi5xLXd7dCpwLHEgICAsLyIvJHskLncgJnwmKnB6cntyKSYlJX0neiArIysh'
    #dam_user = 'api_bot'
    #query = 'user=' + dam_user + '&function=do_search&param1=florence'
    #sign = hashlib.sha256(private_key.encode('utf-8')+query.encode('utf-8'))
    #req = 'http://dighist.fas.harvard.edu/projects/DALME/dam/plugins/api_core/?' + query + '&sign=' + sign.hexdigest()
    base_url = 'http://dighist.fas.harvard.edu/projects/DALME/dam/plugins/api_search/?key='
    query = auth_key + '&search=' + str(resource) + '&previewsize=scr'
    req = base_url + query
    r1 = requests.get(req)
    json_data = str(r1.json())
    json_data = json_data.replace('\'', '\"')
    res = json.loads(json_data)

    results = 'http://dighist.fas.harvard.edu' + res[0]['preview']

    return results
