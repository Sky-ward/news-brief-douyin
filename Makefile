.RECIPEPREFIX := >
.PHONY: install fetch summarize render push all clean

install:
>pip install -r requirements.txt

fetch:
>python -m scripts.run_all --step fetch

summarize:
>python -m scripts.run_all --step summarize

render:
>python -m scripts.run_all --step render

push:
>python -m scripts.run_all --step push

all: install fetch summarize render push

clean:
>rm -rf out/*.md

