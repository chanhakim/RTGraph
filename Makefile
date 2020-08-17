all: gui

gui:
	$(MAKE) -C lcbci_lab/res

run:
	python -m lcbci_lab -v

doc:
	$(MAKE) html -C docs

.PHONY: clean
clean:
	$(MAKE) clean -C lcbci_lab/res
	$(MAKE) clean -C docs
	rm -rf lcbci_lab/*.pyc
	rm -rf lcbci_lab/__pycache__
	rm -rf data