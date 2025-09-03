
.PHONY: install fetch summarize render push all clean

install:
\tpip install -r requirements.txt

fetch:
\tpython -m scripts.run_all --step fetch

summarize:
\tpython -m scripts.run_all --step summarize

render:
\tpython -m scripts.run_all --step render

push:
\tpython -m scripts.run_all --step push

all: install fetch summarize render push

clean:
\trm -rf out/*.md
