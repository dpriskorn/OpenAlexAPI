from unittest import TestCase

# from rich import print

from openalexapi import OpenAlex, Work, Author


class TestOpenAlex(TestCase):
    def test_get_single_work(self):
        oa = OpenAlex()
        work = oa.get_single_entity("W2741809807", "works/")
        # print(work.dict())
        if not isinstance(work, Work):
            self.fail()

    def test_get_single_work_via_doi_namespace(self):
        oa = OpenAlex()
        work = oa.get_single_entity("doi:10.7717/peerj.4375", "works/")
        # print(work.dict())
        if not isinstance(work, Work):
            self.fail()

    def test_get_single_author(self):
        oa = OpenAlex()
        author = oa.get_single_entity("A2479313101", "authors/")
        # print(author.dict())
        if not isinstance(author, Author):
            self.fail()

    # def test_get_single_work_via_pmid_namespace(self):
    #     oa = OpenAlex()
    #     work = oa.get_single_work("pmid:29456894")
    #     print(work.dict())
    #     if not isinstance(work, Work):
    #         self.fail()
