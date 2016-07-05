MYDIR=$(dirname $(readlink -f "$0"))
CLIENT=$(echo python-python-tackerclient_*_all.deb)
CLIREPO="tacker-client"

# Function checks whether a python egg is available, if not, installs
function chkPPkg() {
    PKG="$1"
    IPPACK=$(python - <<'____EOF'
import pip
from os.path import join
for package in pip.get_installed_distributions():
    print(package.location)
    print(join(package.location, *package._get_metadata("top_level.txt")))
____EOF
)
    echo "$IPPACK" | grep -q "$PKG"
    if [ $? -ne 0 ];then
        pip install "$PKG"
    fi
}

function envSetup() {
    apt-get install -y python-all debhelper fakeroot
    pip install --upgrade python-keystoneclient==1.7.4
    chkPPkg stdeb
}

# Function installs python-tackerclient from github
function deployTackerClient() {
    cd $MYDIR
    git clone -b 'SFC_refactor' https://github.com/trozet/python-tackerclient.git $CLIREPO
    cd $CLIREPO
    python setup.py --command-packages=stdeb.command bdist_deb
    cd "deb_dist"
    CLIENT=$(echo python-python-tackerclient_*_all.deb)
    cp $CLIENT $MYDIR
    dpkg -i "${MYDIR}/${CLIENT}"
    apt-get -f -y install
    dpkg -i "${MYDIR}/${CLIENT}"
}

envSetup
deployTackerClient
