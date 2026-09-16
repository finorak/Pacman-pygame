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
	rm -rf dist/ build/ pac-man.spec

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

build_game:
	$(UV) add --dev pyinstaller
	$(UV) run pyinstaller \
		--onefile \
		--windowed \
		--add-data "assets:assets" \
		pac-man.py

.PHONY: install run fclean re clean debug test build_game
