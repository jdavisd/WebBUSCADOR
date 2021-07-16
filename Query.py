from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, RDFXML, JSON

class Busqueda:


    def __init__(self, entrada, idioma):
        self.entrada = entrada.replace(" ", "_")
        self.idioma = idioma

    def consulta(self):
        #print("dshdsdhdsj     ",os.getcwd())
        g = Graph()
        g.parse('wiki2.rdf', format='ttl')
        qres = g.query(
            """SELECT ?abstract ?thumbnail
            WHERE{
            ?x dbp:name '"""+self.entrada+"""'@en;
            dbo:abstract ?abstract .
            ?x dbp:name '"""+self.entrada+"""'@en;
            dbo:thumbnail ?thumbnail.
            FILTER (langMatches(lang(?abstract),'"""+self.idioma+"""')
            )
            }""")
        result=""
        imagen=""
        for s in qres:
           result = s.abstract
           imagen = s.thumbnail
        if(not result):
           result = "No se encontro la busqueda"
        arreglo = [result,imagen]  
        return arreglo

    def consultaConectado(self):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
        SELECT  ?descripcion ?imagen 
            WHERE{
            dbr:Food  dbo:wikiPageWikiLink ?wikiPageWikiLink.
            ?wikiPageWikiLink dbo:abstract ?descripcion.
            ?wikiPageWikiLink    dbp:name '"""+self.entrada+"""'@en.
            ?wikiPageWikiLink dbo:thumbnail ?imagen 
            FILTER (langMatches(lang(?descripcion),'"""+self.idioma+"""'))
           }

        """)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        descripcion = ""
        imagen = ""
        for result in results["results"]["bindings"]:
            descripcion = result["descripcion"]["value"] 
            imagen = result["imagen"]["value"]   
        if(not descripcion):
            # consulta()
            descripcion = "No se encontro la busqueda"
            imagen = "https://icon-library.com/images/default-profile-icon/default-profile-icon-17.jpg"
        arreglo = [descripcion,imagen]

        return arreglo
    def download(self):
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
      qres=wrapper.query().convert()
      qres.serialize("wiki2.rdf", format='ttl')

    


