NAME = pac-man

UV = uv
VENV = .venv

install:
	@$(UV) sync

run:
	@$(UV) run $(NAME).py config.json

debug:
	@$(UV) run python -m pdb $(NAME).py

clean:
	@find . -name "*.pyc" -exec rm -rf {} +
	@find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
	@rm -rf dist/ build/ pac-man.spec

fclean: clean
	@rm -rf $(VENV)

lint:
	@$(UV) run flake8 . --exclude=$(VENV)
	@$(UV) run mypy . --exclude=$(VENV)

lint-strict:
	@$(UV) run flake8 . --exclude=$(VENV)
	@$(UV) run mypy --strict . --exclude=$(VENV)

re: fclean install

build:
	@$(UV) run pyinstaller \
		--onefile \
		--windowed \
		--add-data "assets:assets" \
		--icon=assets/icon.ico \
		pac-man.py
	@cp ./config.json ./dist/
	@tar -czvf pac-man.tar.gz -C dist .
	

run_executable: build
	@./dist/$(NAME) config.json

.PHONY: install run fclean re clean debug build run_executable
