# BetaWriter (2019) document clustering

This repository contains an excerpt of the <i>prototype implementation of <b>Beta Writer</b></i>, the algorithmic author of [the first machine-generated research book published by Springer Nature](https://link.springer.com/book/10.1007/978-3-030-16800-1), developed by [Niko Schenk](https://www.english-linguistics.de/nschenk/), [Samuel Rönnqvist](https://github.com/sronnqvist) and other members of the Applied Computational Linguistics Lab. The original 2019 version of this data has been published under [https://github.com/acoli-repo/book-gen](https://github.com/acoli-repo/book-gen).

This project is open source software and released under the [MIT license](https://opensource.org/licenses/MIT).

For more implementational details, please refer to our [system pipeline description in Section 2.3.](https://link.springer.com/content/pdf/bfm%3A978-3-030-16800-1%2F1.pdf).

The scripts for the major text processing tasks in the publicly released Beta Writer (2019) system include:

* Book structure generation (<code>mkstructure_html.py</code>) and visualization (<code>plot.py</code>)

This implements a simple clustering based on cosine similarity between full texts.
