import re
from django.contrib.staticfiles.templatetags.staticfiles import static as _static
#local files for testing
#input_file_name = 'AM_FF_501.txt'
input_file_name = _static + 'dev_test/test_data.txt'

#CAPITALS? maybe preserve, add a 'normalised' version of token on top of 'clean'

def ingest_inventory(_file):

    #check the file's format:
    results = {}
    status = inventory_check(_file)

    if status['has_metadata'] == 0:

        results = {
            'result': 'Failure',
            'messages': [
                ('The uploaded file is missing the metadata section and cannot be processed.','ERROR')
                ]
            }

    elif status['has_transcription'] == 0:

        results = {
            'result': 'Question',
            'issue': 'transcription missing'
            }

    else:
        if status['has_assets'] == 0:
            results = {
                    'messages': [
                        ('The uploaded file did not contain an assets section.','INFO')
                    ]
                }

            #get the starting lines for the sections present and the file's last line
            metadata_tag = '*METADATA*'
            transcription_tag = '*TRANSCRIPTION*'

            with open(_file, 'r') as f:
                lines = f.readlines()
                last_line = len(lines)
                f.seek(0)

                for num, line in enumerate(f, 1):
                    if metadata_tag in line:
                        metadata_start = num

                    elif transcription_tag in line:
                        transcription_start = num

            #process each section
            transcription_end = last_line
            _metadata_end = transcription_start - 1
            _metadata_results = parse_metadata(_file, metadata_start, _metadata_end)
            transcription_results = parse_transcription(_file, transcription_start, transcription_end)

            if transcription_results['result'] == 'OK' and _metadata_results['result'] == 'OK':
                results['result'] = 'OK'
                results['messages'].append('The inventory was successfully processed.','SUCCESS')

            else:
                results['result'] = 'Failure'
                if _metadata_results['result'] != 'OK':
                    results['messages'].append('There were problems processing the metadata section of the file.','ERROR')
                    results['metadata_errors'] = _metadata_results['metadata_output']

                if transcription_results['result'] != 'OK':
                    results['messages'].append('There were problems processing the transcription section of the file.','ERROR')
                    results['transcription_errors'] = transcription_results['transcription_output']


        else:
            #get the starting lines for all the sections and the file's last line
            metadata_tag = '*METADATA*'
            assets_tag = '*ASSETS*'
            transcription_tag = '*TRANSCRIPTION*'

            with open(_file, 'r') as f:
                lines = f.readlines()
                last_line = len(lines)
                f.seek(0)

                for num, line in enumerate(f, 1):
                    if assets_tag in line:
                        assets_start = num

                    elif metadata_tag in line:
                        metadata_start = num

                    elif transcription_tag in line:
                        transcription_start = num

            #process each section
            transcription_end = last_line
            assets_end = transcription_start - 1
            _metadata_end = assets_start - 1
            _metadata_results = parse_metadata(_file, metadata_start, _metadata_end)
            assets_results = parse_assets(_file, assets_start, assets_end)
            transcription_results = parse_transcription(_file, transcription_start, transcription_end)

            if transcription_results['result'] == 'OK' and _metadata_results['result'] == 'OK':
                results['result'] = 'OK'
                if assets_results['result'] == 'OK':
                    results['messages'].append('The inventory was successfully processed.','SUCCESS')

                else:
                    results['messages'].append('There were problems with the list of assets, but the rest of the inventory was processed successfully.','WARNING')
                    results['assets_errors'] = assets_results['assets_output']

            else:
                results['result'] = 'Failure'
                if _metadata_results['result'] != 'OK':
                    results['messages'].append('There were problems processing the metadata section of the file.','ERROR')
                    results['metadata_errors'] = _metadata_results['metadata_output']

                if transcription_results['result'] != 'OK':
                    results['messages'].append('There were problems processing the transcription section of the file.','ERROR')
                    results['transcription_errors'] = transcription_results['transcription_output']

                if assets_results['result'] != 'OK':
                    results['messages'].append('There were problems with the list of assets.','WARNING')
                    results['assets_errors'] = assets_results['assets_output']

    return results


def inventory_check(_file):
    """Takes the data from a DALME Inventory Package and makes sure it's properly formatted"""

    status = {}

    with open(_file, 'r') as f:
        text = f.read()

        #check that the metadata section is there
        if '*METADATA*' in text:
            status['has_metadata'] = 1
        else:
            status['has_metadata'] = 0

        #check if the file has an ASSETS section
        if '*ASSETS*' in text:
            status['has_assets'] = 1
        else:
            status['has_assets'] = 0

        #check if the file has a TRANSCRIPTION section
        if '*TRANSCRIPTION*' in text:
            status['has_transcription'] = 1
        else:
            status['has_transcription'] = 0

    #remove blank lines
    empty_pattern = re.compile(r'^\n', re.MULTILINE)
    text = empty_pattern.sub('', text)
    with open(_file, 'w') as f:
        f.write(text)

    return status


