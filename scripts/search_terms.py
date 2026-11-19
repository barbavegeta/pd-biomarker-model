"""Ontology search tool for the mapping agent (and for curators).

    python search_terms.py search "neurofilament light" --in loinc,ncit
    python search_terms.py show LOINC:100996-8 NCIT:C28421

`search` matches the text against term labels and synonyms (case-insensitive
substring) and lists candidates, exact label matches first. `show` prints a
term's label, definition, synonyms, parents and status, which is what a
curator needs to choose between an exact, broad, narrow or related match.

Ontologies are read through oaklib from local semantic-sql databases (downloaded
to ~/.data/oaklib on first use). LOINC is not distributed as an OBO ontology,
so it is searched on the public HL7 FHIR terminology server (tx.fhir.org);
only LOINC terms (codes such as 2160-0) are returned, not LOINC parts or answers.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

ONTOLOGIES = ["mondo", "hp", "ncit", "loinc", "uberon", "obi", "uo", "pato", "stato"]
FHIR = "https://tx.fhir.org/r4"
LOINC_CODE = re.compile(r"^\d+-\d$")
_adapters = {}


def adapter(prefix: str):
    from oaklib import get_adapter

    if prefix not in _adapters:
        _adapters[prefix] = get_adapter(f"sqlite:obo:{prefix}")
    return _adapters[prefix]


def fhir(path: str, params: dict) -> dict:
    url = f"{FHIR}/{path}?{urllib.parse.urlencode(params, doseq=True)}"
    request = urllib.request.Request(url, headers={"Accept": "application/fhir+json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def search_loinc(text: str, limit: int) -> list[tuple[str, str, str]]:
    data = fhir("ValueSet/$expand", {"url": "http://loinc.org/vs", "filter": text, "count": 100})
    hits = []
    for item in data.get("expansion", {}).get("contains", []):
        if LOINC_CODE.match(item["code"]):
            hits.append((f"LOINC:{item['code']}", item.get("display", ""), ""))
    return hits[:limit]


def search_obo(prefix: str, text: str, limit: int) -> list[tuple[str, str, str]]:
    from oaklib.datamodels.search import SearchConfiguration
    from oaklib.datamodels.search_datamodel import SearchProperty

    oak = adapter(prefix)
    config = SearchConfiguration(properties=[SearchProperty.LABEL, SearchProperty.ALIAS], is_partial=True)
    wanted = prefix.upper() if prefix != "hp" else "HP"
    hits = []
    for curie in oak.basic_search(text, config=config):
        if not curie.upper().startswith(wanted + ":"):
            continue  # skip imported terms from other ontologies
        label = oak.label(curie) or ""
        status = "OBSOLETE" if label.lower().startswith("obsolete") or curie in obsoletes(prefix) else ""
        hits.append((curie, label, status))
    needle = text.lower()
    hits.sort(key=lambda h: (h[2] != "", h[1].lower() != needle, not h[1].lower().startswith(needle), len(h[1])))
    return hits[:limit]


_obsolete_cache = {}


def obsoletes(prefix: str) -> set[str]:
    if prefix not in _obsolete_cache:
        _obsolete_cache[prefix] = set(adapter(prefix).obsoletes())
    return _obsolete_cache[prefix]


def show_loinc(code: str) -> None:
    data = fhir("CodeSystem/$lookup", {
        "system": "http://loinc.org", "code": code,
        "property": ["COMPONENT", "PROPERTY", "SYSTEM", "SCALE_TYP", "METHOD_TYP", "STATUS", "CLASS"],
    })
    print(f"LOINC:{code}")
    for parameter in data.get("parameter", []):
        if parameter["name"] == "display":
            print(f"  label: {parameter['valueString']}")
        elif parameter["name"] == "property":
            parts = {p["name"]: next((v for k, v in p.items() if k.startswith("value")), "") for p in parameter["part"]}
            value = parts.get("value")
            if isinstance(value, dict):
                value = value.get("display") or value.get("code", "")
            value = loinc_part_name(str(value))
            print(f"  {parts.get('code', '').lower()}: {value}")


def loinc_part_name(code: str) -> str:
    """Readable name of a LOINC part (e.g. LP6827-2 -> MCnc), or the code itself."""
    if not code.startswith("LP"):
        return code
    data = fhir("CodeSystem/$lookup", {"system": "http://loinc.org", "code": code})
    name = next((p["valueString"] for p in data.get("parameter", []) if p["name"] == "display"), "")
    return f"{name} ({code})" if name else code


def show_obo(curie: str) -> None:
    prefix = curie.split(":", 1)[0].lower()
    oak = adapter(prefix)
    print(curie)
    print(f"  label: {oak.label(curie)}")
    definition = oak.definition(curie)
    if definition:
        print(f"  definition: {definition}")
    synonyms = [s for s in (oak.entity_aliases(curie) or []) if s != oak.label(curie)]
    if synonyms:
        print(f"  synonyms: {'; '.join(sorted(set(synonyms))[:12])}")
    parents = [o for _, p, o in oak.relationships([curie], predicates=["rdfs:subClassOf"]) if ":" in o]
    for parent in parents:
        print(f"  is_a: {parent} {oak.label(parent)}")
    if curie in obsoletes(prefix):
        replaced = [o for _, p, o in oak.relationships([curie]) if p == "IAO:0100001"]
        print(f"  status: OBSOLETE{' replaced by ' + ', '.join(replaced) if replaced else ''}")
    else:
        print("  status: current")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="find candidate terms by label or synonym")
    search.add_argument("text")
    search.add_argument("--in", dest="ontologies", default=",".join(ONTOLOGIES),
                        help=f"comma-separated ontologies (default: all of {','.join(ONTOLOGIES)})")
    search.add_argument("--limit", type=int, default=8, help="maximum hits per ontology")
    show = sub.add_parser("show", help="print details of one or more terms")
    show.add_argument("curies", nargs="+")
    args = parser.parse_args()

    if args.command == "search":
        for prefix in [o.strip().lower() for o in args.ontologies.split(",") if o.strip()]:
            if prefix not in ONTOLOGIES:
                print(f"[{prefix}] unknown ontology; choose from {', '.join(ONTOLOGIES)}")
                continue
            try:
                hits = search_loinc(args.text, args.limit) if prefix == "loinc" else search_obo(prefix, args.text, args.limit)
            except Exception as error:  # report and continue with the other ontologies
                print(f"[{prefix}] search failed: {error}")
                continue
            print(f"[{prefix}] {len(hits)} hit(s)")
            for curie, label, status in hits:
                print(f"  {curie}\t{label}{chr(9) + status if status else ''}")
    else:
        for curie in args.curies:
            try:
                if curie.upper().startswith("LOINC:"):
                    show_loinc(curie.split(":", 1)[1])
                else:
                    show_obo(curie)
            except Exception as error:
                print(f"{curie}\n  lookup failed: {error}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
