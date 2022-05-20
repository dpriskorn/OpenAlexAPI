"""
Copyright 2022 Dennis Priskorn
"""
import unittest
from unittest import TestCase

# from rich import print

from openalexapi import OpenAlex, Work


class TestOpenAlex(TestCase):
    def test_get_single_work(self):
        oa = OpenAlex()
        work = oa.get_single_work("W2741809807")
        # print(work.dict())
        if not isinstance(work, Work):
            self.fail()

    def test_get_single_work_via_doi_namespace(self):
        oa = OpenAlex()
        work = oa.get_single_work("doi:10.7717/peerj.4375")
        # print(work.dict())
        if not isinstance(work, Work):
            self.fail()

    # def test_get_single_work_via_pmid_namespace(self):
    #     oa = OpenAlex()
    #     work = oa.get_single_work("pmid:29456894")
    #     print(work.dict())
    #     if not isinstance(work, Work):
    #         self.fail()

    def test_get_multiple_works(self):
        oa = OpenAlex()
        ids = [
            "W1492510670", 
            "https://openalex.org/W2899283552", 
            "https://openalex.org/W2565233142", 
            "W3135266120"
        ]
        works = oa.get_multiple_works(ids)
        self.assertEqual(len(works), 4)
        for w in works:
            self.assertIsInstance(w, Work)

    def test_get_related_works(self):
        oa = OpenAlex()
        works = oa.get_related_works(oa.get_single_work("W3135266120"))
        self.assertEqual(len(works), 20)
        for w in works:
            self.assertIsInstance(w, Work)

    def test_get_referenced_works(self):
        oa = OpenAlex()
        works = oa.get_referenced_works(oa.get_single_work("W3135266120"))
        self.assertEqual(len(works), 29)
        for w in works:
            self.assertIsInstance(w, Work)

    def test_get_cited_by_works(self):
        oa = OpenAlex()
        works = oa.get_cited_by_works(oa.get_single_work("W2899283552"), limit=500)
        self.assertEqual(len(works), 500)
        for w in works:
            self.assertIsInstance(w, Work)


if __name__ == "__main__":
    unittest.main()