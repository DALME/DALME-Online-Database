"""
This file houses all of the miscellaneous functions used elsewhere in the project.
"""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import connections

from async_messages import message_user
import re, json, requests, hashlib, os, uuid, calendar, datetime
import pandas as pd

from . import menus
from .forms import new_user
from .models import (par_inventories, par_folios, par_tokens, par_objects,
    error_messages, Agents, Attribute_types, Attributes, Attributes_DATE,
    Attributes_DBR, Attributes_INT, Attributes_STR, Attributes_TXT, Concepts,
    Content_classes, Content_types, Content_types_x_attribute_types, Headwords,
    Objects, Object_attributes, Places, Source, Pages, Transcriptions,
    Identity_phrases, Object_phrases, Word_forms, Tokens,
    Identity_phrases_x_entities)

#General functions
def inventory_check(_file):
    """
    Takes the data from a DALME Inventory Package and makes sure it's properly formatted
    """

    # TODO: ALSO NEEDS TO CHECK IF INVENTORY ALREADY EXISTS

    metadata_tag = '*METADATA*'
    structure_tag = '*STRUCTURE*'
    transcription_tag = '*TRANSCRIPTION*'

    status = {}

    with _file as f:
        text = f.read()
        text = text.decode("utf-8")

    #check that the metadata section is there
    if metadata_tag in text:
        status['has_metadata'] = 1
    else:
        status['has_metadata'] = 0

    #check if the file has a STRUCTURE section
    if structure_tag in text:
        status['has_structure'] = 1
    else:
        status['has_structure'] = 0

    #check if the file has a TRANSCRIPTION section
    if transcription_tag in text:
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
    """
    Takes a line and returns a list of dictionaries, one for each token, with all the pertinent attributes
    """

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
    """
    Returns information associated with an inventory in the specified format
    """

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
    """
    Gets counts of different types of content based on `item` input string.
    Valid values are: "inventories", "objects", "wiki-articles", "assets", "notarial_sources", "sources", "biblio_sources", "archives".
    All other values for `item` return None
    """
    if item == 'inventories':
        return Sources.objects.filter(is_inventory=True).count()

    elif item == 'archives':
        return Sources.objects.filter(type=19).count()

    elif item == 'sources':
        return Sources.objects.count()

    elif item == 'notarial_sources':
        return Sources.objects.filter(Q(type=12) | Q(type=13)).count()

    elif item == 'biblio_sources':
        return Sources.objects.filter(type__lte=11).count()

    elif item == 'objects':
        return par_objects.objects.count()

    elif item == 'wiki-articles':
        if 'WIKI_BOT_PASSWORD' in os.environ:
            wiki_user = 'Pizzorno@api_bot'
            wiki_pass = os.environ['WIKI_BOT_PASSWORD']
            base_url = 'https://wiki.dalme.org/'
            tokenParams = {
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json",
            }
            loginParams = {
                "action": "login",
                "lgname": wiki_user,
                "lgpassword": wiki_pass,
                "format": "json",
            }
            queryParams = {
                "action": "query",
                "meta": "siteinfo",
                "siprop": "statistics",
                "format": "json",
            }
            #request token
            r1 = requests.post(base_url+'api.php',params=tokenParams)
            loginParams['lgtoken'] = r1.json()['query']['tokens']['logintoken']
            #Login
            r2 = requests.post(base_url+'api.php',data=loginParams,cookies=r1.cookies)
            #query api
            r3 = requests.get(base_url+'api.php',params=queryParams,cookies=r2.cookies)
            stats = r3.json()
            try:
                return stats['query']['statistics']['articles']
            except KeyError:
                return "?"
        else:
            return None

    elif item == 'assets':
        cursor = connections['dam'].cursor()
        cursor.execute("SELECT COUNT(*) FROM resource")
        results = cursor.fetchone()[0]
        return results

        return results

    else:
        return None

def get_dam_preview(resource):
    """
    Returns the url for an image from the ResourceSpace Digital Asset Management
    system for the given resource.
    """
    if 'DAM_BOT_KEY' in os.environ:
        auth_key = os.environ['DAM_BOT_KEY']
        query = 'user=api_bot&function=search_get_previews&param1=' + resource + '&param2=&param3=&param4=0&param5=&param6=asc&param7=&param8=scr&param9=jpg'
        sign_primitive = auth_key + query
        sign = hashlib.sha256(sign_primitive.encode('utf-8')).hexdigest()

        queryParams = {
            "user": "api_bot",
            "function": "search_get_previews",
            "param1": resource,
            "param2": "",
            "param3": "",
            "param4": "0",
            "param5": "1",
            "param6": "asc",
            "param7": "",
            "param8": "scr",
            "param9": "jpg",
            "sign": sign,
        }

        base_url = 'https://dam.dalme.org/api/'
        r1 = requests.get(base_url, params=queryParams)
        res = json.loads(r1.text)

        results = res[0]['url_scr']

        return results

    else:
        return "#"

