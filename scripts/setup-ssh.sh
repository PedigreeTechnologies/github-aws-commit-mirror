rm -Rf /home/circleci/.ssh/config

cat ~/.ssh/id_rsa_ffeb190510d862a23307b06f1dd70fcf

echo "Host !github.com *
User APKAYMLLNMYWO5TS2QMO
IdentityFile /home/circleci/.ssh/id_rsa_ffeb190510d862a23307b06f1dd70fcf" >> /home/circleci/.ssh/config

ssh git-codecommit.us-east-2.amazonaws.com