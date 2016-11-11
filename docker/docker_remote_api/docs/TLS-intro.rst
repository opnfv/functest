Encrypt the docker remote API via TLS for Ubuntu and CentOS

[Introduction]
The Docker daemon can listen to Docker Remote API requests via three types of
Socket: unix, tcp and fd. By default, a unix domain socket (or IPC socket) is
created at /var/run/docker.sock, requiring either root permission, or docker
group membership.

Port 2375 is conventionally used for un-encrypted communition with Docker daemon
remotely, where docker server can be accessed by any docker client via tcp socket
in local area network. You can listen to port 2375 on all network interfaces with
-H tcp://0.0.0.0:2375, where 0.0.0.0 means any available IP address on host, and
tcp://0.0.0.0:2375 indicates that port 2375 is listened on any IP of daemon host.
If we want to make docker server open on the Internet via TCP port, and only trusted
clients have the right to access the docker server in a safe manner, port 2376 for
encrypted communication with the daemon should be listened. It can be achieved to
create certificate and distribute it to the trusted clients.

Through creating self-signed certificate, and using --tlsverify command when running
Docker daemon, Docker daemon opens the TLS authentication. Thus only the clients
with related private key files can have access to the Docker daemon's server. As
long as the key files for encryption are secure between docker server and client,
the Docker daemon can keep secure. 
In summary, 
Firstly we should create docker server certificate and related key files, which 
are distributed to the trusted clients.
Then the clients with related key files can access docker server. 

[Steps]
1.0. Create a CA, server and client keys with OpenSSL.
    OpenSSL is used to generate certificate, and can be installed as follows.
    apt-get install openssl openssl-devel 

1.1 First generate CA private and public keys.
    openssl genrsa -aes256 -out ca-key.pem 4096
    openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem

    You are about to be asked to enter information that will be incorporated
    into your certificate request, where the instance of $HOST should be replaced
    with the DNS name of your Docker daemon's host, here the DNS name of my Docker
    daemon is ly.
	Common Name (e.g. server FQDN or YOUR name) []:$HOST

1.2 Now we have a CA (ca-key.pem and ca.pem), you can create a server key and
	certificate signing request.
	openssl genrsa -out server-key.pem 4096
	openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr

1.3 Sign the public key with our CA.
    TLS connections can be made via IP address as well as DNS name, they need to be
    specified when creating the certificate.

    echo subjectAltName = IP:172.16.10.121,IP:127.0.0.1 > extfile.cnf
    openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
    -CAcreateserial -out server-cert.pem -extfile extfile.cnf

1.4 For client authentication, create a client key and certificate signing request.
	openssl genrsa -out key.pem 4096
	openssl req -subj '/CN=client' -new -key key.pem -out client.csr

1.5 To make the key suitable for client authentication, create an extensions config file.
	echo extendedKeyUsage = clientAuth > extfile.cnf

1.6 Sign the public key and after generating cert.pem and server-cert.pem, two certificate
    signing requests can be removed.
	openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
	-CAcreateserial -out cert.pem -extfile extfile.cnf

1.7 In order to protect your keys from accidental damage, you may change file modes to
	be only readable.
	chmod -v 0400 ca-key.pem key.pem server-key.pem
	chmod -v 0444 ca.pem server-cert.pem cert.pem

1.8 Build docker server
	dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem \
    -H=0.0.0.0:2376
    Then, it can be seen from the command 'netstat -ntlp' that port 2376 has been listened
    and the Docker daemon only accept connections from clients providing a certificate
    trusted by our CA.

1.9 Distribute the keys to the client
    scp /etc/docker/ca.pem wwl@172.16.10.121:/etc/docker
    scp /etc/docker/cert.pem wwl@172.16.10.121:/etc/docker
    scp /etc/docker/key.pem wwl@172.16.10.121:/etc/docker
    Where, wwl and 172.16.10.121 is the username and IP of the client respectively.
    And the password of the client is needed when you distribute the keys to the client.

1.10 To access Docker daemon from the client via keys.
    docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem \
    -H=$HOST:2376 version

    Then we can operate docker in the Docker daemon from the client vis keys, for example:
    1) create container from the client
    docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=ly:2376 run -d \
    -it --name w1 grafana/grafana 
    2) list containers from the client
    docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=ly:2376 pa -a
    3) stop/start containers from the client
    docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=ly:2376 stop w1
    docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=ly:2376 start w1