def get_task_icon(list_id):
    if list_id == 1:
        icon = 'fa-gears'
    return icon

def get_date_from_elements(day, month, year):
    #do some stuff
    if year:
        if month:
            month_name = calendar.month_name[abs(int(month))]
            if day:
                output = str(abs(int(day))) + ' ' + month_name + ', ' + str(abs(int(year)))

            else:
                output = month_name + ' ' + str(abs(int(year)))
        else:
            output = str(abs(int(year)))
    else:
        output = ''

    return output

def create_user(request, data):

    # process the data in form.cleaned_data as required
    username = data.cleaned_data['username']
    first_name = data.cleaned_data['first_name']
    last_name = data.cleaned_data['last_name']
    email = data.cleaned_data['email']
    is_staff = data.cleaned_data['is_staff']
    is_superuser = data.cleaned_data['is_superuser']
    dam_usergroup = data.cleaned_data['dam_usergroup']
    wiki_groups_list = data.cleaned_data['wiki_groups']
    if wiki_groups_list:
        if len(wiki_groups_list) > 1:
            wiki_groups = '|'.join(wiki_groups_list)
        else:
            wiki_groups = wiki_groups_list[0]
    else:
        wiki_groups = 'users'
    wp_role = data.cleaned_data['wp_role']
    #generate extra fields:
    full_name = first_name + ' ' + last_name
    wiki_username = username.title()
    wiki_realname = username
    password = str(uuid.uuid4().hex)
    wp_user_registered = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #create a new user object and add the fields
    the_user = User()
    the_user.username = username
    the_user.first_name = first_name
    the_user.last_name = last_name
    the_user.email = email
    the_user.is_staff = is_staff
    the_user.is_superuser = is_superuser
    the_user.save()
    the_user.profile.dam_usergroup = dam_usergroup
    the_user.profile.wp_role = wp_role
    the_user.profile.full_name = full_name
    the_user.profile.wiki_username = wiki_username
    the_user.profile.wiki_groups = wiki_groups
    the_user.save()

    #create record in WP
    cursor = connections['wp'].cursor()
    cursor.execute("INSERT INTO wp_users (user_login, user_pass, user_nicename, user_email, user_registered, user_status, display_name) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, password, username, email, wp_user_registered, '0', full_name))

    #get wp user id and add it to User object
    cursor.execute("SELECT ID FROM wp_users WHERE user_login = %s",[username])
    wp_userid = cursor.fetchone()[0]
    the_user.profile.wp_userid = wp_userid
    the_user.save()

    #add user metadata
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'first_name', first_name))
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'last_name', last_name))
    cursor.execute("INSERT INTO wp_usermeta (user_id, meta_key, meta_value) VALUES(%s, %s, %s)", (wp_userid, 'wp_capabilities', wp_role))

    #create record in wiki
    cursor = connections['wiki'].cursor()
    cursor.execute("INSERT INTO user (user_name, user_real_name, user_password, user_newpassword, user_email) VALUES(%s, %s, %s, %s, %s)", (wiki_username, wiki_realname, password, password, email))

    #get wiki user id and add it to User object
    cursor.execute("SELECT user_id FROM user WHERE user_name = %s",[wiki_username])
    wiki_userid = cursor.fetchone()[0]
    the_user.profile.wiki_userid = wiki_userid
    the_user.save()

    #add user to groups if necessary
    if wiki_groups != 'user':
        for i in wiki_groups_list:
            if i == 'administrator':
                ug_group = 'sysop'
            elif i == 'bureaucrat':
                ug_group = 'bureaucrat'

            cursor.execute("INSERT INTO user_groups (ug_user, ug_group) VALUES(%s, %s)", (wiki_userid, ug_group))


    #create record in dam
    cursor = connections['dam'].cursor()
    cursor.execute("INSERT INTO user (username, password, fullname, email, usergroup, approved) VALUES(%s, %s, %s, %s, %s, %s)",(username, password, full_name, email,dam_usergroup,1))

    #get dam user id and add it to User object
    cursor.execute("SELECT ref FROM user WHERE username = %s",[username])
    dam_userid = cursor.fetchone()[0]
    the_user.profile.dam_userid = dam_userid
    the_user.save()
