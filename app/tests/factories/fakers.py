"""Fake data in the shape of DALME's corpus.

The locales and their weights follow the places DALME's records come from
(#87 records the corpus profile they were read from). Faker has no Catalan and
no Latin names, so `DalmeProvider` adds those, with the folios, archival
references and record titles the corpus uses. Every value is invented in the
corpus's style; nothing is copied from it.

One generator serves every factory. pytest-randomly reseeds it for each run.

"""

from collections import OrderedDict

from faker import Faker
from faker.providers import BaseProvider

LOCALES = OrderedDict(
    [
        ('it_IT', 0.73),
        ('fr_FR', 0.13),
        ('es_ES', 0.05),
        ('en_GB', 0.02),
        ('en_IE', 0.02),
        ('de_CH', 0.02),
        ('de_DE', 0.01),
        ('de_AT', 0.01),
        ('nl_NL', 0.01),
    ]
)

LATIN_GIVEN_NAMES = (
    'Andreas', 'Antonius', 'Bartholomeus', 'Benedictus', 'Bernardus', 'Bonaventura',
    'Franciscus', 'Guillelmus', 'Jacobus', 'Johannes', 'Laurentius', 'Matheus',
    'Nicolaus', 'Petrus', 'Raimundus', 'Ugolinus', 'Agnes', 'Beatrix', 'Caterina',
    'Clara', 'Francisca', 'Guillelma', 'Johanna', 'Margarita',
)  # fmt: skip
LATIN_FAMILY_NAMES = (
    'Albertini', 'Benincase', 'Bonaccursi', 'Ceccharelli', 'Ferrarii', 'Guidonis',
    'Lanfranchi', 'Martini', 'Orlandi', 'Puccinelli', 'Rainerii', 'Ugolini',
)  # fmt: skip
CATALAN_GIVEN_NAMES = (
    'Antoni', 'Bernat', 'Francesc', 'Guillem', 'Jaume', 'Joan', 'Pere', 'Ramon',
    'Agnès', 'Caterina', 'Elionor', 'Margarida',
)  # fmt: skip
CATALAN_FAMILY_NAMES = (
    'Ferrer', 'Font', 'Puig', 'Pujol', 'Roca', 'Serra', 'Soler', 'Vidal', 'Català', 'Garcés',
)  # fmt: skip
ARCHIVES = ('AHCB', 'AHPB', 'ADBR', 'ADHG', 'ASF', 'ASLu', 'ASPi', 'ASSi', 'BHSA', 'StABS')
OFFICES = (
    'Podestà di Pisa', 'Podestà di Siena', 'Curia del Maleficio', 'Curia dei Consoli',
    'Notarile antecosimiano', 'Corte dei Mercanti',
)  # fmt: skip


class DalmeProvider(BaseProvider):
    """Generate names, references and titles in the corpus's style."""

    def latin_name(self):
        """Return a name in the Latin forms of the notarial record."""
        return f'{self.random_element(LATIN_GIVEN_NAMES)} {self.random_element(LATIN_FAMILY_NAMES)}'

    def catalan_name(self):
        """Return a Catalan personal name."""
        return f'{self.random_element(CATALAN_GIVEN_NAMES)} {self.random_element(CATALAN_FAMILY_NAMES)}'

    def historical_name(self):
        """Return a personal name as the corpus mixes them: mostly Latin, some vernacular."""
        return self.random_element(
            OrderedDict(
                [
                    (self.latin_name(), 0.5),
                    (self.catalan_name(), 0.1),
                    (self.generator.name(), 0.4),
                ]
            )
        )

    def folio(self):
        """Return a folio, or a run of folios, such as `70r` or `138v-139r`."""
        leaf = self.random_int(1, 400)
        if self.random_int(0, 3):
            return f'{leaf}{self.random_element("rv")}'
        return f'{leaf}v-{leaf + 1}r'

    def archival_reference(self):
        """Return an archive's reference, such as `AHPB 56/79`."""
        return f'{self.random_element(ARCHIVES)} {self.random_int(1, 400)}/{self.random_int(1, 200)}'

    def record_title(self):
        """Return a record title in one of the corpus's patterns."""
        name = self.historical_name()
        return self.random_element(
            [
                f'Inventory of {name} ({self.archival_reference()})',
                f'Inventory of the goods of {name} ({self.archival_reference()})',
                f'Act {self.random_int(1, 3000)}, {self.random_element(OFFICES)} '
                f'{self.random_int(1, 120)}, {self.folio()}',
            ]
        )


fake = Faker(LOCALES)
# The multi-locale proxy does not forward `add_provider`, so each locale's
# generator gets the provider itself.
for generator in fake.factories:
    generator.add_provider(DalmeProvider)
