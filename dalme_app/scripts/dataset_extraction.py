import csv
import os
import shutil

from django.contrib.auth.models import User  # noqa

from dalme_app.models import *  # noqa


def extract():
    # define directories for saving data
    dataset = 'italian_11_2021'
    base_dir = f'/Users/gabep/Repos/DALME-Online-Database/extracted_datasets/{dataset}'
    directories = [base_dir, f'{base_dir}/tei', f'{base_dir}/txt']

    # remove directory of dataset if it exists
    if os.path.isdir(base_dir):
        shutil.rmtree(base_dir)

    # (re)create dirs
    for directory in directories:
        os.mkdir(directory)

    # create list of target records
    targets = Attribute.objects.filter( # noqa
        attribute_type=15,  # language
        # attribute_type=36,  # locale
        value_STR='Italian',
        # value_JSON__id='141'  # Marseille || field is JSON blob with id and table name
    )

    print(f'Total targets = {len(targets)}')

    metadata_fields = ['id', 'name', 'short_name', 'parent_name', 'language', 'date', 'record_type', 'locale', 'description']
    metadata = []  # list to store joint metadata
    rec_count = 0  # track records

    for target in targets:
        source = target.sources.first()
        attributes = {a.attribute_type.name: a.value_TXT if a.attribute_type.name == 'Description' else a.value_STR for a in source.attributes.all()}

        if source.type.id == 13 and source.pages:
            transcription_text = ''  # combined plain text of transcribed folios
            source_dir = f'{base_dir}/tei/{source.id}_{source.short_name}'  # dir for tei transcriptions

            for folio in source.pages.all():
                if folio.sources.first().transcription:
                    transcription = folio.sources.first().transcription
                    text = transcription.text_blob
                    if text:
                        # add plain text to combined dump
                        transcription_text = transcription_text + f'## Folio {folio.name} ##\n\n{text}\n\n'

                        # create directory for TEI if necessary
                        if not os.path.isdir(source_dir):
                            os.mkdir(source_dir)

                        # save TEI to individual file
                        with open(f'{source_dir}/{folio.name}.xml', 'w') as file:
                            file.write(transcription.tei)

            if transcription_text != '':
                rec_count += 1  # update count

                # add metadata to list
                metadata.append((
                    source.id,
                    source.name,
                    source.short_name,
                    source.parent.name,
                    attributes.get('Language', 'N/A'),
                    attributes.get('Start date', attributes.get('Date', 'N/A')),
                    attributes.get('Record type', 'NA'),
                    attributes.get('Locale', 'NA'),
                    attributes.get('Description', 'NA'),
                ))

                # save transcription text to file
                with open(f'{base_dir}/txt/{source.id}.txt', 'w') as file:
                    file.write(transcription_text)

    with open(f'{base_dir}/metadata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(metadata_fields)
        for row in metadata:
            writer.writerow(row)

    print(f'Extraction complete on {rec_count} records. Output saved to {base_dir}')
