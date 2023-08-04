# Generated by Django 3.1.14 on 2023-08-03 15:14

import dalme_public.blocks
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_public', '0012_auto_20210902_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='preview',
            field=models.BooleanField(default=True, help_text='Check this box to set this collection to Preview mode only. It will be made public but not added to the search or map. Only people with the link will be able to access it.'),
        ),
        migrations.AlterField(
            model_name='bibliography',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='collections',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='featuredinventory',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='featuredobject',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='flat',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='body',
            field=wagtail.core.fields.StreamField([('main_image', dalme_public.blocks.MainImageBlock()), ('carousel', dalme_public.blocks.CarouselBlock(wagtail.images.blocks.ImageChooserBlock())), ('chart_embed', wagtail.core.blocks.StructBlock([('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned'), ('full', 'Full-width')]))])), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock(required=False)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left-aligned'), ('right', 'Right-aligned')])), ('show_caption', wagtail.core.blocks.BooleanBlock(default=True, required=False))])), ('text', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock()), ('pullquote', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.core.blocks.PageChooserBlock()), ('bibliography', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=[('A4QHN348', 'Editions'), ('BKW2PVCM', 'Glossaries and dictionaries'), ('QM9AZNT3', 'Methodology'), ('SLIT6LID', 'Studies'), ('FRLVXUWL', 'Other resources')]))])), ('document', wagtail.core.blocks.StructBlock([('type', wagtail.core.blocks.ChoiceBlock(choices=[('document', 'Document'), ('publication', 'Publication'), ('talk', 'Talk')])), ('title', wagtail.core.blocks.CharBlock()), ('abstract', wagtail.core.blocks.CharBlock(required=False)), ('author', wagtail.core.blocks.CharBlock()), ('detail', wagtail.core.blocks.CharBlock(required=False)), ('version', wagtail.core.blocks.FloatBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('date', wagtail.core.blocks.DateBlock())])), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('institution', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.URLBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('external_resource', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('info', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock()), ('date', wagtail.core.blocks.DateBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.core.blocks.RawHTMLBlock()), ('subsection', wagtail.core.blocks.StructBlock([('subsection', wagtail.core.blocks.CharBlock()), ('collapsed', wagtail.core.blocks.BooleanBlock(default=True, required=False)), ('minor_heading', wagtail.core.blocks.BooleanBlock(default=False, required=False))])), ('subsection_end_marker', wagtail.core.blocks.StructBlock([]))], null=True),
        ),
    ]