def parse_metadata(_file, start_line, end_line):
    """Parses the metadata section"""

    with open(_file, 'r') as f:
        _data = f.readlines()
        lines = _data[start_line:end_line]
        label_pattern = re.compile(r'^([\w ]+):', re.IGNORECASE)
        line_pattern = re.compile(r'([\w ]+): (.+)', re.IGNORECASE)
        full_pattern = re.compile(r'(.+)', re.IGNORECASE)
        meta_dict = {}

        for line in lines:
            if label_pattern.match(line) != None:
                m = line_pattern.match(line)
                label = m.group(1)
                content = m.group(2)
                meta_dict[label] = content.rstrip()

            else:
                new_content = line.rstrip()
                old_content = meta_dict[label]
                meta_dict[label] = old_content + '\n' + new_content

        _out_list = str(list(meta_dict.items()))
        results = ''.join(_out_list)

    return results


def parse_assets(_file, start_line, end_line):
    """Parses the assets section"""

    with open(_file, 'r') as f:
        _data = f.readlines()
        lines = _data[start_line:end_line]
        line_pattern = re.compile(r'([\w.]+),(.+)\n', re.IGNORECASE)
        assets_dict = {}

        for line in lines:
                m = line_pattern.match(line)
                _filename = m.group(1)
                _folio = m.group(2)
                assets_dict[_filename] = _folio

        results = {
            'result': 'OK',
        }

    return results


def parse_transcription(_file, start_line, end_line):
    """Parses the transcription"""

    with open(_file, 'r') as f:
        _data = f.read().splitlines()
        lines = _data[start_line:end_line]

        #get each line and its atributes
        folio_pattern = re.compile(r'^FOLIO ([0-9]+(v|r)):')
        current_folio = '00'
        line_num = 0
        headers = ['line_no','folio','tokens']
        lines_list = [headers]
        token_type = 'UNDEFINED'

        for line in lines:
            if folio_pattern.match(line):
                m = folio_pattern.match(line)
                current_folio = m.group(1)

            else:
                tokenised = tokenise(line, token_type)
                token_type = tokenised[0]
                tokens_list = tokenised[1]
                line_num = line_num + 1
                list_entry = [line_num,current_folio,tokens_list]
                lines_list.append(list_entry)

            #add code to rejoin tokens split at the end of a line

    results = ''.join(str(lines_list))
    return results

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
            tags_pattern_start = re.compile(r'^(-|\?|\^|\[)')
            tags_pattern_end = re.compile(r'(-|\?|\^|\])$')
            tags_pattern_hyphen = re.compile(r'(_|\[_\])$')
            tags_pattern_period = re.compile(r'\.$')
            tags_pattern_period_enc = re.compile(r'\.([a-z]+)\.', re.IGNORECASE)
            tags_pattern_partial = re.compile(r'([a-z]+)(-|\?|\^|\[|\]|\{|\()([a-z]+)(-|\?|\^|\[|\]|\{|\()(-|\?|\^|\[|\]|\{|\(|([a-z]*))', re.IGNORECASE)

            if tags_pattern.search(token):

                #first check for simple cases of flags that enclose words
                if tags_pattern_start.search(token) and tags_pattern_end.search(token):
                    m = tags_pattern.search(token)
                    flags = []
                    flags.append(m.group(1))
                    tokens_list.append(tokens_dict)
                    _span = str(m.start()) + '-' + str(m.end())
                    clean_token = tags_pattern.sub('', token)
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags
                    tokens_dict['span'] = _span

                #then words that break at the end of a line, we'll just flag them here and rejoin them later
                elif tags_pattern_hyphen.search(token):
                    flags = []
                    flags.append('_')
                    clean_token = tags_pattern_hyphen.sub('', token)
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags

                #eliminate words, like numbers, that have periods enclosing them
                elif tags_pattern_period_enc.search(token):
                    m = tags_pattern_period_enc.search(token)
                    clean_token = m.group(1)
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['token_type'] = token_type

                #then check for full stops, i.e. flag tokens that mark end-of-sentence
                elif tags_pattern_period.search(token):
                    flags = []
                    flags.append('eos')
                    clean_token = tags_pattern_period.sub('', token)
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['token_type'] = token_type
                    tokens_dict['flags'] = flags

                #check for tags enclosing only part of the word
                elif tags_pattern_partial.search(token):
                     m = tags_pattern_partial.search(token)
                     t = tags_pattern.search(token)
                     flags = []
                     flags.append(t.group(1))
                     clean_token = m.group(1) + m.group(3) + m.group(5)
                     _span = str(m.start()) + '-' + str(m.end())
                     tokens_dict = {}
                     tokens_dict['position'] = num - keyword_substract
                     tokens_dict['raw_token'] = token
                     tokens_dict['clean_token'] = clean_token
                     tokens_dict['token_type'] = token_type
                     tokens_dict['flags'] = flags
                     tokens_dict['span'] = _span

                else:
                    clean_token = token
                    tokens_dict = {}
                    tokens_dict['position'] = num - keyword_substract
                    tokens_dict['raw_token'] = token
                    tokens_dict['clean_token'] = clean_token
                    tokens_dict['token_type'] = token_type

            else:
                clean_token = token
                tokens_dict = {}
                tokens_dict['position'] = num - keyword_substract
                tokens_dict['raw_token'] = token
                tokens_dict['clean_token'] = clean_token
                tokens_dict['token_type'] = token_type

            tokens_list.append(tokens_dict)
            results = [token_type, tokens_list]

    return results
