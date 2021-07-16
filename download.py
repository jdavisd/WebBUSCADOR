from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON
endpoint = 'http://dbpedia.org/sparql'
wrapper = SPARQLWrapper(endpoint)
wrapper.setQuery('''
       CONSTRUCT{
        dbr:Food  dbo:wikiPageWikiLink ?wikiPageWikiLink.
        ?wikiPageWikiLink dbo:abstract ?descripcion.
        ?wikiPageWikiLink    dbp:name ?name.
        ?wikiPageWikiLink dbo:thumbnail ?imagen
       }
      WHERE{
        dbr:Food  dbo:wikiPageWikiLink ?wikiPageWikiLink.
        ?wikiPageWikiLink dbo:abstract ?descripcion.
        ?wikiPageWikiLink    dbp:name ?name.
        ?wikiPageWikiLink dbo:thumbnail ?imagen 
       }''')
wrapper.setReturnFormat(RDFXML)
qres = wrapper.query().convert()
qres.serialize("wiki2.rdf", format='ttl')
