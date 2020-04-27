import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.models import Page, Site
from wagtail.core.rich_text import RichText

from dalme_public.models import (
    Collection,
    Collections,
    Essay,
    FeaturedInventory,
    FeaturedObject,
    Features,
    Flat,
    Home,
    Set,
    SubsectionBlock
)


HOME_DATA = {
    'title': 'The Documentary Archaeology of Late Medieval Europe',
    'slug': 'DALME',
    'body': '<p>The goal of DALME is to increase our understanding of Europe’s material horizons during the later Middle Ages, an era when changing patterns of production and consumption altered the material world and transformed the relationship between people and things. We aim to accomplish this by developing a publicly accessible and fully searchable online database of material culture based on household inventories and other textual sources from the period. Along the way, we hope to develop open standards and protocols for the nascent practice of documentary archaeology.</p>',
    'show_in_menus': True,
}

ABOUT_DATA = {
    'title': 'About the Project',
    'short_title': 'About',
    'body': '<p>''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce risus tellus, ultrices aliquet purus eu, tempor malesuada erat. Nulla in lorem sem. Vivamus commodo dignissim dolor vitae efficitur. Integer sit amet risus nisi. Proin a ultrices sem. Vestibulum sit amet sollicitudin purus. Vivamus ultrices aliquam orci. Vestibulum lacinia sapien nec diam pellentesque molestie. Quisque vestibulum tortor consectetur varius porta. Sed est augue, luctus eget sem eget, volutpat interdum arcu. Aliquam bibendum cursus dolor, ut pharetra dolor convallis sit amet. Curabitur ligula lacus, vulputate in lectus ac, porta rutrum leo. In congue elit justo, non tristique velit sagittis vitae. Nam posuere enim id nisi vestibulum pretium.</p><p>Maecenas tincidunt volutpat eleifend. Maecenas ac auctor arcu. Aenean mollis luctus sem, lacinia vehicula nibh sodales et. Pellentesque sagittis, augue eu convallis imperdiet, enim neque pharetra mauris, in accumsan nisl nunc sed arcu. Nam fringilla ornare suscipit. Quisque imperdiet elit nec neque iaculis, vel mattis enim pellentesque. Nullam in ultrices purus. Nulla consectetur eros eget neque rutrum aliquet id a odio. Sed in ornare arcu. Suspendisse condimentum ultrices consequat. Phasellus vel ipsum sit amet justo gravida ultricies ut sed ligula. Praesent tortor eros, cursus fermentum ex in, faucibus accumsan magna. Ut dignissim consequat dolor at auctor. Nam ornare nisi orci, a blandit leo lobortis nec.<p>',
    'show_in_menus': True,
}

PEOPLE_DATA = {
    'title': 'Who We Are',
    'short_title': 'People',
    'slug': 'people',
    'body': '<p>''Maecenas id lacinia sapien, ac suscipit nibh. In congue nunc eu hendrerit tristique. Sed luctus arcu tortor, ut bibendum quam tincidunt ut. Ut maximus augue non nisl efficitur, vitae hendrerit magna sollicitudin. Maecenas mattis magna sed ultrices interdum. Vivamus congue ex in tortor sagittis gravida. Maecenas ipsum arcu, consequat sed metus a, tempus lacinia libero. Vestibulum tristique leo eu lectus dapibus dapibus a at mi. Duis id ante bibendum, tempor nulla at, aliquet mauris. Nullam arcu arcu, malesuada ut molestie consequat, placerat a tortor. Integer ultricies, tortor at ultricies ultrices, magna ante tempus massa, eget ultricies arcu massa a turpis. Fusce gravida ante at nulla varius, vitae egestas massa eleifend. Vestibulum lobortis sit amet justo non lobortis.</p><p>Duis faucibus neque id lectus aliquet sodales. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed congue enim et scelerisque condimentum. Nunc mattis dignissim turpis non faucibus. Cras posuere, dolor a porttitor ultrices, purus tortor venenatis nunc, vel hendrerit augue ante at purus. Morbi scelerisque augue et maximus iaculis. Mauris ac efficitur elit, in bibendum enim. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi volutpat ex nisl, in porta dolor posuere a. Donec porttitor vel libero id ultrices. Cras lacinia dolor nunc, nec tempor libero tincidunt vel. Praesent ut tincidunt dui.</p>',
    'show_in_menus': False,
}


