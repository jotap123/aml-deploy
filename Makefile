SHELL := /bin/bash

train:
	python run.py task pipeline train

predict:
	python run.py task pipeline predict

tests:
