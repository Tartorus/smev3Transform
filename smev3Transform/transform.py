import re
from lxml.etree import fromstring, tostring, Element, _Comment, SubElement

TEXT = re.compile(r'[\w\d]')
NAMESPACE = re.compile(r'^\{(.*)\}')


class Smev3Transform:
    """Класс транформации xml элементов согласно методоческим рекомендациям."""

    def __init__(self, xml):
        """:param xml :type _Element / bytes / string"""
        if isinstance(xml, str):
            xml = xml.encode()
        xml = fromstring(xml)

        self.xml = xml
        self.ns_num = 1
        self.element_id = 1
        self.attrib_map = dict()

    def get_ns(self, uri, prefix_map):
        """Формирование нового namespace.
        :param uri :type str
        :param prefix_map :type dict
        :return str"""
        ns = 'ns%s' % self.ns_num
        self.ns_num += 1
        prefix_map[uri] = ns
        return ns

    def fake_attrib(self, attrib, prefix_map):
        """ Создание "ложного" атрибута, для дальнейшей его подмена на настоящие атрибуты и namespaces.
        :param attrib :type dict
        :param prefix_map :type dict"""
        attrib = self.sort_attrib(attrib, prefix_map)

        if attrib:
            fake_attrib = dict(fake='id_%s' % self.element_id)
            str_fake = '%s="%s"' % tuple(*fake_attrib.items())
            self.element_id += 1
            self.attrib_map[str_fake] = attrib
        else:
            fake_attrib = dict()
        return fake_attrib

    def transform(self, element, prefix_map=None, parent=None):
        """Рекурсивная трансформация элементов.
        :param element :type lxml.Element
        :param prefix_map :type dict - мап namespaces
        :return новый сконструированный lxml.Element"""
        if prefix_map is None:
            prefix_map = dict()

        uri = element.nsmap[element.prefix]
        ns = prefix_map.get(uri)

        if ns is None:
            ns = self.get_ns(uri, prefix_map)
        ns_map = {ns: uri}

        fake_attrib = self.fake_attrib(element.attrib, prefix_map)
        if parent is not None:
            new_element = SubElement(parent, element.tag, attrib=fake_attrib, nsmap=ns_map)
        else:
            new_element = Element(element.tag, attrib=fake_attrib, nsmap=ns_map)

        children = element.getchildren()
        if children:
            for child in element.getchildren():
                if not isinstance(child, _Comment):
                    self.transform(child, dict(prefix_map), parent=new_element)
        else:
            if element.text and TEXT.findall(element.text):
                new_element.text = element.text

        return new_element

    def sort_attrib(self, attrib, prefix_map):
        """Сортировака атрибутов и namespaces.
        :param attrib :type dict
        :param prefix_map :type dict
        :return str"""

        l1 = []
        l2 = []
        result = []

        # разделям атрибуты с namespace и без
        for k, v in attrib.items():
            uri = NAMESPACE.search(k)
            if uri:
                uri = uri.group(1)
                attr = NAMESPACE.sub('', k)
                l1.append((uri, attr, v))
            else:
                l2.append((k, v))

        # сортируем атрибуты с namespace по локальному названию
        l1.sort(key=lambda x: (x[0], x[1]))

        l3 = []
        for uri, attr, v in l1:
            ns = prefix_map.get(uri)
            if ns is None:
                ns = self.get_ns(uri, prefix_map)
                result.append('xmlns:%s="%s"' % (ns, uri))
            # "собираем" атрибут
            l3.append(('%s:%s' % (ns, attr), v))

        l2.sort(key=lambda x: x[0])
        l3.extend(l2)

        for k, v in l3:
            result.append('%s="%s"' % (k, v))
        return ' '.join(result)

    def run(self):
        xml = tostring(self.transform(self.xml), method='c14n', exclusive=True,  with_comments=False).decode()
        for k, v in self.attrib_map.items():
            xml = xml.replace(k, v)
        return xml
