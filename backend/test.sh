# 테스트 코드

set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;` # No Color

echo "${COLOR_GREEN}Starting black${COLOR_NC}"
poetry run black .
echo "${COLOR_GREEN}OK${COLOR_NC}"

echo "${COLOR_GREEN}Starting isort${COLOR_NC}"
poetry run isort .
echo "${COLOR_GREEN}OK${COLOR_NC}"

echo "${COLOR_GREEN}Starting test with coverage${COLOR_NC}"
poetry run coverage run manage.py test
poetry run coverage report -m
echo "${COLOR_GREEN}OK${COLOR_NC}"