Here is some migration script for portation from COREBlog to COREBLog2.

+ coreblogexport.dtml.txt
This DTML is to write text data to migrate to COREBlog2. Put this in COREBlog instance's content folder.

+ port.py
This script is to migrate old COREBlog data(entry,comment,trackbac,category) to COREBlog2.

+ rdf91_xml.dtml.txt
DTML file for COREBlog RSS compatibility. Put this in portal_skins/custom etc.

+ rdf10_xml.dtml.txt
This is for same as upper file.

* Migration steps.

+ Put export DTML

Put coreblogexport.dtml.txt in your old COREBlog instance's contents. Then, view this script and download blog data in text format.

+ Put importing script

After setting up COREBlog2 instance on Plone site, put port.py in portal_skins/custom with ID 'port'.
Then, put exported text file created in previous step,in portal_skins/custom/, with type 'File',ID 'COREBlog_Export'.
After all, view COREBlog2 instance in Web brouser. Add '/port' in URL field and access that URL.
Wait a moment till migration is finished.

