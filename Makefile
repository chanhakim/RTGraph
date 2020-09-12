all: gui

gui:
	$(MAKE) -C mbci_lab/res

run:
	python -m mbci_lab -v

doc:
	$(MAKE) html -C docs

.PHONY: clean
clean:
	$(MAKE) clean -C mbci_lab/res
	$(MAKE) clean -C docs
	rm -rf mbci_lab/*.pyc
	rm -rf mbci_lab/__pycache__
	rm -rf data