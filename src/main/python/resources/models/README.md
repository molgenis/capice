# Creating new model files

This readme is dedicated to instruct users to create new model files in case a new model has been created.

##Steps

1. Create a new file or copy one of the `capice_v1_0_0.py` or `capice_v2_0_0.py`, make sure the filename does __NOT__ end with abstract.py.

1. Create a new child class within the new file of parent class `TemplateSetup` within `model_abstract.py`, make sure that the child class does __NOT__ start with Template.

1.  Implement the abstract methods defined in the class `TemplateSetup` and fill them in to your use case.

1. Implement the following function: `def __init(self):` with as first line: `super().__init(name, usable, cadd_version, grch_build)` 
where name has to be replaced with how you want the model file to be recognized, usable to True if you want to use it, 
cadd_version to the float of the CADD version that the model file is suitable for and 
grch_build to an integer of the genome build suitable for the model file.

1. Run capice.py using the --overwrite_model_file `above defined name variable` to test if all is implemented correctly.

For an example of how the methods should be filled in, see `capice_v2_0_0.py`
