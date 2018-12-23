.. include:: abbreviation.txt

.. _design-note-page:

==============
 Design Notes
==============

G-Code Parser
-------------

The RS-274 parser is generated automatically from the grammar defined in the paper |NIST-RS-274|_
(Appendix E) using the generator `PLY <https://www.dabeaz.com/ply/ply.html>`_ which implement a
LALR(1) parser similar to the tools **lex** and **yacc**.

The parser construct an `abstract syntax tree (AST)
<https://en.wikipedia.org/wiki/Abstract_syntax_tree>`_ during the parsing.

User can subclass this parser to support a derived G-code flavour.

G-code flavours
---------------

The different flavours are partly handled in |YAML|_ files.
