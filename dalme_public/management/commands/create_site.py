import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from wagtail.core.models import Page, Site
from wagtail.core.rich_text import RichText

from dalme_app.models import Source
from dalme_public.models import (
    Corpus,
    Collections,
    Essay,
    FeaturedInventory,
    FeaturedObject,
    Features,
    Flat,
    Home,
    Set,
    Section,
)


HOME_DATA = {
    'title': 'The Documentary Archaeology of Late Medieval Europe',
    'slug': 'DALME',
    'body': [
        ('text', RichText('<p>The goal of DALME is to increase our understanding of Europe’s material horizons during the later Middle Ages, an era when changing patterns of production and consumption altered the material world and transformed the relationship between people and things. We aim to accomplish this by developing a publicly accessible and fully searchable online database of material culture based on household inventories and other textual sources from the period. Along the way, we hope to develop open standards and protocols for the nascent practice of documentary archaeology.</p>')),
    ],
    'show_in_menus': True,
}

PROJECT_DATA = {'title': 'Project', 'show_in_menus': True}

ABOUT_DATA = {'title': 'About', 'show_in_menus': True}

PROJECT_FLAT_DATA = [
    {
        'title': 'Overview',
        'body': [
            ('text', RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>')),
            ('text', RichText('<p>Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.</p>')),
            ('text', RichText('<p>Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.</p>')),
            ('text', RichText('<p>Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>')),
        ],
    },
    {
        'title': 'Documentation',
        'body': [
            ('text', RichText('<p>The DALME project is unequivocally committed to the ideals of openness and transparency as fundamental to scholarship and the scholarly community.</p>')),
            ('text', RichText('<p>We rely as much as possible on existing standards with broad support in the scholarly community. We only develop our own solutions where it is appropriate (and then contribute them back to the community). This page serves as an entry point to the project’s documentation. The entries below explain aspects of the project’s methods and developing standards, and are made available under a Creative Commons Attribution-ShareAlike 4.0 International License. The source code of the software we develop is available on the project’s GitHub repository under an open source, BSD-style license.</p>')),
            ('text', RichText('<p>Our goal is to be equally open with our datasets, by making them available under the Open Data Commons Attribution License v1.0, through our online database, and as Linked Open Data. In addition, static versions can be downloaded, in a range of open formats (eg N-triples, Notation-3, Comma Separated Values), from the project’s dataverse.</p>')),
            ('heading', 'Documents'),
        ],
    },
    {
        'title': 'Publications',
        'body': [
            ('text', RichText('The following list includes publications based on the DALME dataset. A number of additional articles are awaiting publication in journals and will be added as they become available. In addition, we have featured DALME in presentations at venues all over the United States as well as in France and England, and a list is provided below.')),
            ('heading', 'Books and Articles'),
            ('heading', 'Talks and Presentations'),
            ('external_resource', {
                'title': 'Debt: A Natural History',
                'info': 'Daniel Lord Smail. Lecture delivered at Trinity College Dublin. Invited speaker.',
                'url': 'https://www.youtube.com/watch?v=SRmeANXMTNI',
                'date': datetime.date(2017, 11, 1),
            }),
        ],
    },
]

ABOUT_FLAT_DATA = [
    {
        'title': 'About DALME',
        'body': [
            ('text', RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>')),
            ('text', RichText('<p>Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.</p>')),
        ],
    },
    {
        'title': 'People',
        'body': [
            ('text', RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore.</p>')),
            ('subsection', {'subsection': 'Project Team'}),
            ('subsection', {'subsection': 'Contributors'}),
            ('subsection', {
                'subsection': 'Advisory Board',
                'collapsed': False,
            }),
            ('person', {
                'name': 'Samuel Kline Cohn',
                'job': 'Professor of History',
                'institution': 'University of Glasgow',
                'url': 'https://www.gla.ac.uk/schools/humanities/staff/samuelcohn/'
            }),
            ('person', {
                'name': 'Maryanne Kowaleski',
                'job': 'Professor of History',
                'institution': 'Fordham University',
                'url': 'https://www.fordham.edu/info/20762/faculty/6408/maryanne_kowaleski'
            }),
            ('person', {
                'name': 'Juan Vicente Garcia-Marsilla',
                'job': 'Professor of Art History',
                'institution': 'University of Valencia',
                'url': 'https://uv.academia.edu/JuanVicenteGarc%C3%ADaMarsilla'
            }),
            ('person', {
                'name': 'Rena Lauer',
                'job': 'Assistant Professor of History',
                'institution': 'Oregon State University',
                'url': ''
            }),
        ],
    },
    {
        'title': 'Contact',
        'body': [
            ('text', RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore.</p>')),
        ],
        'show_contact_form': True,
    },
    {
        'title': 'Privacy',
        'body': [
            ('text', RichText('<p>Your privacy and the security of your data is important to us. To better protect your privacy, we provide this notice explaining our online information practices and the choices you can make about the way your information is collected and used. To make this notice easy to find, we make it available on our homepage and at every point where personally identifiable information may be requested. This notice applies to all information collected or submitted on the DALME website.</p>')),
            ('heading', 'The Information We Collect'),
            ('text', RichText('<p>We may collect non-personal information about the computer, mobile device or other device you use to access this website, such as IP address, geolocation information, unique device identifiers, browser type, browser language, or other information of this nature. We use this information in an aggregate fashion to track access to our website. At no time do we disclose site usage by individual IP addresses.</p>')),
            ('text', RichText('<p>On some pages, you can make requests and register to receive materials. The types of personal information collected on these pages are name and email address. On some pages, you can submit information to other people. For example, if you want to forward an article to another person, you will need to submit the recipient’s email address.</p>')),
            ('heading', 'The Way We Use Information'),
            ('text', RichText('<p>We use the information you provide about yourself only to complete the task for which it is requested. We do not share this information with outside parties. We use return email addresses to answer the email we receive. Such addresses are not used for any other purpose and are not shared with outside parties. We employ non-identifying and aggregate information to better design our website. Finally, we never use or share the personally identifiable information provided to us online in ways unrelated to the ones described above without also providing you with an opportunity to opt-out or otherwise prohibit such unrelated uses.</p>')),
            ('text', RichText('<p>We use your IP address to help diagnose problems with our server and to administer our website by identifying (1) which parts of our site are most heavily used, and (2) which portion of our audience comes from within the Harvard network. We do not link IP addresses to anything personally identifiable. This means that user sessions will be tracked, but the users will remain anonymous.</p>')),
        ],
    },
]

FEATURES_DATA = {
    'title': 'Features',
    'short_title': None,
    'body': [
        ('text', RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore.</p>')),
    ],
    'show_in_menus': True,
}


FEATURED_OBJECT_DATA = {
    'owner_id': 5,
    'source_id': '01c0da6f-487f-45ed-aae7-8894fbe4131c',
    'title': 'A Pair of Coconut-Shell Goblets',
    'body': [
        ('pullquote', RichText('<p>Item et due nuces indie ad potandum cum pedibus argenti.</p><p>Item et quidam nux indie non munita.</p>')),
        ('text', RichText('<p>Tucked inside a chest in this 1295 inventory were two extremely unusual objects: "Two Indian nuts for drinking, with silver feet." Next to it, the inventory records a third coconut shell, as-yet unworked, waiting its own turn to become a goblet. A number of coconut-shell goblets from Europe\'s past survive today in museum collections and antiquary shops, though few date from the thirteenth century, making this one of the earliest attested objects of this type. No coconut goblets are attested elsewhere in the existing Marseille collection, and their presence here points to the thirteenth-century city\'s far-flung trade horizons. These goblets were found in a chest made of white wood (de ligno albe), which is also unusual. They were stored in the chest alongside six cruets, four of which were made of brass, and with nine candelbra, some made of brass and others of iron. The juxtaposition suggests the possibility that the chest was used to store items associated with the Roman Catholic liturgy.</p>')),
    ],
}


FEATURED_INVENTORY_DATA = {
    'owner_id': 5,
    'source_id': '82a803bc-31a9-4d2b-90aa-2901ba0d2fa0',
    'title': 'Bonafos Bonet, a victim of the Black Death',
    'body': [
        ('text', RichText('<p>This inventory records the possessions of Bonafos Bonet, a citizen and resident of Marseille who died in the Black Death. Bonafos had a wife named Doneta, who died just before him, were immigrants from a town in Languedoc named Lunel, located about 30 kms northeast of Montpellier. The inventory was made on 5 June 1348, in the very midst of the plague, by Bonet Vital, also a citizen and resident of Marseille, who had immigrated from the town of Uzès in the Gard. Bonet Vital was acting as the guardian of Bonafos’s heir, a child named Benet Bensegnori. The Bonet family was Jewish, and the circumstances suggest that couple had left the Kingdom of France amid the expulsion of Jews in 1306 and had settled in Marseille, where they met Bonet Vital, another Jewish immigrant. The two lived comfortably but were not especially well off; among other things, there was no gold or jewels and very little silver. There were a number of items made of silk and a Damascene lamp.</p><p>Jewish inventories are exceedingly uncommon; this is only one of half-dozen or so discovered so far in Marseille (see the collection of Jewish inventories in the DALME environment). This one is interesting for a number of reasons, not the least of which is the fact that Bonafos and Doneta, to judge by the items found in their house, were nearly indistinguishable from their Christian neighbors from the point of view of material culture. The inventory does include a number of brightly colored articles of clothing as well as children\'s things. One of the most unusual items is identified as "quendam rasali cirici," that is to say a type of fabric known in Iberia as a rançal made of silk. Inside a chest, Bonet discovered a set of deep blue garments lined with ruby red sendal and fringed with squirrel fur and tassels called "rapra." No kitchen items were listed in the inventory and the act ends abruptly, suggesting that a page or more may be missing.</p>')),
    ],
}


ESSAY_DATA = {
    'owner_id': 1,
    'source': None,
    'title': 'Gender and Colour in Clothing',
    'body': [
        ('text', RichText('<p>Etiam eget scelerisque lorem, id sollicitudin mi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Quisque semper ante in leo vestibulum auctor. Donec at libero id mauris laoreet ullamcorper eget at lectus. Nullam lectus sem, eleifend sed lacinia vel, ornare eget lacus. Donec tellus quam, lobortis at arcu sed, cursus pulvinar nulla. Morbi et quam eget ante convallis dapibus. Pellentesque molestie erat nunc, ac dignissim urna sodales vitae. Sed elementum sagittis luctus. Aliquam et leo sit amet odio convallis dignissim at vel arcu. Phasellus maximus ligula sed sollicitudin luctus. Proin tempus imperdiet augue, ut cursus mauris semper non.</p><p>Cras non turpis magna. Etiam non consequat tellus. Mauris eu mauris ullamcorper, aliquam arcu vitae, egestas tortor. Vestibulum in odio quam. Vestibulum facilisis, lectus eget sodales dapibus, enim nibh sodales lacus, ut accumsan urna urna ac elit. Nulla nisl justo, venenatis vitae arcu vitae, sodales porttitor est. Ut elementum lectus vitae ultricies semper. Duis ut pharetra ipsum, ultrices rutrum nibh. Aenean commodo, ante non dictum dictum, magna elit sodales nisl, sed vulputate quam risus vitae metus. Sed ultricies magna id mi eleifend tincidunt. Nullam molestie lectus quis mauris imperdiet, consequat lobortis nisi gravida. Cras eleifend mi id tortor dictum vestibulum. Mauris purus nulla, ultrices sed felis eu, venenatis suscipit quam.</p>')),
    ],
}


COLLECTIONS_DATA = {
    'title': 'Collections',
    'body': [
        ('text', RichText('<p>Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.</p>')),
        ('text', RichText('<p>Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.</p>')),
    ],
    'show_in_menus': True,
}

CORPUS_DATA = {
    'title': 'The Secular Household of Late Medieval Europe',
    'description': RichText('<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore.</p>'),
}

MARSEILLE_SET = {
    'source_set_id': '77d709a6-6b87-4116-9c46-d6dd8468129e',
    'title': 'Marseille and its Environs',
    'body': [
        ('text', RichText('<p>The records from the city of Marseille constitute the oldest and currently the richest set of inventories in the entire DALME collection. The initial set was identified by Dan Smail in archival work dating from the 1990s and was substantially enlarged by Nathan Melson in 2011–12. Additional inventories were collected in 2018, including a set of inventories previously transcribed and published by Christine Barnel.</p>')),
        ('subsection', {'subsection': 'The Region'}),
        ('text', RichText('<p>Vestibulum vitae sagittis purus. Sed aliquet tincidunt neque. Donec vitae leo imperdiet, vehicula ligula gravida, sollicitudin ligula. Duis sit amet nulla neque. In hac habitasse platea dictumst. Vivamus tortor metus, faucibus a pulvinar non, ullamcorper non leo. Morbi a aliquam turpis. Duis ac eleifend nunc. Nam imperdiet velit ac enim venenatis, vel porta metus elementum. Vestibulum viverra placerat accumsan. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>')),
        ('subsection', {'subsection': 'Sampling'}),
        ('text', RichText('<p>The majority of the Marseille inventories have been collected from the city\'s extant notarial archive, which is the oldest and richest in the territory of modern France, dating back to 1248. Several extant court registers of post-mortem inventories, from the years 1298, 1405, and 1420-22, provided an important supplement, along with several acts preserved in records of the episcopal court. The records of several of the city\'s hospitals and religious foundations also contributed several dozen inventories of important benefactors, typically in the form of parchment rolls. Within the date range covered by the sample, the current collection may include half or more of all extant inventories from the city and the immediate region, with a probable bias toward the first half of the fifteenth century, a period that was particularly well sampled. The acts in the collection include post- mortem inventories, inventories of insolvent estates, inventories of fugitives from justice, and lists of objects identified in estate divisions.</p>')),
        ('subsection', {'subsection': 'Goals and Prospects'}),
        ('text', RichText('<p>Proin sollicitudin neque dignissim mauris luctus cursus. Maecenas vitae augue posuere, mattis elit id, placerat magna. Fusce laoreet quam non justo viverra, nec consequat augue fermentum. Nam mattis, tellus at pulvinar condimentum, libero libero ultrices velit, nec euismod dui felis in ligula. Morbi mollis augue eget tempus dignissim. Sed aliquam odio at interdum finibus. Curabitur consequat hendrerit libero non lobortis. Donec ut leo turpis. Vivamus convallis fringilla nisl nec tristique. Nulla congue, urna ut accumsan varius, sapien augue tristique orci, id rutrum orci est in justo.</p>')),
        ('subsection', {'subsection': 'Highlights', 'collapsed': False}),
        ('text', RichText('<p>Vestibulum fermentum enim sem, quis mattis nunc blandit hendrerit. Morbi commodo dolor nec nisi porta, vel fringilla velit pretium. Aliquam erat volutpat. Donec egestas sodales venenatis. Cras id iaculis dui. Vestibulum commodo viverra magna. Aliquam erat volutpat. Donec sodales sit amet ante non egestas. Maecenas mollis tristique mi quis dignissim. Vestibulum tempus malesuada massa, vel vestibulum lectus tristique in. Morbi in ex ac enim ultrices pharetra. Duis malesuada fermentum viverra. Integer suscipit imperdiet velit, nec finibus dolor consectetur ut. Nullam ac augue vestibulum, tincidunt massa eget, vehicula leo. Quisque pellentesque metus ac ipsum tempor, eget condimentum elit auctor.</p>')),
        ('subsection', {'subsection': 'Outcomes'}),
        ('text', RichText('<p>Maecenas aliquam eros eu sollicitudin feugiat. Aliquam tortor enim, venenatis a pulvinar accumsan, maximus nec eros. Donec sem sapien, bibendum vitae ornare auctor, ornare eget velit. Vivamus non fermentum sem. Nulla luctus justo ultrices, venenatis sapien non, convallis libero. Mauris in dolor mollis, molestie elit dapibus, eleifend lacus. Suspendisse finibus fermentum feugiat. Nulla eget elit nec nisl bibendum tincidunt. Vestibulum varius a libero a rhoncus. In varius ex quis risus sagittis, id feugiat risus tempor. Pellentesque sed volutpat tellus. Nunc odio turpis, congue aliquam eleifend a, efficitur fringilla ligula. Nam et tempus diam. Sed dictum ante in elementum hendrerit. Cras ligula velit, rhoncus et mattis et, bibendum vel magna.</p>')),
    ],
}

SET_DATA = [MARSEILLE_SET]


class Command(BaseCommand):
    help = 'Create the DALME public site tree.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home = None
        self.features = None
        self.collections = None
        self.sets = None

    def create_corpora(self):
        marseille = Set.objects.first()
        Corpus.objects.create(
            sets=[marseille], page_id=self.collections.pk, **CORPUS_DATA
        )

    def create_set_pages(self):
        for data in SET_DATA:
            self.collections.add_child(instance=Set(**data))

    def create_collections_page(self):
        self.collections = self.home.add_child(
            instance=Collections(**COLLECTIONS_DATA)
        )

    def create_feature_pages(self):
        source_id = FEATURED_OBJECT_DATA.pop('source_id')
        instance = FeaturedObject(
            source=Source.objects.get(pk=source_id),
            **FEATURED_OBJECT_DATA
        )
        self.features.add_child(instance=instance)

        source_id = FEATURED_INVENTORY_DATA.pop('source_id')
        instance = FeaturedInventory(
            source=Source.objects.get(pk=source_id),
            **FEATURED_INVENTORY_DATA
        )
        self.features.add_child(instance=instance)

        self.features.add_child(instance=Essay(**ESSAY_DATA))

    def create_features_page(self):
        self.features = self.home.add_child(instance=Features(**FEATURES_DATA))

    def create_about_section(self):
        section = self.home.add_child(instance=Section(**ABOUT_DATA))
        for flat_data in ABOUT_FLAT_DATA:
            section.add_child(instance=Flat(**flat_data))

    def create_project_section(self):
        section = self.home.add_child(instance=Section(**PROJECT_DATA))
        for flat_data in PROJECT_FLAT_DATA:
            section.add_child(instance=Flat(**flat_data))

    def create_home(self):
        try:
            Site.objects.first().delete()
            Page.objects.last().delete()
        except AttributeError:
            pass

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
        self.create_project_section()
        self.create_features_page()
        self.create_feature_pages()
        self.create_collections_page()
        self.create_set_pages()
        self.create_corpora()
        self.create_about_section()

        for page in Page.objects.all():
            if not page.is_root():
                page.specific.save_revision().publish()

        # TODO: Remove this!
        user = User.objects.get(username='jhrr')
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Created DALME'))
