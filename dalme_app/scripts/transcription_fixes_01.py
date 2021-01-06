from dalme_app.models import * # noqa
import lxml.etree as et
import csv


def run():
    transcriptions = Transcription.objects.all() # noqa
    print('Starting: {} transcriptions to process.'.format(transcriptions.count()))
    fixed_braces = []
    problem_braces = []
    xml_parser = et.XMLParser(recover=True)
    ns = {'xml': 'http://www.w3.org/XML/1998/namespace'}
    count = 0
    for t in transcriptions:
        text = t.transcription
        brace_count = text.count('<seg type="brace"')

        if brace_count > 0:
            source = t.source_pages.first().source
            record_data = {
                'transcription': str(t.id),
                'source_id': str(source.id),
                'source_name': source.name,
                'folio': t.source_pages.first().page.name
            }
            tree = et.fromstring('<xml>' + text + '</xml>', xml_parser)
            braces = tree.xpath("//seg[@type='brace']", namespaces=ns)
            all_notes = tree.xpath("//note", namespaces=ns)
            if len(braces) == len(all_notes):
                for i, brace in enumerate(braces):
                    braces[i].attrib['target'] = f'nb_{i}'
                    all_notes[i].attrib[et.QName('http://www.w3.org/XML/1998/namespace', 'id')] = f'nb_{i}'
                    all_notes[i].attrib['type'] = 'brace'
                    if not all_notes[i].getchildren() and all_notes[i].text is None:
                        all_notes[i].text = "?"
                    fixed_braces.append(record_data)
            else:
                for i, brace in enumerate(braces):
                    try:
                        notes = tree.xpath(f'//note[@xml:id="{brace.attrib["target"]}"]', namespaces=ns)
                        for note in notes:
                            if 'type' not in note.attrib or note.attrib['type'] == 'brace':
                                brace.attrib['target'] = f'nb_{i}'
                                note.attrib[et.QName('http://www.w3.org/XML/1998/namespace', 'id')] = f'nb_{i}'
                                note.attrib['type'] = 'brace'
                                if not note.getchildren() and note.text is None:
                                    note.text = "?"
                                break
                        fixed_braces.append(record_data)
                    except KeyError:
                        problem_braces.append(record_data)

            t.transcription = et.tostring(tree, encoding='unicode', xml_declaration=None)[5:-6]
            t.save()

        count += 1
        if (count % 100 == 0):
            print('{} transcriptions processed.'.format(str(count)))

    for name, results in {'fixed_braces': fixed_braces, 'problem_braces': problem_braces}.items():
        keys = results[0].keys()
        with open(f'{name}.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

    return 'done'


def run1():
    transcriptions = Transcription.objects.all() # noqa
    print('Starting: {} transcriptions to process.'.format(transcriptions.count()))
    results = []
    orphans = []
    for t in transcriptions:
        text = t.transcription
        f0 = text.count('<hi rend="indent"></hi>')
        f1 = text.count('<hi rend="indent1"></hi>')
        f2 = text.count('<hi rend="indent2"></hi>')
        findings = f0 + f1 + f2

        if findings > 0:
            try:
                source = t.source_pages.first().source
                results.append({
                    'transcription': str(t.id),
                    'source_id': str(source.id),
                    'source_name': source.name,
                    'folio': t.source_pages.first().page.name
                })
            except AttributeError:
                orphans.append(str(t.id))

    keys = results[0].keys()
    with open('empty_indents.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(orphans)

    return 'done'


def run2():
    transcriptions = Transcription.objects.all() # noqa
    print('Starting: {} transcriptions to process.'.format(transcriptions.count()))
    results = []
    orphans = []
    xml_parser = et.XMLParser(recover=True)
    ns = {'xml': 'http://www.w3.org/XML/1998/namespace'}
    for t in transcriptions:
        text = t.transcription
        tree = et.fromstring('<xml>' + text + '</xml>', xml_parser)
        finds = tree.xpath("//note[not(@xml:id)]", namespaces=ns)
        if finds:
            try:
                source = t.source_pages.first().source
                results.append({
                    'transcription': str(t.id),
                    'source_id': str(source.id),
                    'source_name': source.name,
                    'folio': t.source_pages.first().page.name
                })
            except AttributeError:
                orphans.append(str(t.id))

    keys = results[0].keys()
    with open('notes_wo_id.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(orphans)

    return 'done'
