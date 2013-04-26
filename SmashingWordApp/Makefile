#
# A number of make targets to simpligy testing and setup tasks
#

# Default target: run all the tests
.PHONY: all_tests
all_tests ::

# Run the unit tests
.PHONY: unit_tests
unit_tests: 
	@echo "\n=======  Running unit tests =========\n"
	python serverTest.py
all_tests :: unit_tests

# Run the functional tests
# The functional tests are discovered by scanning files that start with test... for unittest.TestCase subclasses
.PHONY: func_tests
func_tests:
	@echo "\n======= Running functional tests ======\n"
	python -m unittest discover -v $(TESTARGS)

all_tests :: func_tests


# Make the student package
.PHONY: package
PACKAGE=loginCounterWarmup.tar.gz
package:
	cd .. && rm -f $(PACKAGE) && \
        tar cvfz $(PACKAGE) \
            --exclude .git --exclude .gitignore --exclude .idea --exclude testPrivate.py --exclude TODO --exclude '*.pyc' \
            warmup

.PHONY: post_package
post_package: 
	$(MAKE) package
	scp ../$(PACKAGE) cs169@cory.eecs.berkeley.edu:public_html/sp13/samples/$(PACKAGE)
	ssh cs169@cory.eecs.berkeley.edu chmod 0644 public_html/sp13/samples/$(PACKAGE)
