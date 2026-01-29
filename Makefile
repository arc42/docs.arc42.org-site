.PHONY: clean dev

clean:
	rm -rf _site

dev:
	docker compose up