DOCUMENTATION_DATA = {
    'title': 'Documentation',
    'short_title': None,
    'body': '<p>''Integer condimentum, elit a ullamcorper maximus, nisi risus lobortis diam, et convallis libero nisi nec nibh. Aenean sed ultricies erat. Aliquam tempor et velit ac maximus. Maecenas nec arcu bibendum, euismod sem euismod, tincidunt lectus. Donec a nunc sed nisl laoreet consequat. Pellentesque ut mi nisi. Nam commodo turpis risus, at consectetur justo placerat non. In laoreet, justo ac iaculis placerat, quam urna posuere libero, quis dignissim risus mauris sed arcu. Quisque pharetra quis quam vel ultricies. Suspendisse vehicula pellentesque elit in ultrices. Duis consectetur consequat ex, vel lacinia mi elementum eget. Mauris porttitor ipsum egestas tortor mollis, at pulvinar risus lobortis. Pellentesque et dapibus sem, a luctus velit. Sed at tellus rutrum augue tincidunt molestie. Curabitur vulputate rhoncus nulla ac venenatis. Donec aliquet cursus consectetur.</p><p>Cras tristique erat vel ligula viverra aliquam. Ut ornare, nisl vitae tempor pellentesque, ipsum mi fringilla diam, sed dapibus lectus felis in nisi. Fusce erat leo, vehicula at vehicula sit amet, malesuada id elit. Aliquam eu sem magna. Nulla sagittis elit massa, vel pretium velit gravida eu. Aenean ac sollicitudin ligula. Praesent et lacus quis justo facilisis tempus at eu odio. Nulla facilisi. Nunc facilisis, lectus eget bibendum fermentum, nulla quam euismod lorem, eu scelerisque neque elit vel nisi. Curabitur consectetur, nulla quis euismod sodales, eros justo consequat purus, at tempus nibh enim vel felis. Nullam ut laoreet urna, a mattis metus. Cras tellus diam, hendrerit vitae libero nec, fermentum accumsan nunc. Phasellus finibus at augue eu dictum.</p>',
    'show_in_menus': False,
}


PUBLICATIONS_DATA = {
    'title': 'Our Publications',
    'short_title': 'Publications',
    'slug': 'publications',
    'body': '<p>''Fusce et eros aliquam, consectetur nisi ac, consectetur lectus. Ut euismod ut dui in aliquam. Pellentesque sed mauris orci. Nam hendrerit purus eget felis sollicitudin euismod id ac odio. Vestibulum diam ligula, condimentum eu pharetra in, ullamcorper vel nunc. Duis ut ipsum quis ex tincidunt fringilla semper vitae metus. Nam neque justo, aliquam nec quam vel, commodo ullamcorper metus. Curabitur porta lobortis metus, a elementum justo aliquam in. Vestibulum venenatis turpis et elementum eleifend. Nam feugiat justo aliquet odio ornare, ac rutrum ipsum consequat. Maecenas a purus dapibus, pellentesque elit eu, imperdiet enim. Aliquam vel leo ac massa luctus suscipit. Vestibulum neque nulla, porttitor vitae urna vitae, cursus pulvinar arcu. Etiam iaculis leo lacus, et dictum nibh imperdiet vel.</p><p>Etiam a sem sed odio consequat elementum sed vitae mi. Etiam interdum diam sit amet lacus dignissim, in tincidunt tortor tempor. Nulla lacinia nunc mauris, nec placerat nisi fringilla non. Aenean id tellus viverra, maximus est ac, blandit arcu. Nulla pretium quam nec feugiat porta. Fusce ultrices lacinia est at egestas. In ut hendrerit dui. Pellentesque dictum turpis elementum turpis volutpat molestie. Donec facilisis arcu quis tellus sollicitudin, pulvinar facilisis lacus efficitur. Quisque in tortor imperdiet, elementum eros nec, interdum orci. Donec vitae purus ac felis fringilla faucibus eget in metus. Phasellus neque lacus, vulputate mollis posuere in, tempus a ligula. Nulla malesuada erat ut purus bibendum, at blandit augue fermentum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean ornare quam at justo pulvinar dignissim. Morbi tellus odio, pharetra nec urna vel, pretium facilisis felis. Fusce quis est auctor ligula hendrerit congue nec sed est. Integer euismod rhoncus nisl, eget hendrerit nisl laoreet eget. Integer a nulla et ligula pulvinar semper. Aenean pharetra scelerisque urna eget facilisis. Fusce egestas imperdiet scelerisque.</p>',
    'show_in_menus': False,
}


