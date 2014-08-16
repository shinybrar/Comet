# VOEvent messages.
# John Swinbank, <swinbank@transientskp.org>.

# Python standard library
import re
from datetime import datetime

# XML parsing using lxml
import lxml.etree as ElementTree

from comet import __version__, __url__
from comet.utility.xml import xml_document
from comet.utility import log

ElementTree.register_namespace("voe", "http://www.ivoa.net/xml/VOEvent/v2.0")

IVORN_RE = re.compile("""ivo://
                         (?P<auth>[a-zA-Z0-9][\w\-.~*'()]{2,}) / # Authority
                         (?P<rsrc>[\w\-.~*'()/]*) \#?            # Resource name
                         (?P<localID>[\w\-.~*'()/:]*) $          # Fragment
                      """, re.VERBOSE)
def parse_ivorn(ivorn):
    """
    Takes an IVORN of the form

        ivo://authorityID/resourceKey#local_ID

    and returns (authorityID, resourceKey, local_ID). Raise if that isn't
    possible.
    """
    try:
        return IVORN_RE.match(ivorn).groups()
    except AttributeError, e:
        log.debug("Failed to parse as IVORN: ", str(e))
        raise Exception("Invalid IVORN: %s" % (ivorn,))

def broker_test_message(ivo):
    """
    Test message which is regularly broadcast to all subscribers.
    """
    root_element = ElementTree.Element("{http://www.ivoa.net/xml/VOEvent/v2.0}VOEvent",
        attrib={
            "ivorn": ivo + "#TestEvent-%s" % datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "role": "test",
            "version": "2.0",
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.ivoa.net/xml/VOEvent/v2.0 http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
        }
    )
    who = ElementTree.SubElement(root_element, "Who")
    author_ivorn = ElementTree.SubElement(who, "AuthorIVORN")
    author_ivorn.text = ivo
    date = ElementTree.SubElement(who, "Date")
    date.text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    what = ElementTree.SubElement(root_element, "What")
    description =  ElementTree.SubElement(what, "Description")
    description.text = "Broker test event generated by Comet %s." % (__version__,)
    reference = ElementTree.SubElement(what, "Reference", uri=__url__)
    return xml_document(root_element)
