# coding=utf-8
from __future__ import absolute_import

import itertools

from kitty_watcher.gateways.cia import CIAGateway
from kitty_watcher.models.segment import Phrase, SegmentNode
from kitty_watcher.models.match import Match

PRIVILEGED_PEOPLE = [u'信']


class AnalyzeService(object):

    @classmethod
    def analyze(cls, message, analysis):
        if not message.type == 'text':
            return []

        text = message.data.get('text')
        phrases = cls.get_all_phrases(text)
        filtered_phrases = cls.filter_phrases(phrases)

        matches = []
        matched_persons = cls.find_names_in_cia(filtered_phrases)

        if len(matched_persons) == 0:
            return []

        for matched_person in matched_persons:
            for phrase in filtered_phrases:
                if phrase.text == matched_person.get('name'):
                    matches.append(make_match_by_person_and_phrase(matched_person, phrase, 'name'))
                    continue

                if phrase.text in matched_person.get('aliases'):
                    matches.append(make_match_by_person_and_phrase(matched_person, phrase, 'alias'))
                    continue

                if phrase.text == matched_person.get('zi'):
                    matches.append(make_match_by_person_and_phrase(matched_person, phrase, 'zi'))
                    continue

                if isinstance(matched_person.get('hao'), list) and phrase.text in matched_person.get('hao'):
                    matches.append(make_match_by_person_and_phrase(matched_person, phrase, 'hao'))

        if len(matches) == 0:
            return []
        return [m.to_dict() for m in matches]

    @classmethod
    def find_names_in_cia(cls, phrases):
        words = [phrase.text for phrase in phrases]
        matched_persons, error = CIAGateway.entity_query(
            'people', {'$or': [
                {'name': {'$in': words}}, 
                {'aliases': {'$elemMatch': {'$in': words}}},
                {'zi': {'$in': words}},
                {'hao': {'$elemMatch': {'$in': words}}}
            ]}, 0, 30
        )
        if len(matched_persons) == 0 or matched_persons is None:
            return []

        return matched_persons

    @classmethod
    def filter_phrases(cls, phrases):
        filtered_phrases = [
            phrase for phrase in phrases if 11 > len(phrase.text) > 1 or
            phrase.text in PRIVILEGED_PEOPLE
            ]

        if len(filtered_phrases) > 200:
            filtered_phrases = [
                phrase for phrase in filtered_phrases if len(phrase.text) < 10 or
                phrase.text in PRIVILEGED_PEOPLE
            ]
        if len(filtered_phrases) > 200:
            filtered_phrases = [
                phrase for phrase in filtered_phrases if len(phrase.text) < 9 or
                phrase.text in PRIVILEGED_PEOPLE
            ]
        if len(filtered_phrases) > 200:
            filtered_phrases = [
                phrase for phrase in filtered_phrases if len(phrase.text) < 8 or
                phrase.text in PRIVILEGED_PEOPLE
            ]
        if len(filtered_phrases) > 200:
            filtered_phrases = filtered_phrases[:200]

        return filtered_phrases

    @classmethod
    def get_all_phrases(cls, string):
        phrase_list = []
        for i, j in itertools.combinations(xrange(len(string) + 1), 2):
            if j - i > 20:
                continue
            phrase_list.append(Phrase(text=string[i:j], start=i, end=j))
        return phrase_list


def make_match_by_person_and_phrase(person, phrase, subtype):
    # 需要改成entity, class, mode字段的格式, 但是使用people分析结果的服务有点多, 需要找时间统一修改
    return Match(
        type='people',
        subtype=subtype,
        word=phrase.text,
        start=phrase.start,
        end=phrase.end,
        data={
            'uuid': person.get('uuid'),
            'name': person.get('name'),
            'aliases': person.get('aliases'),
            'roles': person.get('roles'),
            'gender': person.get('gender'),
            'nationalities': person.get('nationalities'),
            'introduction': person.get('introduction'),
            'birthday': person.get('birthday'),
            'dynasty': person.get('dynasty'),
        }
    )