FEATURES_DATA = {
    'title': 'Features',
    'short_title': None,
    'body': '<p>Month by month you can find here objects, inventories and essays of particular interest that have been selected and documented by the members of DALME.</p>',
    'show_in_menus': True,
}


FEATURED_OBJECT_DATA = {
    'owner_id': 5,
    'source_id': '01c0da6f-487f-45ed-aae7-8894fbe4131c',
    'title': 'A Pair of Coconut-Shell Goblets',
    'phrase': '<p><i>Item et due nuces indie ad potandum cum pedibus argenti.</i><br><i>Item et quidam nux indie non munita.</i><p>',
    'body': '<p>Tucked inside a chest in this 1295 inventory were two extremely unusual objects: "Two Indian nuts for drinking, with silver feet." Next to it, the inventory records a third coconut shell, as-yet unworked, waiting its own turn to become a goblet. A number of coconut-shell goblets from Europe\'s past survive today in museum collections and antiquary shops, though few date from the thirteenth century, making this one of the earliest attested objects of this type. No coconut goblets are attested elsewhere in the existing Marseille collection, and their presence here points to the thirteenth-century city\'s far-flung trade horizons. These goblets were found in a chest made of white wood (de ligno albe), which is also unusual. They were stored in the chest alongside six cruets, four of which were made of brass, and with nine candelbra, some made of brass and others of iron. The juxtaposition suggests the possibility that the chest was used to store items associated with the Roman Catholic liturgy.</p>'
}


FEATURED_INVENTORY_DATA = {
    'owner_id': 5,
    'source_id': '82a803bc-31a9-4d2b-90aa-2901ba0d2fa0',
    'title': 'Bonafos Bonet, a victim of the Black Death',
    'body': '<p>This inventory records the possessions of Bonafos Bonet, a citizen and resident of Marseille who died in the Black Death. Bonafos had a wife named Doneta, who died just before him, were immigrants from a town in Languedoc named Lunel, located about 30 kms northeast of Montpellier. The inventory was made on 5 June 1348, in the very midst of the plague, by Bonet Vital, also a citizen and resident of Marseille, who had immigrated from the town of Uzès in the Gard. Bonet Vital was acting as the guardian of Bonafos’s heir, a child named Benet Bensegnori. The Bonet family was Jewish, and the circumstances suggest that couple had left the Kingdom of France amid the expulsion of Jews in 1306 and had settled in Marseille, where they met Bonet Vital, another Jewish immigrant. The two lived comfortably but were not especially well off; among other things, there was no gold or jewels and very little silver. There were a number of items made of silk and a Damascene lamp.</p><p>Jewish inventories are exceedingly uncommon; this is only one of half-dozen or so discovered so far in Marseille (see the collection of Jewish inventories in the DALME environment). This one is interesting for a number of reasons, not the least of which is the fact that Bonafos and Doneta, to judge by the items found in their house, were nearly indistinguishable from their Christian neighbors from the point of view of material culture. The inventory does include a number of brightly colored articles of clothing as well as children\'s things. One of the most unusual items is identified as "quendam rasali cirici," that is to say a type of fabric known in Iberia as a rançal made of silk. Inside a chest, Bonet discovered a set of deep blue garments lined with ruby red sendal and fringed with squirrel fur and tassels called "rapra." No kitchen items were listed in the inventory and the act ends abruptly, suggesting that a page or more may be missing.</p>'
}


ESSAY_DATA = {
    'owner_id': 5,
    'title': 'Gendered Items of Clothing',
    'body': '<p>Etiam eget scelerisque lorem, id sollicitudin mi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Quisque semper ante in leo vestibulum auctor. Donec at libero id mauris laoreet ullamcorper eget at lectus. Nullam lectus sem, eleifend sed lacinia vel, ornare eget lacus. Donec tellus quam, lobortis at arcu sed, cursus pulvinar nulla. Morbi et quam eget ante convallis dapibus. Pellentesque molestie erat nunc, ac dignissim urna sodales vitae. Sed elementum sagittis luctus. Aliquam et leo sit amet odio convallis dignissim at vel arcu. Phasellus maximus ligula sed sollicitudin luctus. Proin tempus imperdiet augue, ut cursus mauris semper non.</p><p>Cras non turpis magna. Etiam non consequat tellus. Mauris eu mauris ullamcorper, aliquam arcu vitae, egestas tortor. Vestibulum in odio quam. Vestibulum facilisis, lectus eget sodales dapibus, enim nibh sodales lacus, ut accumsan urna urna ac elit. Nulla nisl justo, venenatis vitae arcu vitae, sodales porttitor est. Ut elementum lectus vitae ultricies semper. Duis ut pharetra ipsum, ultrices rutrum nibh. Aenean commodo, ante non dictum dictum, magna elit sodales nisl, sed vulputate quam risus vitae metus. Sed ultricies magna id mi eleifend tincidunt. Nullam molestie lectus quis mauris imperdiet, consequat lobortis nisi gravida. Cras eleifend mi id tortor dictum vestibulum. Mauris purus nulla, ultrices sed felis eu, venenatis suscipit quam.</p>'
}


