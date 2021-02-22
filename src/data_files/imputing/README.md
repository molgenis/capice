# Creating new imputing files

In order to make a new file containing imputing files for the gaps within the CADD output data a new python file has to be created.
This readme will tell you explicitly how to do so.

## Steps

1. Create a new python file or copy `Cadd14Grch37.py` 
(___Note___: Make sure the name of the new file does __NOT__ end with abstract.py)

1. Create a new child class within the new python file with, as parent, `TemplateImputeValues` from the `impute_values_abstract.py` file. 
(___Note___: Make sure that the name of the class does __NOT__ start with Template or a double underscore)

1. Implement the abstract methods defined in the class `TemplateImputeValues` and fill them in according to your use case.

1. Implement the following function: `def __init(self):` with as first line: `super().__init(name, usable, cadd_version, grch_build)` 
where name has to be replaced with how you want the impute file to be recognized, usable to True if you want to use it, 
cadd_version to the float of the CADD version that the impute file is suitable for and 
grch_build to an integer of the genome build suitable for the impute file.

1. Run capice.py using the --overwrite_impute_file `above defined name variable` to test if all is implemented correctly.

For an example of how the methods should be filled in, see `Cadd14Grch37.py` 
