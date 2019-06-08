# Dependencies
## golang
wget https://storage.googleapis.com/golang/go1.12.5.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.12.5.linux-armv6l.tar.gz
export PATH=$PATH:/usr/local/go/bin
 - Add the export line to the $HOME/.profile to be available after a restart.
## libraries
go get github.com/gorilla/mux
go get github.com/stretchr/testify/assert