COLLECTIONS_DATA = {
    'title': 'Our Collections',
    'short_title': 'Collections',
    'slug': 'collections',
    'body': '<p>DALME currently houses two collections, both of which include a preliminary array of sets.</p>',
    'show_in_menus': True,
}


MARSEILLE_SET = {
    'source_set_id': '77d709a6-6b87-4116-9c46-d6dd8468129e',
    'title': 'Marseille and its Environs',
    'description': '<p>Donec ullamcorper urna sit amet vulputate bibendum. Sed sed tincidunt turpis. Ut mattis pharetra neque. Aenean pharetra rutrum scelerisque.</p>',
    'body': '<p>The records from the city of Marseille constitute the oldest and currently the richest set of inventories in the entire DALME collection. The initial set was identified by Dan Smail in archival work dating from the 1990s and was substantially enlarged by Nathan Melson in 2011–12. Additional inventories were collected in 2018, including a set of inventories previously transcribed and published by Christine Barnel.</p>',
    'subsections': [
        ('subsection', {
            'heading': 'The Region',
            'body': RichText('<p>Vestibulum vitae sagittis purus. Sed aliquet tincidunt neque. Donec vitae leo imperdiet, vehicula ligula gravida, sollicitudin ligula. Duis sit amet nulla neque. In hac habitasse platea dictumst. Vivamus tortor metus, faucibus a pulvinar non, ullamcorper non leo. Morbi a aliquam turpis. Duis ac eleifend nunc. Nam imperdiet velit ac enim venenatis, vel porta metus elementum. Vestibulum viverra placerat accumsan. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>'),
        }),
        ('subsection', {
            'heading': 'Sampling',
            'body': RichText('<p>The majority of the Marseille inventories have been collected from the city\'s extant notarial archive, which is the oldest and richest in the territory of modern France, dating back to 1248. Several extant court registers of post-mortem inventories, from the years 1298, 1405, and 1420-22, provided an important supplement, along with several acts preserved in records of the episcopal court. The records of several of the city\'s hospitals and religious foundations also contributed several dozen inventories of important benefactors, typically in the form of parchment rolls. Within the date range covered by the sample, the current collection may include half or more of all extant inventories from the city and the immediate region, with a probable bias toward the first half of the fifteenth century, a period that was particularly well sampled. The acts in the collection include post- mortem inventories, inventories of insolvent estates, inventories of fugitives from justice, and lists of objects identified in estate divisions.</p>'),
        }),
        ('subsection', {
            'heading': 'Goals and Prospects',
            'body': RichText('<p>Proin sollicitudin neque dignissim mauris luctus cursus. Maecenas vitae augue posuere, mattis elit id, placerat magna. Fusce laoreet quam non justo viverra, nec consequat augue fermentum. Nam mattis, tellus at pulvinar condimentum, libero libero ultrices velit, nec euismod dui felis in ligula. Morbi mollis augue eget tempus dignissim. Sed aliquam odio at interdum finibus. Curabitur consequat hendrerit libero non lobortis. Donec ut leo turpis. Vivamus convallis fringilla nisl nec tristique. Nulla congue, urna ut accumsan varius, sapien augue tristique orci, id rutrum orci est in justo.</p>'),
        }),
        ('subsection', {
            'heading': 'Highlights',
            'body': RichText('<p>Vestibulum fermentum enim sem, quis mattis nunc blandit hendrerit. Morbi commodo dolor nec nisi porta, vel fringilla velit pretium. Aliquam erat volutpat. Donec egestas sodales venenatis. Cras id iaculis dui. Vestibulum commodo viverra magna. Aliquam erat volutpat. Donec sodales sit amet ante non egestas. Maecenas mollis tristique mi quis dignissim. Vestibulum tempus malesuada massa, vel vestibulum lectus tristique in. Morbi in ex ac enim ultrices pharetra. Duis malesuada fermentum viverra. Integer suscipit imperdiet velit, nec finibus dolor consectetur ut. Nullam ac augue vestibulum, tincidunt massa eget, vehicula leo. Quisque pellentesque metus ac ipsum tempor, eget condimentum elit auctor.</p>'),
        }),
        ('subsection', {
            'heading': 'Outcomes',
            'body': RichText('<p>Maecenas aliquam eros eu sollicitudin feugiat. Aliquam tortor enim, venenatis a pulvinar accumsan, maximus nec eros. Donec sem sapien, bibendum vitae ornare auctor, ornare eget velit. Vivamus non fermentum sem. Nulla luctus justo ultrices, venenatis sapien non, convallis libero. Mauris in dolor mollis, molestie elit dapibus, eleifend lacus. Suspendisse finibus fermentum feugiat. Nulla eget elit nec nisl bibendum tincidunt. Vestibulum varius a libero a rhoncus. In varius ex quis risus sagittis, id feugiat risus tempor. Pellentesque sed volutpat tellus. Nunc odio turpis, congue aliquam eleifend a, efficitur fringilla ligula. Nam et tempus diam. Sed dictum ante in elementum hendrerit. Cras ligula velit, rhoncus et mattis et, bibendum vel magna.</p>'),
        }),
    ]
}


