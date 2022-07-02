Only applies to Manual updates.

To Make the file:
Update config file and versioning
Move the updated source code into the hysteresis folder
update the index file to reflect any changes to the TOC.

run the command: sphinx-apidoc -e -o source/rst hysteresis
run the command: make html

update github



Note:
I don't know why we need both the :doc: and toc tree part of the sub-functions