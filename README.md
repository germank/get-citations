# get-citations

A script to scrap from Google Scholar the number of citations for each one
of your publications, and generating a LaTeX command for each of them
that you can later insert in your LaTeX publication list.

By default, for each publication it generates two LaTeX commands that expand
either to the raw number of citations, or to a short text description with a
link to the Google Scholar page listing all the corresponding papers that cite
that work.

## Installation

Install required libraries `nltk` and `scholarly` (note that the version in pip
of scholarly doesn't work, so I am using an alternative source), as follows:

`pip install -r requirements.txt`


Then, download the `stopwords` corpus for `nltk` as follows:

`python -c 'import nltk; nltk.download("stopwords")'`


## Usage

Simply run `python get-citations.py <your_name> -o citations.tex` and the
`citations.tex` file will get populated with the following LaTeX commands:

* `\cittotal` expands to your total number of citations.
* `\cithindex` expands to your h-index.
* `\cit<keyword>` expands to the number of citations corresponding to the publication identified by `keyword`, which is the first content word in the title that has not been used before.
* `\fullcit<keyword>` expands to a rendered text corresponding to the publication identified by `keyword`. By default, this has the form "Cit. num_citations" and
it's linked to the Google Scholar page that list all the papers citing this corresponding work.

To change how keywords are selected, you can change the `get_publication_keyword` function. To change the behaviour of the `\fullcit<keyword>` command you can modify the 
`write_render_citations_command` method.

## Random

One immediately obvious modification of this script would allow to generate
the publication list automatically. This was not my intention because I wanted
to have some control on the formatting. However, if you are interested
in having that behaviour, you are of course welcome to adapt it to your needs!
