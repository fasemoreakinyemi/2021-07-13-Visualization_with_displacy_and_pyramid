main(){
	ENV_NAME=conda_env
	DIR="${PWD}"
#	conda_create_env
#	conda_start_env
	install_dep
}

conda_create_env(){
	conda create -n ${ENV_NAME} python=3.6
}
conda_start_env(){
	eval "$(conda shell.bash hook)"
	conda activate ${ENV_NAME}
}
install_dep(){
#	pip install pyramid 
#	pip install -U pip setuptools wheel
#	pip install -U spacy
	python -m spacy download en_core_web_sm
#	conda install cookiecutter
#	cookiecutter --no-input --config-file ./config.yaml gh:Pylons/pyramid-cookiecutter-starter
}
main
