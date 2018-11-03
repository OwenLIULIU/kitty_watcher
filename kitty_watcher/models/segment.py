# coding=utf-8
from __future__ import absolute_import


class Segment(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.word = kwargs.get('word')
        self.head = kwargs.get('head')
        self.cpostag = kwargs.get('cpostag')
        self.postag = kwargs.get('postag')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.deprel = kwargs.get('deprel')
        self.deprel_zh = kwargs.get('deprel_zh')

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'head': self.head,
            'cpostag': self.cpostag,
            'postag': self.postag,
            'start': self.start,
            'end': self.end,
            'deprel': self.deprel,
            'deprel_zh': self.deprel_zh,
        }

    @classmethod
    def instance_to_dict(cls, x):
        if x is None:
            return None
        return x.to_dict()

    @classmethod
    def dict_to_instance(cls, d):
        if d is None:
            return None
        return cls(**d)


class Phrase(object):

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.group = kwargs.get('group')


class SegmentNode(object):

    def __init__(self, **kwargs):
        self.segment = Segment.dict_to_instance(kwargs.get('segment'))
        self.children = [SegmentNode(**c) for c in (kwargs.get('children') or [])]
        self.level = kwargs.get('level')
        self.parent = kwargs.get('parent')

    def to_dict(self):
        return {
            'segment': Segment.instance_to_dict(self.segment),
            'children': [c.to_dict() for c in self.children],
        }

    @classmethod
    def instance_to_dict(cls, x):
        if x is None:
            return None
        return x.to_dict()

    @classmethod
    def dict_to_instance(cls, d):
        if d is None:
            return None
        return cls(**d)

    @classmethod
    def load_from_dependency_list(cls, dependency_list):
        segment_nodes = cls.load_by_head_from_dependency_list(dependency_list, 0)
        if len(segment_nodes) == 0:
            return None
        root = segment_nodes[0]
        cls._mark_level_and_parent(root, 0, None)
        return root

    @classmethod
    def load_by_head_from_dependency_list(cls, dependency_list, head):
        segments_json = cls._find_by_head_from_dependency_list(dependency_list, head)
        segment_nodes = [SegmentNode(segment=s) for s in segments_json]
        for segment_node in segment_nodes:
            segment_node.children = cls.load_by_head_from_dependency_list(dependency_list, segment_node.segment.id)
        return segment_nodes

    @classmethod
    def _mark_level_and_parent(cls, node, level, parent):
        node.level = level
        node.parent = parent
        for c in node.children:
            cls._mark_level_and_parent(c, level + 1, node)

    @classmethod
    def _find_by_head_from_dependency_list(cls, dependency_list, head):
        results = []
        for s in dependency_list:
            if s.get('head') == head:
                results.append(s)
        return results

    @property
    def offsprings(self):
        results = [c for c in self.children]
        for c in self.children:
            results += c.offsprings
        return results

    @property
    def sorted_offsprings(self):
        return sorted(self.offsprings, cmp=lambda a, b: a.segment.start - b.segment.start)

    def children_continuous_groups(self):
        if len(self.children) == 0:
            return [[self]]
        offsprings_include_self = sorted(self.offsprings + [self], cmp=lambda a, b: a.segment.start - b.segment.start)
        groups = []
        current_group = None

        for child in offsprings_include_self:
            if current_group is None:
                current_group = [child]
                continue
            if current_group[-1].segment.end == child.segment.start:
                current_group.append(child)
                continue
            groups.append(current_group)
            current_group = [child]
        if current_group is not None:
            groups.append(current_group)
        return groups

    @classmethod
    def children_continuous_relative_groups(cls, node):
        groups = node.children_continuous_groups()
        group_contains_self = None
        self_index = -1
        for group in groups:
            if node in group:
                group_contains_self = group
                self_index = group_contains_self.index(node)
                break
        if group_contains_self is None:
            return []
        results = []
        for left_index in range(0, self_index + 1):
            for right_index in range(self_index + 1, len(group_contains_self) + 1):
                if cls._is_group_relative_to_node(node, group_contains_self[left_index: right_index]):
                    results.append(group_contains_self[left_index: right_index])
        return results

    @classmethod
    def _is_group_relative_to_node(cls, node, group):
        for current in group:
            if current == node:
                continue
            if current.level <= node.level:
                return False
            current = current.parent
            while current is not None and current.level >= node.level:
                if current not in group and not current == node:
                    return False
                current = current.parent
        return True

    @classmethod
    def children_continuous_relative_texts(cls, node):
        groups = cls.children_continuous_relative_groups(node)
        results = [{
            'text': u''.join([sn.segment.word for sn in group]),
            'start': group[0].segment.start,
            'end': group[-1].segment.end,
            'group': group,
       } for group in groups]
        return results

    @classmethod
    def all_possible_continuous_semantic_substrings(cls, node):
        results = cls.children_continuous_relative_texts(node)
        for child in node.children:
            results += cls.all_possible_continuous_semantic_substrings(child)
        seen = []
        unique_results = []
        for r in results:
            if (r.get('start'), r.get('end')) in seen:
                continue
            unique_results.append(r)
            seen.append((r.get('start'), r.get('end')))
        sorted_results = sorted(
            unique_results,
            cmp=lambda a, b: (b.get('end') - b.get('start')) - (a.get('end') - a.get('start')),
        )
        return sorted_results

    @classmethod
    def all_possible_substrings(cls, segs):
        if len(segs) == 0 or segs is None:
            return []
        seg_len = len(segs)
        substrings = []
        for index, seg in enumerate(segs):
            substring = seg.get('word')
            for i in range(index+1, seg_len):
                substrings.append({'text': substring, 'start': seg.get('start'), 'end': seg.get('end')})
                substring += segs[i].get('word')
                substrings.append({'text': substring, 'start': seg.get('start'), 'end': segs[i].get('end')})
        last_seg = segs[len(segs) - 1]
        substrings.append({'text': last_seg.get('word'), 'start': last_seg.get('start'), 'end': last_seg.get('end')})
        return substrings

    @property
    def string(self):
        return u'[{} {} {} >{} {} {}]'.format(
            self.segment.id,
            self.segment.word,
            self.segment.postag,
            self.segment.head,
            self.segment.deprel,
            self.segment.deprel_zh,
        )

    @property
    def string_length(self):
        return len(self.string) + len(self.segment.word) + len(self.segment.deprel_zh)

    @classmethod
    def print_tree(cls, current_node, indent=u'', last=u'updown'):
        nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
        size_branch = {child: nb_children(child) for child in current_node.children}

        """ Creation of balanced lists for "up" branch and "down" branch. """
        up = sorted(current_node.children, key=lambda node: nb_children(node))
        down = []
        while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
            down.append(up.pop())

        """ Printing of "up" branch. """
        for child in up:
            next_last = u'up' if up.index(child) is 0 else u''
            next_indent = u'{0}{1}{2}'.format(
                indent,
                u' ' if u'up' in last else u'│',
                u' ' * current_node.string_length,
            )
            cls.print_tree(child, indent=next_indent, last=next_last)

        """ Printing of current node. """
        if last == u'up': start_shape = u'┌'
        elif last == u'down': start_shape = u'└'
        elif last == u'updown': start_shape = u' '
        else: start_shape = u'├'

        if up: end_shape = u'┤'
        elif down: end_shape = u'┐'
        else: end_shape = u''

        # print u'{0}{1}{2}{3}'.format(indent, start_shape, current_node.string, end_shape)

        """ Printing of "down" branch. """
        for child in down:
            next_last = u'down' if down.index(child) is len(down) - 1 else u''
            next_indent = u'{0}{1}{2}'.format(
                indent,
                u' ' if u'down' in last else u'│',
                u' ' * current_node.string_length,
            )
            cls.print_tree(child, indent=next_indent, last=next_last)
