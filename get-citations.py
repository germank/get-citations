#!/usr/bin/env python

#NB: If there is some error on retrieving the publication year,
# scholarly.py:191 should be patched with
# self.bib['year'] = arrow.get(val.text, ['YYYY/M','YYYY/MM/DD', 'YYYY', 'YYYY/M/DD', 'YYYY/M/D', 'YYYY/MM/D']).year 
import scholarly

import arrow
import nltk
from nltk.corpus import stopwords
import argparse
english_stopwords = set(stopwords.words('english'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('author_name', help='Your name')
    ap.add_argument('-o', '--output', default='citations.tex',
            help='Tex filename to store auto-generated commands')
    args = ap.parse_args()
    print('Retrieving data...')
    author = get_author_by_name(args.author_name)
    print('Writing results...')
    publications_citations = get_publications_citations(author)
    write_tex(args.output, author, publications_citations)

def get_author_by_name(author_name):
    authors = scholarly.search_author(author_name)
    author = next(authors).fill()
    assert author.name == author_name, f"{author.name} does not match {author_name}"
    return author

def get_publications_citations(author):
    publications = author.publications
    citations = {}
    for pub in publications:
        try:
            year = pub.bib["year"]
            key = get_publication_keyword(pub, citations)
            try:
                val = pub.citedby # citation count
                id_scholarcitedby = pub.id_scholarcitedby[0] # id of Google Scholar webpage with citations list
            except AttributeError:
                print(f'Cannot retrieve citations count for "{pub.bib["title"]}"')
                #print(pub)
                continue
            citations[key] = {'num_cit': val, 'id_scholarcitedby': 
                    id_scholarcitedby}
        except arrow.parser.ParserError:
            print("Couldn't fill", pub.bib)
    return citations

def get_publication_keyword(pub, keywords):
    alphabetical_title = remove_symbols(pub.bib['title'])
    title_words = (w.lower() for w in alphabetical_title.split()
            if w.lower() not in english_stopwords)
    first_word = next(title_words)
    key = f'{first_word}'
    while key in keywords:
        try:
            next_word = next(title_words)
        except StopIteration:
            raise RuntimeError(f"Couldn't find unique id for {pub.bib['title']}")
        key = 'f{key}{second_word}'
    return key

def remove_symbols(x):
    symbols = "’'-!?:,"
    for s in symbols:
        x = x.replace(s, ' ')
    return x

def write_tex(output_filename, author, citations):
    with open(output_filename, 'w') as f:
        write_generic_command(f, 'cittotal', author.citedby)
        write_generic_command(f, 'cithindex', author.hindex)
        for kcit, vcit in citations.items():
            write_generic_command(f, f'cit{kcit}', vcit['num_cit'])
            write_render_citations_command(f, f'fullcit{kcit}', vcit['num_cit'], vcit['id_scholarcitedby'])

def write_generic_command(f, name, value):
    f.write(f'\\newcommand{{\\{name}}}{{{value}}}\n')

def write_render_citations_command(f, name, ncit, id_scholarcitedby):
    f.write(f'\\newcommand{{\\{name}}}{{\\href{{https://scholar.google.com/scholar?cites={id_scholarcitedby}}}{{Cit. {ncit}}}}}\n')

if __name__ == '__main__':
    main()
