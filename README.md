# smev3Transform

transform.Smev3Transform - класс транформации xml элементов согласно методоческим рекомендациям СМЭВ3.

## example

```python
xml = """
<elementOne xmlns="http://test/1">
	<qwe:elementTwo xmlns:qwe="http://test/2">asd</qwe:elementTwo>  
</elementOne>"""
Smev3Transform(xml).run()  
```

Результат:  
<ns1:elementOne xmlns:ns1="http://test/1"><ns2:elementTwo xmlns:ns2="http://test/2"><ns3:elementThree xmlns:ns3="http://test/3"><ns1:elementFour> z x c </ns1:elementFour><ns2:elementFive> w w w </ns2:elementFive></ns3:elementThree><ns4:elementSix xmlns:ns4="http://test/3">eee</ns4:elementSix></ns2:elementTwo></ns1:elementOne>
