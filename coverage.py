import subprocess

def main():
	cmds = [
		["pip", "install", "coverage"],
		["coverage", "run", "-m", "unittest", "PyCode.test_order_calculator"],
		["coverage", "report", "-m"],
	]
	for cmd in cmds:
		subprocess.run(cmd, check=True)

if __name__ == "__main__":
	main()

