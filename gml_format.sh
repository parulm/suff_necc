cat inputfile.gml | perl -p -e 's/\s+\[/J\[/g' | perl -p -e 's/\n/Q/g' | sed 's/QJ\[/ \[/g' | sed 's/Q/\n/g' > outputfile.gml