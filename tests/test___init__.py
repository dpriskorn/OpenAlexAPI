from unittest import TestCase

from rich import print

from openalexapi import OpenAlex, Work


class TestOpenAlex(TestCase):
    def test_get_work(self):
        oa = OpenAlex()
        work = oa.get_work("W2741809807")
        print(work.dict())
        if not isinstance(work, Work):
            self.fail()
