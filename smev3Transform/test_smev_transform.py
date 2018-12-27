from unittest.case import TestCase
from smev3Transform.transform import Smev3Transform


class TestTransform(TestCase):
    maxDiff = None

    def test_1(self):
        """Сценарий 1: тестирование правил 1, 2, 6"""
        in_data = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Тестирование правил 1, 2, 6:
	- XML declaration выше, этот комментарий, и следующая за ним processing instruction должны быть вырезаны;
	- Переводы строки должны быть удалены;
	- Namespace prefixes заменяются на автоматически сгенерированные.
-->
<?xml-stylesheet type="text/xsl" href="style.xsl"?>

<elementOne xmlns="http://test/1">
	<qwe:elementTwo xmlns:qwe="http://test/2">asd</qwe:elementTwo>
</elementOne>"""
        expected = """<ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2">asd</ns2:elementTwo></ns1:elementOne>"""
        result = Smev3Transform(in_data).run()
        self.assertEqual(expected, result)

    def test_2(self):
        """Сценарий 2: тестирование правил 4, 5"""
        in_data = """<?xml version="1.0" encoding="UTF-8"?>
<!--
	Всё то же, что в test case 1, плюс правила 4 и 5:
	- Удалить namespace prefix, которые на текущем уровне объявляются, но не используются.
	- Проверить, что namespace текущего элемента объявлен либо выше по дереву, либо в текущем элементе. Если не объявлен, объявить в текущем элементе
-->
<?xml-stylesheet type="text/xsl" href="style.xsl"?>

<elementOne xmlns="http://test/1" xmlns:qwe="http://test/2" xmlns:asd="http://test/3">
	<qwe:elementTwo>
		<asd:elementThree>
			<!-- Проверка обработки default namespace. -->
			<elementFour> z x c </elementFour>
			<!-- Тестирование ситуации, когда для одного namespace объявляется несколько префиксов во вложенных элементах. -->
			<qqq:elementFive xmlns:qqq="http://test/2"> w w w </qqq:elementFive>
		</asd:elementThree>
		<!-- Ситуация, когда prefix был объявлен выше, чем должно быть в нормальной форме,
		при нормализации переносится ниже, и это приводит к генерации нескольких префиксов
		для одного namespace в sibling элементах. -->
		<asd:elementSix>eee</asd:elementSix>
	</qwe:elementTwo>
</elementOne> """
        expected = """<ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2"><ns3:elementThree xmlns:ns3="http://test/3"><ns1:elementFour> z x c </ns1:elementFour><ns2:elementFive> w w w </ns2:elementFive></ns3:elementThree><ns4:elementSix xmlns:ns4="http://test/3">eee</ns4:elementSix></ns2:elementTwo></ns1:elementOne>"""
        result = Smev3Transform(in_data).run()
        self.assertEqual(expected, result)

    def test_3(self):
        in_data = """<?xml version="1.0" encoding="UTF-8"?>
<!--
	Всё то же, что в test case 1, плюс правила 3, 7 и 8:
	- Атрибуты должны быть отсортированы в алфавитном порядке: сначала по namespace URI (если атрибут - в qualified form), затем – по local name.
		Атрибуты в unqualified form после сортировки идут после атрибутов в qualified form.
	- Объявления namespace prefix должны находиться перед атрибутами. Объявления префиксов должны быть отсортированы в порядке объявления, а именно:
		a.	Первым объявляется префикс пространства имен элемента, если он не был объявлен выше по дереву.
		b.	Дальше объявляются префиксы пространств имен атрибутов, если они требуются.
			Порядок этих объявлений соответствует порядку атрибутов, отсортированных в алфавитном порядке (см. п.5).
-->
<?xml-stylesheet type="text/xsl" href="style.xsl"?>

<elementOne xmlns="http://test/1" xmlns:qwe="http://test/2" xmlns:asd="http://test/3">
	<qwe:elementTwo>
		<asd:elementThree xmlns:wer="http://test/a" xmlns:zxc="http://test/0" wer:attZ="zzz" attB="bbb" attA="aaa" zxc:attC="ccc" asd:attD="ddd" asd:attE="eee" qwe:attF="fff"/>
	</qwe:elementTwo>
</elementOne>"""
        expected = """<ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2"><ns3:elementThree xmlns:ns3="http://test/3" xmlns:ns4="http://test/0" xmlns:ns5="http://test/a" ns4:attC="ccc" ns2:attF="fff" ns3:attD="ddd" ns3:attE="eee" ns5:attZ="zzz" attA="aaa" attB="bbb"></ns3:elementThree></ns2:elementTwo></ns1:elementOne>"""
        result = Smev3Transform(in_data).run()
        self.assertEqual(expected, result)

    def test_4(self):
        in_data = """<ns2:SenderProvidedRequestData xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.0" Id="SIGNED_BY_CONSUMER">
 <MessagePrimaryContent xmlns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.0">
 <SomeRequest:SomeRequest xmlns:SomeRequest="urn://x-artifacts-it-ru/vs/smev/test/test-business-data/1.0">
 <x xmlns="urn://x-artifacts-it-ru/vs/smev/test/test-business-data/1.0">qweqwe</x>
 </SomeRequest:SomeRequest>
 </MessagePrimaryContent>
</ns2:SenderProvidedRequestData>"""
        expected = """<ns1:SenderProvidedRequestData xmlns:ns1="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.0" Id="SIGNED_BY_CONSUMER"><ns2:MessagePrimaryContent xmlns:ns2="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.0"><ns3:SomeRequest xmlns:ns3="urn://x-artifacts-it-ru/vs/smev/test/test-business-data/1.0"><ns3:x>qweqwe</ns3:x></ns3:SomeRequest></ns2:MessagePrimaryContent></ns1:SenderProvidedRequestData>"""
        result = Smev3Transform(in_data).run()
        self.assertEqual(expected, result)
