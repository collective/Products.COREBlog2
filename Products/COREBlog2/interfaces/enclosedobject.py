from Interface import Interface, Attribute

class IEnclosedObject(Interface):
    """Marker interface for IEnclosedObject
    """

    def isEnclosedObject():
        """
        Return true if object is "enclosed object".
        """

    def getEnclosureURL():
        """
        Return URL for RSS enclosure tag.
        When you define this method,
        Be sure to imprement getEncosureContentType,getEnclosureSize
        """

    def getEncosureContentType():
        """
        Return ContentType for RSS enclosure tag.
        """

    def getEncosureSize():
        """
        Return size for RSS enclosure tag.
        """