COLLECTION_DATA = [
    {
        'title': 'The Secular Household of Late Medieval Europe',
        'description': '<p>Donec efficitur metus a mauris feugiat vulputate. Sed vehicula dui ac turpis luctus interdum. Phasellus vestibulum justo id lacus ornare cursus. Proin at viverra ex, ut sodales risus.</p>',
        'body': '<p>Nam justo risus, consequat et pulvinar non, fermentum nec dui. Vivamus tempor diam eleifend, volutpat libero in, accumsan lacus. Cras sed lacinia erat. Phasellus tincidunt urna eros, at scelerisque quam vestibulum id. Integer id felis dui. Pellentesque gravida ultricies nisl, at ultrices risus rutrum sit amet. Duis vehicula gravida turpis, et dapibus lorem molestie eu. Fusce commodo facilisis tortor, in faucibus mauris blandit pulvinar. Nulla at lacus sit amet magna sollicitudin mollis. In dignissim dictum dignissim. Mauris est purus, porttitor quis consequat non, fringilla non libero.</p>',
        'set_data': [MARSEILLE_SET]
    },
]


class Command(BaseCommand):
    help = 'Create the DALME public site tree.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home = None
        self.features = None
        self.collections = None
        self.sets = None

    def create_collection_and_set_pages(self):
        for data in COLLECTION_DATA:
            set_data = data.pop('set_data')
            collection = self.collections.add_child(
                instance=Collection(**data)
            )
            for subdata in set_data:
                collection.add_child(instance=Set(**subdata))

    def create_collections_page(self):
        self.collections = self.home.add_child(
            instance=Collections(**COLLECTIONS_DATA)
        )

    def create_feature_pages(self):
        self.features.add_child(instance=FeaturedObject(**FEATURED_OBJECT_DATA))
        self.features.add_child(instance=FeaturedInventory(**FEATURED_INVENTORY_DATA))
        self.features.add_child(instance=Essay(**ESSAY_DATA))

    def create_features_page(self):
        self.features = self.home.add_child(instance=Features(**FEATURES_DATA))

    def create_flat_pages(self):
        self.home.add_child(instance=Flat(**ABOUT_DATA))
        self.home.add_child(instance=Flat(**PEOPLE_DATA))
        self.home.add_child(instance=Flat(**DOCUMENTATION_DATA))
        self.home.add_child(instance=Flat(**PUBLICATIONS_DATA))

    def create_home(self):
        Site.objects.first().delete()
        Page.objects.last().delete()

        root = Page.objects.first()
        home = root.add_child(instance=Home(**HOME_DATA))

        Site.objects.create(
            hostname='localhost',
            site_name='DALME',
            root_page=root,
            is_default_site=True
        )
        return home

    def handle(self, *args, **options):
        self.home = self.create_home()
        self.create_flat_pages()
        self.create_features_page()
        self.create_feature_pages()
        self.create_collections_page()
        self.create_collection_and_set_pages()

        # TODO: Remove this!
        user = User.objects.get(username='jhrr')
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Created DALME'))
