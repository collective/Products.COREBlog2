from Interface import Interface, Attribute

class IInlineObject(Interface):
    """Marker interface for IInlineObject
    """

    def isInlineObject():
        """
        Return true if object is "Inline object",
        who must have "Inline view".
        Inline object will be shown in entry.
        Optionally, object might have "Attachment view",
        which used for object presentation, bottom of the entry.
        
        method must be accessed with permission CMFCorePermissions.View
        """

    def getInlineView():
        """
        Return path of metal, which define "Inline view" of object.

        method must be accessed with permission CMFCorePermissions.View
        """

    def getAttachmentView():
        """
        Return path to metal, ('template_name','macro_id'),
                        which define "Attachment view" of object.

        method must be accessed with permission CMFCorePermissions.View
        """

