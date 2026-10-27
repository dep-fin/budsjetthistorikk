"""Bevar O2/T1s historiske CR i tekst ved begge libxml2-parserreglene."""

import re
from html import unescape

from lxml import html


def parse_legacy_html(raw: bytes) -> html.HtmlElement:
    """Skjerm CR før parsing; originalbyte, lokatorer og ID-regler er uendret.

    Markøren er selv HTML-mellomrom, også mellom tagger/attributter og i head.
    Den finnes ikke i originalen, heller ikke etter tegnreferanseutvidelse, og
    kan ikke overlappe seg selv. Bare parserinput endres; treets tekstfelt
    tilbakestilles før tekst/HTML/hierarki og identiteter beregnes.
    """
    source = raw.decode("utf-8")
    marker = "\t" + " " * 8
    decoded = unescape(source)
    if marker in decoded:
        # Fast bredde begrenser utvidelsen også ved lange serier med mellomrom.
        width = max(8, len(decoded).bit_length())
        used = set(re.findall(rf"\t[ \n]{{{width}}}", decoded))
        alphabet = str.maketrans("01", " \n")
        for number in range(len(used) + 1):
            marker = "\t" + format(number, f"0{width}b").translate(alphabet)
            if marker not in used:
                break
    document = html.fromstring(
        source.replace("\r", marker), parser=html.HTMLParser(no_network=True)
    )
    if "\r" in source:
        for node in document.iter():
            if node.text:
                node.text = node.text.replace(marker, "\r")
            if node.tail:
                node.tail = node.tail.replace(marker, "\r")
            for key, value in node.attrib.items():
                if marker in value:
                    node.set(key, value.replace(marker, "\r"))
    return document
