from __future__ import absolute_import, unicode_literals
import re, requests
from dalme_app.models import par_inventories, par_folios, par_tokens, error_messages, par_objects
from dalme_app import functions
from dalme.celery import app
from async_messages import messages
from django.contrib.auth.models import User


@app.task
def parse_inventory(form_data, inve_id, username):
    """Parses the inventory"""
    inv = par_inventories.objects.get(pk=inve_id)
    inv_name = inv.title
    #first parse the STRUCTURE section
    f = form_data['text']
    _data = f.split('\n')
    str_start = form_data['structure_start']
    str_end = form_data['structure_end']

    str_lines = _data[str_start:str_end]
    line_pattern = re.compile(r'([\w.]+),([0-9]+)', re.IGNORECASE)

    for line in str_lines:
            m = line_pattern.match(line)
            _folio = m.group(1)
            dam_id = m.group(2)
            fol = par_folios(
                inv_id = inv,
                folio_no =_folio,
                dam_id = dam_id,
                creation_username=username,
                modification_username=username
                )
            fol.save()

    if form_data['has_transcription'] == 1:
        #now process the transcription if present
        tr_start = form_data['transcription_start']
        tr_end = form_data['transcription_end']
        tr_lines = _data[tr_start:tr_end]

        #get each line and its atributes
        folio_pattern = re.compile(r'^FOLIO ([0-9]+(v|r)):')
        current_folio = '00'
        line_num = 0
        lines_list = []
        token_type = 'UNDEFINED'

        for line in tr_lines:
            if folio_pattern.match(line):
                m = folio_pattern.match(line)
                current_folio = m.group(1)

            else:
                tokenised = functions.tokenise(line, token_type)
                token_type = tokenised[0]
                tokens_list = tokenised[1]
                line_num = line_num + 1
                list_entry = [line_num,current_folio,tokens_list]
                lines_list.append(list_entry)

            #add code to rejoin tokens split at the end of a line

        #create tokens in database
        for line, folio, tokens in lines_list:
            fol = par_folios.objects.get(inv_id=inv, folio_no=folio)
            #add logic to deal with folio not existing
            for i, token in enumerate(tokens):
                the_token = par_tokens(
                    folio_id=fol,
                    line_no=line,
                    position=token['position'],
                    raw_token=token['raw_token'],
                    clean_token=token['clean_token'],
                    norm_token=token['norm_token'],
                    token_type=token['token_type'],
                    flags=token['flags'],
                    span_start=token['span_start'],
                    span_end=token['span_end'],
                    creation_username=username,
                    modification_username=username
                    )
                the_token.save()

    #message
    functions.notification('req', 2502, para={'inv': inv_name}, user=username)
