# This will be changed to pac-man.py later on
# AS THE SUBJECT ASK FOR IT.
NAME = pac-man.py

UV = uv
VENV = .venv

install:
	$(UV) sync

run:
	$(UV) run $(NAME) config.json

debug:
	$(UV) run python -m pdb $(NAME)

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

# this reciep is only used for testing
# launch it with the command `make -B test`
test:
	$(UV) run python -m test.main config.json

fclean: clean
	rm -rf $(VENV)

lint:
	$(UV) run flake8 . --exclude=$(VENV)
	$(UV) run mypy . --exclude=$(VENV)

lint-strict:
	$(UV) run flake8 . --exclude=$(VENV)
	$(UV) run mypy --strict . --exclude=$(VENV)

re: fclean install

.PHONY: install run fclean re clean debug test
