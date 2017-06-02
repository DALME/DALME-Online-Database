from django.test import TestCase

from .models import PlatonicConcept, Relationship

class LandingPageTests(TestCase):
    def test_landing_page_empty(self):
        """
        Makes sure that landing page works with no entries, shows something sensible.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are currently no Platonic Concepts')
        self.assertContains(response, 'There are currently no Relationships between Platonic Concepts')
    def test_landing_page_only_concepts(self):
        """
        Make sure landing page displays properly when only Platonic Concepts are present.
        """
        PlatonicConcept.objects.create(term='Red')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Red')
        self.assertContains(response, 'There are currently no Relationships between Platonic Concepts')
        self.assertNotContains(response, 'There are currently no Platonic Concepts')
    def test_landing_page_concepts_and_relationships(self):
        """
        Make sure that Relationships are displayed on the home page when they exist.
        """
        red = PlatonicConcept(term='Red')
        red.save()
        darkRed = PlatonicConcept(term='Dark Red')
        darkRed.save()
        Relationship.objects.create(source=red, target=darkRed, relationship='Narrower term')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Red - Narrower term -&gt; Dark Red')
        self.assertNotContains(response, 'There are currently no Platonic Concepts')
        self.assertNotContains(response, 'There are currently no Relationships between Platonic Concepts')

class PlatonicConceptTest(TestCase):
    def test_create_concept(self):
        """
        Make sure that Platonic Concepts can be successfully created.
        """
        red = PlatonicConcept(term='Red')
        red.save()
        self.assertEqual(red.term, 'Red')
        self.assertTrue(red.creation_timestamp != None)
        self.assertTrue(red.modification_timestamp != None)
