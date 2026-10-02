.PHONY: demo test cpp clean

demo:
	python3 scripts/run_demo.py

test:
	python3 -m unittest discover -s tests -p 'test_*.py' -v

cpp:
	g++ -std=c++17 -O2 -Wall -Wextra -pedantic lyapunov/lyapunov_engine.cpp -o lyapunov_engine

clean:
	rm -f lyapunov_engine experiments/wave/wave_output.csv experiments/wave/demo_summary.json
